import pandas as pd
from sqlalchemy import text
from typing import List, Literal


def get_symbols(
    basket: Literal["HOSE", "HNX", "UPCOM", "VN30", "VN100", "VNFINLEAD", "VNDIAMOND"],
    engine=None,
) -> List[str]:
    if basket in ("HOSE", "HNX", "UPCOM"):
        with engine.connect() as conn:
            all_symbols = conn.execute(
                text(
                    "select symbol from symbol_info.ssi_company_info where exchange = '{}'".format(
                        basket
                    )
                )
            ).fetchall()
    else:
        with engine.connect() as conn:
            all_symbols = conn.execute(
                text(
                    "select symbol from symbol_info.symbol_basket where basket = '{}'".format(
                        basket
                    )
                )
            ).fetchall()

    return [s[0] for s in all_symbols]
