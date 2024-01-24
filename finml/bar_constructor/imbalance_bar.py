import pandas as pd 
import numpy as np
from .utils import aggregate_bar
import logging
from tqdm import tqdm
logger = logging.getLogger(__name__)

def imbalance_bar(df:pd.DataFrame, price_col:str='price', value_col:str='value', alpha:float = 0.8, bar_daily_ratio:float=0.1, verbose=False):
    """
    Constructs imbalance bars from a DataFrame of tick data.
    [Critical] Got exploding problem. Need to be fixed.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame of tick data, with columns 'timestamp', 'price', and 'value' (optional).
    price_col : str, default 'price'
        Name of the column containing the tick prices.
    value_col : str, default 'value'
        Name of the column containing the tick values (optional).
    alpha : float, default 0.8
        Exponential decay factor for the estimation of the accumulated signed value.
    bar_daily_ratio : float, default 0.1
        Ratio of the first day's signed value to use as the initial estimate of the accumulated signed value.
    verbose: bool, default False
        If True, print progress bars.
    Returns:
    --------
    pd.DataFrame
        DataFrame of imbalance bars, with columns 'timestamp', 'open', 'high', 'low', 'close', 'volume', and 'value'.
    """
    df['sign'] = df[price_col].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else np.nan)
    df['sign'] = df['sign'].ffill()
    if value_col is not None:
        df['signed_value'] = df['sign'] * df[value_col]
    else:
        df['signed_value'] = df['sign']
    df['signed_value'].fillna(0, inplace=True)
    accumulated_signed_value = 0
    # Initialize estimated_accumulated_signed_value to the 10% of first day value
    first_day_value = df[df['timestamp'].dt.date == df['timestamp'].dt.date.iloc[0]][value_col].sum()
    estimated_accumulated_signed_value = abs(bar_daily_ratio * first_day_value)
    current_indices = []
    result = []
    e_t = 0
    imbalance_v = 0
    for idx, row in tqdm(df.iterrows(),total=df.shape[0], disable=not verbose):
        accumulated_signed_value += row['signed_value'] 
        current_indices.append(idx)
        if abs(accumulated_signed_value) > estimated_accumulated_signed_value:
            record = aggregate_bar(df.loc[current_indices])
            record['estimated_accumulated_signed_value'] = estimated_accumulated_signed_value
            record['accumulate_signed_value'] = accumulated_signed_value
            result.append(record)

            # e_t = e_t * (1-alpha) + alpha * len(current_indices)
            # imbalance_v = (1-alpha)* imbalance_v + alpha *abs(accumulated_signed_value) / e_t
            # estimated_accumulated_signed_value = e_t * imbalance_v

            estimated_accumulated_signed_value = estimated_accumulated_signed_value * (1-alpha) + alpha * abs(accumulated_signed_value)
            accumulated_signed_value = 0
            current_indices = []
    return pd.DataFrame(result)
        
