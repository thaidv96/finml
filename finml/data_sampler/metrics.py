from ..helpers.mp_apply import mp_apply
import numpy as np
from tqdm import tqdm

tqdm.pandas()
def cal_co_event_per_row(row, df):
    return df[(df.timestamp >= row.timestamp) & (df.timestamp <= row.t1)].shape[0]

def measure_num_co_events(df):
    df['co_events'] = df.apply(lambda row: cal_co_event_per_row(row, df), axis=1)
    return df

def cal_uniqueness_per_row(row, df):
    return (1/df.loc[(df.timestamp >= row.timestamp) & (df.timestamp <= row.t1),'co_events']).mean()

def measure_uniqueness(df):
    df = measure_num_co_events(df)
    uniqueness = df.progress_apply(lambda row: cal_uniqueness_per_row(row, df), axis=1).replace([np.inf, -np.inf], np.nan)
    df['uniqueness'] = uniqueness
    return df