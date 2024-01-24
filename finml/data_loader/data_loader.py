from .price_volume import query_ohlcv
from .universe import get_symbols


class DataLoader:
    def __init__(self, engine):
        self.engine = engine

    def query_ohlcv(
        self,
        resolution,
        symbol,
        from_date,
        to_date=None,
        chunksize=5000,
        source="ohlcv",
    ):
        return query_ohlcv(
            resolution,
            symbol,
            from_date,
            to_date,
            chunksize,
            source,
            engine=self.engine,
        )

    def get_symbols(self, basket):
        return get_symbols(basket, engine=self.engine)
