import pandas as pd
import matplotlib.pyplot as plt

def plot_pnl(pnl_series: pd.Series):
    plt.plot(pnl_series.index, pnl_series.cumsum(), label = "PnL")
    plt.legend(loc="upper left")
    plt.title("Cumulative PnL")
    plt.xticks(rotation = 20)
    fig=plt.gcf()
    fig.set_size_inches(14, 7)