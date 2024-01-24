import pandas as pd
from .utils import aggregate_bar
from typing import Literal
def value_bar(df: pd.DataFrame, price_col:str='price', 
              value_col:str='value', bar_daily_ratio:float=0.1, 
              method:Literal['ema','ma']='ma', span:int=20,
              cutoff_atc:bool=True,
              ):
    """
    Construct OHLCV bars based on the accumulated value of an asset, using a specified ratio of the daily value as the bar size.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the asset's data, with columns for the timestamp, price, and value.
    price_col : str, optional
        The name of the column in `df` containing the asset's price. Default is 'price'.
    value_col : str, optional
        The name of the column in `df` containing the asset's value. Default is 'value'.
    bar_daily_ratio : float, optional
        The ratio of the daily value of the asset to use as the size of each bar. Default is 0.1.
    
    Returns:
    --------
    pd.DataFrame
        A new DataFrame containing the OHLCV bars for the asset, with columns for the timestamp, open, high, low, close, and volume.
    """
    # Add a 'date' column to the DataFrame
    df['date'] = df['timestamp'].dt.date
    
    # Calculate the daily value of the asset
    daily_value = df.groupby('date')[value_col].sum()
    
    # Calculate the exponential moving average of the daily value
    if method == 'ema':
        daily_threshold = daily_value.ewm(span=span).mean().shift(1).reset_index()
    elif method == 'ma':
        daily_threshold = daily_value.rolling(span).mean().shift(1).reset_index()

    daily_threshold.columns = ['date', 'daily_value']
    
    # Merge the exponential moving average of the daily value with the input DataFrame
    df = df.merge(daily_threshold, on='date', how='left')
    
    # Create OHLCV bars based on the specified ratio of the daily value of the asset
    result = []
    accumulated_row_idx = []
    accumulated_value = 0
    if cutoff_atc:
        df = df[df['timestamp'].dt.time < pd.to_datetime('14:30').time()]
    for timestamp, row in df.iterrows():
        accumulated_value += row[value_col]
        if accumulated_value > row['daily_value'] * bar_daily_ratio:
            accumulated_row_idx.append(timestamp)
            record = aggregate_bar(df.loc[accumulated_row_idx], price_col=price_col)
            record['symbol'] = row['symbol']
            result.append(record)
            accumulated_row_idx = []
            accumulated_value = 0
        else:
            accumulated_row_idx.append(timestamp)
    
    # Return the new DataFrame with OHLCV bars
    return pd.DataFrame(result)