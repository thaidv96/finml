from ..base_operator import BaseOperator
import pandas as pd


class Rank(BaseOperator):
    def __init__(self, field: str) -> None:
        self.field = field

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[f"rank_{self.field}"] = df.groupby("date")[self.field].rank()
        return df
