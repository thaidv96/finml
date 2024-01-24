from typing import List, Union
from datetime import datetime, timedelta
import pandas as pd
from pytz import timezone

tz = timezone("Asia/Ho_Chi_Minh")


def query_ohlcv(
    resolution,
    symbol: Union[List[str], str, None],
    from_date,
    to_date=None,
    chunksize=5000,
    source="ohlcv",
    engine=None,
):
    if not to_date:
        to_date = datetime.now() + timedelta(days=1)
    if isinstance(symbol, str):
        sql = f"""
    SELECT bucket, symbol, open, high, low, close, volume, value from price_volume.{source}_{resolution}
    where symbol = '{symbol}' and bucket >= '{from_date}' and bucket <= '{to_date}'
    """
    elif isinstance(symbol, list):
        sql = f"""
    SELECT bucket, symbol, open, high, low, close, volume, value from price_volume.{source}_{resolution}
    where symbol in {tuple(symbol)} and bucket >= '{from_date}' and bucket <= '{to_date}'
    """
    elif symbol is None:
        sql = f"""
    SELECT bucket, symbol, open, high, low, close, volume, value from price_volume.{source}_{resolution}
    where bucket >= '{from_date}' and bucket <= '{to_date}'
    """
    with engine.connect() as con:
        df = pd.read_sql(sql, con, chunksize=chunksize)
    result = pd.concat(df, ignore_index=True)
    if result.empty:
        return result
    result.sort_values(by=["bucket"], inplace=True)
    result["timestamp"] = result["bucket"].dt.tz_convert(tz).dt.tz_localize(None)
    result.set_index("timestamp", inplace=True, drop=False)
    result["rank_date"] = result["timestamp"].dt.date.rank(method="dense")
    start_date = result["timestamp"].dt.date.min()
    result["relative_date"] = result["rank_date"].map(
        lambda x: pd.Timedelta(days=x - 1) + start_date
    )
    result["relative_timestamp"] = result.apply(
        lambda row: row["timestamp"].replace(
            year=row["relative_date"].year,
            month=row["relative_date"].month,
            day=row["relative_date"].day,
        ),
        axis=1,
    )

    return result
