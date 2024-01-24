import pandas as pd
import numpy as np
from tqdm import tqdm


def gen_indicator_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate an indicator matrix based on a DataFrame of events.

    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame of events with columns 't1' and 'timestamp'.

    Returns:
    --------
    pd.DataFrame
        An indicator matrix with 1's indicating the presence of an event and 0's otherwise.
    """
    result = pd.DataFrame(0, index=df.index, columns=range(df.shape[0]))
    for idx, (timestamp, row) in enumerate(df.iterrows()):
        result.loc[timestamp: row['t1'], idx] = 1
    return result

def get_avg_uniqueness(indicator_matrix:pd.DataFrame):
    """
    Calculates the average uniqueness of a given indicator matrix.

    Parameters:
    indicator_matrix (pd.DataFrame): A pandas DataFrame containing the indicator matrix.

    Returns:
    float: The average uniqueness of the indicator matrix.
    """
    c = indicator_matrix.sum(axis=1)
    u = indicator_matrix.div(c, axis=0)
    avg_u = u[u>0].mean()
    return avg_u

def sequential_bootstrap(bar_df: pd.DataFrame, num_sample:int):
    indicator_matrix = gen_indicator_matrix (bar_df)
    if num_sample is None:
        num_sample = indicator_matrix.shape[1]
    result = []
    for i in tqdm(range(num_sample),total=num_sample):
        avg_u = pd.Series()
        for i in indicator_matrix:
            sub_indicator_matrix = indicator_matrix[result+[i]]
            avg_u.loc[i] = get_avg_uniqueness(sub_indicator_matrix).iloc[-1]
        prob = avg_u/avg_u.sum()
        result += [np.random.choice(indicator_matrix.columns, p=prob)]
    return result