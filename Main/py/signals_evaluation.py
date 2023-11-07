import pandas as pd

def get_turnover_series(signal: pd.DataFrame) -> pd.Series:
    """_summary_

    Function to get turnover day by day of our signal already normalized
    
    Args:
        df (dataframe): signal datframe normalized and weighted

    Returns:
        series: time series of turnover
    """
    temp=signal.copy()
    temp2=temp.diff().abs()
    turnover_series = temp2.sum(axis=1)
    return turnover_series

def get_pnl_series(signal: pd.DataFrame, returns: pd.DataFrame) -> pd.Series:
    """Function that returns pnl series from a signal and returns

    Args:
        signal (pd.DataFrame): signal to evaluate
        returns (pd.DataFrame): returns matrix

    Returns:
        pd.Series: pnl series obtained
    """
    pnl = (signal * returns[signal.columns]).sum(axis=1)
    return pnl

def compute_metrics(signal: pd.DataFrame, returns: pd.DataFrame) -> dict:
    """Function that collect metrics to evaluate performance of a signal

    Args:
        signal (pd.DataFrame): dataframe of the signal
        returns (pd.DataFrame): dataframe of the returns

    Returns:
        dict: all metrics and series that defines a signal performance
    """
    pnl_series = get_pnl_series(signal, returns)
    daily_pnl = pnl_series.mean()
    sharpe_ratio = daily_pnl * (365)**0.5 / pnl_series.std()
    
    turnover_series = get_turnover_series(signal)
    daily_turnover = turnover_series.mean()
    
    fee_binance = 0.0007
    daily_benefit = daily_pnl - fee_binance * daily_turnover
    annual_benefit = daily_benefit * 365
    
    metrics = {
        "sharpe_ratio" : sharpe_ratio,
        "annual_benefit" : annual_benefit,
        "daily_benefit" : daily_benefit,
        "daily_turnover" : daily_turnover,
        "daily_pnl" : daily_pnl,
        "pnl_series" : pnl_series,
        "turnover_series" : turnover_series
    }
    return metrics
    