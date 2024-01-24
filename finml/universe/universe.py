from sqlalchemy import create_engine
from cachetools import cached, TTLCache
import pandas as pd
from sqlalchemy import text
class Universe:
    def __init__(self,exchange='HOSE', top_liquidity=100, basket='VN100', db_engine=None):
        self.exchange = exchange.upper()
        self.top_liquidity = top_liquidity
        self.basket = basket
        self.symbols = []
        self.db_engine = db_engine
    
    def get_symbols(self):
        if self.symbols:
            return self.symbols
        if self.exchange:
            with self.db_engine.connect() as conn:
                all_symbols = conn.execute(text("select symbol from symbol_info.ssi_company_info where exchange = '{}'".format(self.exchange))).fetchall()
        else:
            with self.db_engine.connect() as conn:
                all_symbols = conn.execute(text("select symbol from symbol_info.symbol_basket where basket = '{}'".format(self.basket))).fetchall()
        
        # Filter by Liquidity
        sql = '''SELECT *
	FROM price_volume.liquidity
	where bucket = (select max(bucket) from price_volume.liquidity)
    and symbol in ({})'''.format(','.join(["'{}'".format(x[0]) for x in all_symbols]))
        df = pd.read_sql(text(sql), self.db_engine)
        df = df.sort_values(by=['rank_adv_20'])
        self.symbols = df.iloc[:self.top_liquidity].symbol.unique().tolist()
        return self.symbols

