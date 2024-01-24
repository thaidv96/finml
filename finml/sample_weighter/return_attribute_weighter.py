import numpy as np
import pandas as pd


def returns_attribute_weighter(df):
    returns = df['close'].map(np.log).diff()
    weights = pd.Series(index=df.index)
    for idx, row in df.iterrows():
        weights.loc[idx] = (returns.loc[idx:row['t1']]/df['co_events'].loc[idx:row['t1']]).sum()
    return weights.abs()

