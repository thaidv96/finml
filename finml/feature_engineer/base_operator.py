import pandas as pd


class BaseOperator:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
