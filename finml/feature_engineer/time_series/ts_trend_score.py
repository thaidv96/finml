from ..base_operator import BaseOperator
import pandas as pd


class TsTrendScore(BaseOperator):
    def __init__(self, window: int, field: str) -> None:
        self.window = window
        self.field = field

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[f"{self.field}_ts_trend_score_{self.window}"] = (
            df[self.field] - df[self.field].rolling(self.window).mean()
        ) / df[self.field].rolling(self.window).std()
        df[f"{self.field}_ts_trend_score_{self.window}"] = df[
            f"{self.field}_ts_trend_score_{self.window}"
        ].fillna(0)
        return df
