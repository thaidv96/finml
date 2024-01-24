from ..base_operator import BaseOperator
import pandas as pd
import numpy as np


class Log(BaseOperator):
    def __init__(self, field: str) -> None:
        self.field = field

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[f"log_{self.field}"] = np.log(df[self.field])
        return df
