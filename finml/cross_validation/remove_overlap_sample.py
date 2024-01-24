import pandas as pd
def remove_overlap_sample(train_df: pd.DataFrame, test_df: pd.DataFrame):
    result = train_df.copy()
    overlap_indices = []
    for _, row in test_df.iterrows():
        start_between_indices = train_df[(train_df.timestamp >= row.timestamp) & (train_df.t1 <= row.timestamp) ].index
        end_between_indices = train_df[(train_df.t1 >= row.index) & (train_df.t1 <= row.t1)].index
        overlap_indices += list(start_between_indices) + list(end_between_indices)
    overlap_indices = list(set(overlap_indices))
    result.drop(overlap_indices, inplace=True)
    return result, test_df

