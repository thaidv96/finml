import pandas as pd


class BaseIndicator:
    def __init__(self) -> None:
        pass

    def transform_symbol_df(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
