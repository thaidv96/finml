import multiprocessing as mp
import numpy as np
import pandas as pd

def mp_apply(df, func, num_processes=4):
    """
    Applies a function to a pandas DataFrame in parallel using multiprocessing.

    Args:
        df (pandas.DataFrame): The DataFrame to apply the function to.
        func (function): The function to apply to the DataFrame.
        num_processes (int): The number of processes to use for parallel processing.

    Returns:
        pandas.DataFrame: The resulting DataFrame after applying the function.
    """
    with mp.Pool(num_processes) as pool:
        results = pool.map(func, np.array_split(df, num_processes))
    return pd.concat(results)