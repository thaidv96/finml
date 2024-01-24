import numpy as np
import pandas as pd
from tqdm import tqdm
from numpy.random.mtrand import RandomState
from .metrics import measure_num_co_events


def pseudo_sequential_bootstrap(df, num_sample, seed=None):
    if isinstance(seed, RandomState):
        np.random.set_state(seed.get_state())
    else:
        np.random.seed(seed)
    if 'co_events' not in df.columns:
        df = measure_num_co_events(df)
    result = []

    proba = np.ones(df.shape[0]) / df.shape[0]
    for _ in range(num_sample):
        if len(result) > 0:
            proba = get_probability(df, proba, result[-1])
        result += [np.random.choice(range(df.shape[0]), p=proba)]
    return sorted(df.index[result])

def get_probability(df, prior_proba, chosen_idx):
    # Linear decay
    num_co_events = df.iloc[chosen_idx]['co_events']
    start_relative_idx = max(int(chosen_idx - num_co_events/2),0)
    end_relative_idx = min(int(chosen_idx + num_co_events/2), df.shape[0]-1)
    min_between = prior_proba[start_relative_idx:end_relative_idx].min()
    prior_proba[start_relative_idx:chosen_idx] -= np.linspace(prior_proba[start_relative_idx], min_between, chosen_idx-start_relative_idx)
    prior_proba[chosen_idx:end_relative_idx] -= np.linspace(min_between, prior_proba[end_relative_idx], end_relative_idx-chosen_idx)
    prior_proba[prior_proba < 0] = prior_proba[prior_proba>0].min()/10
    return prior_proba/prior_proba.sum()