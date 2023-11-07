from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import QuantileTransformer
import pandas as pd
import numpy as np

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_
    
    Method of normalization also called zscore

    Args:
        df (dataframe): signal dataframe

    Returns:
        dataframe: normalized df
    """
    temp=df.copy()
    rows=temp.shape[0]
    cols=temp.shape[1]
    temp=temp.sub(temp.mean(axis=1), axis=0)
    temp=temp.div(temp.std(axis=1),axis=0)
    temp=temp.clip(-3, 3)
    temp=temp.sub(temp.mean(axis=1), axis=0)
    temp=temp.div(temp.std(axis=1),axis=0)
    return temp

def normalize2(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Normalization by mean and median of absolute values
    
    Args:
        df (dataframe): signal dataframe

    Returns:
        dataframe: normalized df
    """
    temp=df.copy()
    rows=temp.shape[0]
    cols=temp.shape[1]
    temp=temp.sub(temp.mean(axis=1), axis=0)
    temp=temp.div(temp.abs().median(axis=1),axis=0)
    return temp

def normalize3(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Normalization by power transformer with the method yeo-johnson
    
    Args:
        df (dataframe): signal dataframe

    Returns:
        dataframe: normalized df
    """
    scaler = PowerTransformer(method="yeo-johnson")
    temp=pd.DataFrame(scaler.fit_transform(df.T).T,columns=df.columns,index=df.index)
    temp=temp.clip(-3, 3)
    return temp

def normalize4(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_
    
    Normalization by quantile transformer with a normal distribution as an output

    Args:
        df (dataframe): signal dataframe

    Returns:
        dataframe: normalized df
    """
    scaler = QuantileTransformer(n_quantiles=100,output_distribution="normal")
    temp=pd.DataFrame(scaler.fit_transform(df.T).T,columns=df.columns,index=df.index)
    temp=temp.clip(-3, 3)
    return temp

def normalize5(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_
        Normalization of a signal by ranks on a row
    Args:
        df (dataframe): signal dataframe

    Returns:
        dataframe: normalized df
    """
    temp = df.rank(axis=1, pct=True)
    temp=temp.sub(temp.mean(axis=1), axis=0)
    temp=temp.div(temp.std(axis=1),axis=0)
    temp = temp.clip(-3, 3, axis=1)
    return temp

def convert_to_weights(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_
    
    Function to convert a signal into weights
    
    Args:
        df (dataframe): a normalized signal

    Returns:
        dataframe: a df where sum of absolute values of each row equals 1
    """
    temp=df.copy()
    temp=temp.div(temp.abs().sum(axis=1),axis=0)
    return temp

def apply_normalizations(df: pd.DataFrame, normalization_choice: int) -> pd.DataFrame:
    """Fonction to apply the normalization choosen

    Args:
        df (pd.DataFrame): input dataframe that we want to normalize
        normalization_choice (int): number of the normalization we want to apply

    Returns:
        pd.DataFrame: dataframe normalized
    """
    if(normalization_choice==1) :
        df = normalize(df)
    elif(normalization_choice == 2):
        df = normalize2(df)
    elif(normalization_choice == 3):
        df = normalize3(df)
    elif(normalization_choice == 4):
        df = normalize4(df)
    elif(normalization_choice == 5):
        df = normalize5(df)
    return df
        
        