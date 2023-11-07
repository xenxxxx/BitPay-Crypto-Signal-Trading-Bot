import pandas as pd
from abc import ABC, abstractmethod

from typing import Optional

import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras import layers
import math
import warnings
import os
warnings.filterwarnings("ignore")

ON_PRICING = False

class Strategy(ABC):

    @abstractmethod
    def required_rows(self):
        raise NotImplementedError("Specify required_rows!")

    @abstractmethod
    def compute_target_position(self, current_data: pd.DataFrame, current_position: float) -> Optional[float]:
        assert len(current_data) == self.required_rows  # This much data will be fed to model

        return None  # If None is returned, no action is executed


class MeanReversionStrategy(Strategy):
    required_rows = 2*24*60   # minutes of data to be fed to model.

    def compute_target_position(self, current_data: pd.DataFrame, current_position: float) -> Optional[float]:
        avg_price = current_data['price'].mean()
        current_price = current_data['price'][-1]

        target_position = current_position + (avg_price - current_price)/1000

        return target_position


class YourStrategy(Strategy):
# Specify how many minutes of data are required for live prediction

    required_rows = 60000
    
    def __init__(self):

        #lstm model
        if ON_PRICING:
            if os.path.exists('model_lstm_min'):
                self.model = keras.models.load_model('model_lstm_min')
                self.values_max = 24877.39
                self.values_min = 14490.54
                self.last_pred_price = 0
                self.last_cur_price = None
                self.last_h = None
                self.i = 0
                self.position_limit_str = 200
                self.current_position_str = 0
            else:
                self.training_data = pd.read_pickle("data/train_data.pickle")
                self.training_data.index = pd.to_datetime(self.training_data.index)
                self.training_data = self.training_data[-60000:]

                self.close_prices = self.training_data['price']
                self.values = self.close_prices.values

                self.values_max = self.values.max()
                self.values_min = self.values.min()

                self.training_data_len = math.ceil(len(self.values) * 0.7)

                self.scaler = MinMaxScaler(feature_range=(0, 1))
                self.scaled_data = self.scaler.fit_transform(self.values.reshape(-1, 1))

                self.last_pred_price = 0
                self.last_h = None

                self.train_data = self.scaled_data[0: self.training_data_len, :]

                x_train = []
                y_train = []

                for i in range(60, len(self.train_data)):
                    x_train.append(self.train_data[i - 60:i, 0])
                    y_train.append(self.train_data[i, 0])

                x_train, y_train = np.array(x_train), np.array(y_train)
                x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

                test_data = self.scaled_data[self.training_data_len - 60:, :]
                x_test = []
                y_test = self.values[self.training_data_len:]

                for i in range(60, len(test_data)):
                    x_test.append(test_data[i - 60:i, 0])

                x_test = np.array(x_test)
                x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

                self.model = keras.Sequential()
                self.model.add(layers.LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
                self.model.add(layers.LSTM(100, return_sequences=False))
                self.model.add(layers.Dense(25))
                self.model.add(layers.Dense(1))
                self.model.summary()

                self.model.compile(optimizer='adam', loss='mean_squared_error')
                self.model.fit(x_train, y_train, batch_size=1, epochs=3)

                self.model.compute_output_shape(input_shape=(1, 1))
                self.model.save("model_lstm_min")

        else:
            pass

        self.max_in_new_cur_phase_up = 0
        self.max_in_new_cur_phase_down = 0
        self.time_in_new_phase_up = 0
        self.time_in_new_phase_up_adv = 0
        self.time_in_new_phase_down_adv = 0
        self.time_in_new_phase_down = 0
        self.k = 0
        self.last_phase = 0
        self.cur_phase = 0
        self.phase_time_down = 0
        self.phase_time_up = 0
        self.k_len_m2 = 0
        self.k_len_m2_adv = 0
        self.k_len_m2_down_adv = 0
        self.k_len_m2_down = 0
        self.new_part = 0
        self.new_part_last = 0

        self.stop_loss = False

        self.time_long_down = 0

    def compute_target_position(self, current_data: pd.DataFrame, current_position: float) -> Optional[float]:#, simulation_data: pd.DataFrame
#         pass  # produce inputs to model from datafram, compute predictions and submit new target position

        current_price = current_data.price[-1]
        av_price = current_data['price'][-42:-12].mean()
        av_5_price = current_data['price'][-17:-2].mean()
        vol_feat = ((current_data.volume[-1] - current_data.volume[-3]) -
                    (current_data.volume[-2] - current_data.volume[-4])) / (current_data.volume[-2] - current_data.volume[-4])
        vol_feat_back = ((current_data.volume[-2] - current_data.volume[-4]) -
                         (current_data.volume[-3] - current_data.volume[-5])) / (
                                    current_data.volume[-3] - current_data.volume[-5])

        #++

        if ON_PRICING:
            close_prices = pd.DataFrame(current_data['price'])
            close_prices = close_prices[-60:]
            values_cur = close_prices['price'].values

            X_std = (values_cur - self.values_min) / (self.values_max - self.values_min)  # если сохранять модель, то нужно фиксировать
            scaled_data = X_std.reshape(-1, 1)
            test_data = scaled_data[:, :]

            x_test = []

            x_test.append(test_data[:, 0])
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            predictions = self.model.predict(x_test, verbose=0)
            predictions = (predictions * (self.values_max - self.values_min) + self.values_min)
            target_price = predictions[0, 0]
            delta_position = abs(target_price - current_price)

        else:
            delta_position = 100000
        #++
        self.new_part_last = self.new_part

        if current_data['price'][-45000:-2].mean() > current_data['price'][-25000:-2].mean():
            self.time_long_down += 1
        else:
            self.time_long_down = 0

        if av_5_price - av_price > 30 and av_5_price - av_price > self.max_in_new_cur_phase_up:
            self.new_part = 10
            self.time_in_new_phase_up += 1
            self.time_in_new_phase_down = 0
            self.time_in_new_phase_down_adv = 0
            self.time_in_new_phase_up_adv = 0

        elif av_5_price - av_price > 30 and av_5_price - av_price < self.max_in_new_cur_phase_up:
            self.new_part = 15
            self.time_in_new_phase_up_adv += 1
            self.time_in_new_phase_down = 0
            self.time_in_new_phase_down_adv = 0
            self.time_in_new_phase_up = 0

        elif av_5_price - av_price < -30 and av_5_price - av_price > self.max_in_new_cur_phase_down:
            self.time_in_new_phase_up_adv = 0
            self.time_in_new_phase_up = 0
            self.time_in_new_phase_down_adv = 0
            self.time_in_new_phase_down += 1
            self.new_part = -10

        elif av_5_price - av_price < -30 and av_5_price - av_price < self.max_in_new_cur_phase_down:  ##
            self.time_in_new_phase_up = 0
            self.time_in_new_phase_up_adv = 0
            self.time_in_new_phase_down = 0
            self.time_in_new_phase_down_adv += 1
            self.new_part = -15

        else:
            self.new_part = 0
            self.time_in_new_phase_up = 0
            self.time_in_new_phase_up_adv = 0
            self.time_in_new_phase_down = 0
            self.time_in_new_phase_down_adv = 0


        if av_5_price - av_price > 30:
            if av_5_price - av_price > self.max_in_new_cur_phase_up:
                self.max_in_new_cur_phase_up = av_5_price - av_price
                self.max_in_new_cur_phase_down = 0
            else:
                self.max_in_new_cur_phase_down = 0

        elif av_5_price - av_price < -30:
            if av_5_price - av_price < self.max_in_new_cur_phase_down:
                self.max_in_new_cur_phase_down = av_5_price - av_price
                self.max_in_new_cur_phase_up = 0
            else:
                self.max_in_new_cur_phase_up = 0

        else:
            self.max_in_new_cur_phase_up = 0
            self.max_in_new_cur_phase_down = 0

        self.last_phase = self.cur_phase

        if self.new_part == + 10 or self.new_part == + 15:
            self.cur_phase = + 1
        else:
            self.cur_phase = - 1

        if self.k == 0:
            if (self.cur_phase + self.last_phase) == - 1:
                self.phase_time_down += 1
                self.phase_time_up = 0
            else:
                self.phase_time_up += 1
        else:
            if (self.cur_phase + self.last_phase) == - 2:
                self.phase_time_down += 1
            elif (self.cur_phase + self.last_phase) == 0:  # special lag 1 min
                self.phase_time_down = 0
                self.phase_time_up = 0
            else:
                self.phase_time_up += 1
                self.phase_time_down = 0


        if current_price > av_5_price and current_price > av_price:
            self.new_tst = + 2
        elif current_price > av_5_price and current_price < av_price:  # what if 4 <-> 2 to try
            self.new_tst = + 1
        elif current_price < av_5_price and current_price < av_price:
            self.new_tst = - 2
        elif current_price < av_5_price and current_price > av_price:
            self.new_tst = - 1


        if self.new_part == + 10:
            self.k_len_m2 += 1  # rename late
            self.k_len_m2_adv = 0
            self.k_len_m2_down_adv = 0
            self.k_len_m2_down = 0

        elif self.new_part == + 15:
            self.k_len_m2_adv += 1
            self.k_len_m2 = 0
            self.k_len_m2_down_adv = 0
            self.k_len_m2_down = 0

        elif self.new_part == - 10:
            self.k_len_m2_down += 1
            self.k_len_m2 = 0
            self.k_len_m2_adv = 0
            self.k_len_m2_down_adv = 0

        elif self.new_part == - 15:
            self.k_len_m2_down_adv += 1
            self.k_len_m2 = 0
            self.k_len_m2_adv = 0
            self.k_len_m2_down = 0

        else:
            self.k_len_m2 = 0
            self.k_len_m2_adv = 0
            self.k_len_m2_down_adv = 0
            self.k_len_m2_down = 0


        if self.new_part == + 10:# and self.stop_loss == False:

            if self.k_len_m2 == 1 and vol_feat < -0.25 and (vol_feat_back * vol_feat) > 0:
                delta_pos = - delta_position

            elif self.k_len_m2 == 1 and vol_feat < -0.25 and (vol_feat_back * vol_feat) < 0:
                delta_pos = + delta_position

            else:
                if self.new_part_last != + 15:
                    delta_pos = - (np.sin(np.pi * 2 * self.k_len_m2 / 5) - np.sin(np.pi * 2 * (self.k_len_m2 - 1) / 5)) * 0.002
                else:
                    delta_pos = - current_position

        elif self.new_part == + 15:

            if self.k_len_m2_adv == 1 and vol_feat > -0.35 and (vol_feat_back * vol_feat) > 0:
                delta_pos = - delta_position

            else:
                if self.new_part_last != + 10:
                    delta_pos = - (np.sin(np.pi * 2 * self.k_len_m2_adv / 5) - np.sin(np.pi * 2 * (self.k_len_m2_adv - 1) / 5)) * 0.002
                else:
                    delta_pos = - current_position

        elif self.new_part == - 10:

            if self.k_len_m2_down == 1 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) > 0 and self.time_long_down < 25000 and self.time_long_down > 0:
                delta_pos = + delta_position

            elif self.k_len_m2_down == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat)) > 0 and self.time_long_down > 25000:
                delta_pos = - delta_position

            elif self.k_len_m2_down == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat)) > 0 and self.time_long_down == 0 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) > 50:
                delta_pos = - delta_position

            elif self.k_len_m2_down == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat)) > 4.5 and self.time_long_down == 0 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) < 50:
                delta_pos = + delta_position

            elif self.k_len_m2_down == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat)) > 0 and self.time_long_down == 0 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) < 4:
                delta_pos = + delta_position

            elif self.k_len_m2_down == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat)) > 4 and self.time_long_down == 0 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) < 4.5:
                delta_pos = - delta_position

            elif self.k_len_m2_down == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat)) < 0:
                delta_pos = 0

            else:
                if self.new_part_last == -15:
                    delta_pos = - current_position
                else:
                    delta_pos = + current_position / 6

        elif self.new_part == - 15 and self.k_len_m2_down_adv <= 2:

            if self.k_len_m2_down_adv == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat_back)) > 0.3 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) < 100 and (vol_feat_back * vol_feat) > 0 and abs(
                    vol_feat) > 0.35 and abs(vol_feat) < 0.5:
                delta_pos = - delta_position

            elif self.k_len_m2_down_adv == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat_back)) > 0.3 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) < 100 and (vol_feat_back * vol_feat) > 0 and abs(vol_feat) > 0.5:
                delta_pos = + 0

            elif self.k_len_m2_down_adv == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat_back)) > 0.3 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) > 100 and (vol_feat_back * vol_feat) > 0 and abs(vol_feat) > 0.35:
                delta_pos = - delta_position

            elif self.k_len_m2_down_adv == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat_back)) > 0.3 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) > 100 and (vol_feat_back * vol_feat) > 0 and abs(vol_feat) < 0.35:
                delta_pos = + delta_position

            elif self.k_len_m2_down_adv == 1 and ((vol_feat - vol_feat_back) / abs(vol_feat_back)) < 0 and (
                    (vol_feat - vol_feat_back) / abs(vol_feat)) > 0:
                delta_pos = + 0

            else:
                if self.new_part_last == -10:
                    delta_pos = - current_position
                else:
                    delta_pos = + current_position / 8

        else:
            delta_pos = - current_position

        self.k += 1
        target_position = current_position + delta_pos

        return target_position