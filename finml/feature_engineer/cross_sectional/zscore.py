from ..base_operator import BaseOperator
import pandas as pd


class ZScore(BaseOperator):
    def __init__(self, field: str):
        self.field = field

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[f"{self.field}_zscore"] = (
            df.groupby("date")[self.field]
            .apply(lambda x: (x - x.mean()) / x.std())
            .reset_index(level=0, drop=True)
        )
        return df
