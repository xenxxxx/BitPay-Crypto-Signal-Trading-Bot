import pandas as pd
import optuna
from src.signals_evaluation import compute_metrics
from src.signals_creation import *
import src.settings as settings
from typing import Union
import yaml
from src.settings import yaml_to_dict

config_values = settings.config_values
optim_parameters = config_values["signals_optimizations"]
lag_ranges = optim_parameters["commons"]["lag"]
normalization_ranges = optim_parameters["commons"]["normalization_choice"]
metric_to_optimize = optim_parameters["param_to_optimize"]
n_trials = optim_parameters["n_trials"]
optuna_study_direction = optim_parameters["optuna_study_direction"]
train_data = settings.train_data
returns = settings.returns
SIGNAL_SCORES_FILENAME = "best_signals_scores.yaml"
SIGNAL_PARAMETERS_FILENAME = "best_parameters.yaml"
OPTUNA_EARLY_STOPPING = optim_parameters["n_trials_before_callback"]

def params_to_optimize_with_trial(trial, signal_name:str):
    """
    Function that returns parameters to try for a signal,
    based on signal name
    :param trial: trail object of optuna
    :param signal_name: name of the signal we want to optimize
    :return: tuple of a dict of parameters and the trial
    """
    signal_parameters = optim_parameters[signal_name]
    param_names = signal_parameters.keys()
    all_trial_params = {}
    for param in param_names:
        if signal_parameters[param]["type"] == "int":
            trial_param = trial.suggest_int(
                param,
                signal_parameters[param]["min"],
                signal_parameters[param]["max"],
                signal_parameters[param]["step"]
                )
        if signal_parameters[param]["type"] == "float":
            trial_param = trial.suggest_float(
                name = param,
                low = signal_parameters[param]["min"],
                high = signal_parameters[param]["max"],
                step = signal_parameters[param]["step"]
                )
        all_trial_params[param] = trial_param
    return all_trial_params, trial


def objective(trial) -> Union[float, int]:
    """
    Objective function of the optuna study
    :param trial: trail object of optuna
    :return: metric that we want to optimize
    """
    lag = trial.suggest_int("lag",
                            lag_ranges["min"],
                            lag_ranges["max"],
                            lag_ranges["step"]
                            )
    normalization_choice = trial.suggest_int("normalization_choice",
                                             normalization_ranges["min"],
                                             normalization_ranges["max"],
                                             normalization_ranges["step"]
                                             )
    params, trial = params_to_optimize_with_trial(trial, signal_name_to_optimize)

    params.update({"lag": lag, "normalization_choice": normalization_choice})
    signal = compute_signal(signal_name_to_optimize, train_data, **params)
    metrics = compute_metrics(signal, returns)
    return metrics[metric_to_optimize]


def optimize_signal(signal_name: str) -> optuna.study.study.Study:
    """
    Function that optimizes a signal based on its name
    :param signal_name: name of the signal we want to optimize
    :return: study of all trials
    """
    global signal_name_to_optimize
    signal_name_to_optimize = signal_name
    study = optuna.create_study(direction = optuna_study_direction)
    try:
        study.optimize(objective, n_trials = n_trials, callbacks=[early_stopping_opt])
    except EarlyStoppingExceeded:
        print(f'EarlyStopping Exceeded: No new best scores on iters {OPTUNA_EARLY_STOPPING}')

    signal = compute_signal(signal_name_to_optimize, train_data, **study.best_params)
    metrics = compute_metrics(signal, returns)

    improvement = check_if_improvement(signal_name, metrics)
    if improvement:
        save_parameters(signal_name, study.best_params)
        save_scores(signal_name, metrics)

    return study


def save_parameters(signal_name: str, dict_of_parameters: dict):
    """
    Function that saves in a yaml file best parameters of a certain signal
    :param signal_name: Name of the signal that we are saving its parameters
    :param dict_of_parameters: best parameters of the signal
    :return: None
    """
    best_parameters_file = yaml_to_dict(SIGNAL_PARAMETERS_FILENAME)
    if signal_name not in best_parameters_file:
        best_parameters_file[signal_name] = {}
    best_parameters_file[signal_name] = dict_of_parameters
    with open(SIGNAL_PARAMETERS_FILENAME, 'w') as outfile:
        yaml.safe_dump(best_parameters_file, outfile, default_flow_style=False)


def save_scores(signal_name: str, dict_of_metrics: dict):
    """
    Function that saves metrics of the best combination of parameters of a signal, in a yaml file
    :param signal_name: name of the signal we are dealing with
    :param dict_of_metrics: metrics of the signal like sharpe ratio or daily pnl
    :return: None
    """
    best_scores_file = yaml_to_dict(SIGNAL_SCORES_FILENAME)
    if signal_name not in best_scores_file:
        best_scores_file[signal_name] = {}
    if "pnl_series" in dict_of_metrics:
        del dict_of_metrics["pnl_series"]
    if 'turnover_series' in dict_of_metrics:
        del dict_of_metrics["turnover_series"]
    best_scores_file[signal_name] = {k: str(round(v, 4)) if isinstance(v, float)
                                                else v for k, v in
                                                dict_of_metrics.items()}

    with open(SIGNAL_SCORES_FILENAME, 'w') as outfile:
        yaml.dump(best_scores_file, outfile, default_flow_style=False)


def check_if_improvement(signal_name: str, dict_of_metrics: dict) -> bool:
    """
    Return true if there is an improvement of the metric studied
    :param signal_name: name of the signal evaluated
    :param dict_of_metrics: metrics of the current study
    :return: True if there is an improvement
    """
    best_scores_file = yaml_to_dict(SIGNAL_SCORES_FILENAME)
    improvement = False
    if signal_name in best_scores_file:
        previous_scores = best_scores_file[signal_name]
        if ((dict_of_metrics[metric_to_optimize] > float(previous_scores[metric_to_optimize]))
            and (optuna_study_direction.lower() == "maximize")):
            improvement = True
        if ((dict_of_metrics[metric_to_optimize] < float(previous_scores[metric_to_optimize]))
            and (optuna_study_direction.lower() == "minimize")):
            improvement = True
    else:
        improvement = True
    return improvement


class EarlyStoppingExceeded(optuna.exceptions.OptunaError):
    early_stop = OPTUNA_EARLY_STOPPING
    early_stop_count = 0
    best_score = None


def early_stopping_opt(study, trial):
    """
    Function that raises an error if callback is triggered
    :param study: optuna study
    :param trial: optuna trial
    :return: None
    """
    if EarlyStoppingExceeded.best_score == None:
        EarlyStoppingExceeded.best_score = study.best_value

    if (study.best_value > EarlyStoppingExceeded.best_score
            and optuna_study_direction.lower() == "maximize") or \
            (study.best_value < EarlyStoppingExceeded.best_score
            and optuna_study_direction.lower() == "minimize"):
        EarlyStoppingExceeded.best_score = study.best_value
        EarlyStoppingExceeded.early_stop_count = 0
    else:
        if EarlyStoppingExceeded.early_stop_count > EarlyStoppingExceeded.early_stop:
            EarlyStoppingExceeded.early_stop_count = 0
            best_score = None
            raise EarlyStoppingExceeded()
        else:
            EarlyStoppingExceeded.early_stop_count = EarlyStoppingExceeded.early_stop_count+1
    print(f'EarlyStop counter: {EarlyStoppingExceeded.early_stop_count}, Best score: {study.best_value}')
    return

