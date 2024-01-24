from ..base_indicator import BaseIndicator
import pandas as pd
import talib


class RSI(BaseIndicator):
    def __init__(self, window=14) -> None:
        self.window = window

    def transform_symbol_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[f"rsi_{self.window}"] = talib.RSI(df["close"], self.window)
        df[f"rsi_{self.window}"] = df[f"rsi_{self.window}"].fillna(50)
        return df
