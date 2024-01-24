from ..base_operator import BaseOperator
import pandas as pd


class TsZscore(BaseOperator):
    def __init__(self, window: int, field: str) -> None:
        self.window = window
        self.field = field

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        if df["symbol"].nunique() == 1:
            df[f"{self.field}_ts_zscore_{self.window}"] = (
                df[self.field] - df[self.field].rolling(self.window).mean()
            ) / df[self.field].rolling(self.window).std()
        else:
            df[f"{self.field}_ts_zscore_{self.window}"] = (
                df.groupby("symbol")
                .apply(
                    lambda _df: (
                        _df[self.field] - _df[self.field].rolling(self.window).mean()
                    )
                    / _df[self.field].rolling(self.window).std()
                )
                .reset_index(level=0, drop=True)
            )
        df[f"{self.field}_ts_zscore_{self.window}"] = df[
            f"{self.field}_ts_zscore_{self.window}"
        ].fillna(0)
        return df
