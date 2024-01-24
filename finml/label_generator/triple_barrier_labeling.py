import pandas as pd
import numpy as np


def triple_barrier_label(
    df: pd.DataFrame,
    side=None,
    sl=1,
    tp=1,
    max_sl=0.05,
    available_from=2.5,
    max_holding_period=6,
    bar_daily_ratio=0.1,
):
    df = gen_vertical_bar(
        df, available_from=available_from, max_holding_period=max_holding_period
    )
    df = gen_horizontal_bar(
        df,
        sl=sl,
        tp=tp,
        max_sl=max_sl,
        max_holding_period=max_holding_period,
        bar_daily_ratio=bar_daily_ratio,
    )
    df["sl"] = df["sl"].fillna(pd.to_datetime("2099-01-01"))
    df["tp"] = df["tp"].fillna(pd.to_datetime("2099-01-01"))
    df["first_touch_at"] = df[["t1", "sl", "tp"]].min(axis=1)
    df["bin"] = df[["sl", "t1", "tp"]].apply(lambda row: row.argmin(), axis=1) - 1
    df["sell_price"] = (
        df.set_index("timestamp")["close"].reindex(df.first_touch_at).values
    )
    df["returns"] = df["sell_price"] / df["close"] - 1
    if side is not None:
        df["meta_returns"] = side * df["returns"]
        df["meta_bin"] = df["meta_returns"] > 0

    return df


def gen_vertical_bar(df: pd.DataFrame, available_from=2.5, max_holding_period=6):
    if available_from == 2.5:
        df["relative_t0"] = df.apply(
            lambda row: row["relative_timestamp"].replace(hour=13, minute=0, second=0)
            + pd.Timedelta(days=2),
            axis=1,
        )
    else:
        raise NotImplementedError
    df["relative_t1"] = df.apply(
        lambda row: row["relative_timestamp"].replace(hour=14, minute=30, second=0)
        + pd.Timedelta(days=max_holding_period),
        axis=1,
    )
    df["t0"] = df["relative_t0"].map(
        lambda x: df[df["relative_timestamp"] > x]["timestamp"].min()
    )
    df["t1"] = df["relative_t1"].map(
        lambda x: df[df["relative_timestamp"] > x]["timestamp"].min()
    )
    return df


def gen_horizontal_bar(
    df, sl=2, tp=2, max_sl=0.05, max_holding_period=6, bar_daily_ratio=0.1
):
    df["bar_volatility"] = df["close"].pct_change().rolling(20).std().shift(1)
    df["onhold_volatility"] = (
        np.sqrt(max_holding_period / bar_daily_ratio) * df["bar_volatility"]
    )
    df = df.set_index("timestamp", drop=False)
    result = []
    for _idx, row in df.iterrows():
        path_prices = df[row["t0"] : row["t1"]]["close"]
        path_returns = path_prices / row.close - 1
        sl_events = path_returns[
            path_returns < min(-sl * row["onhold_volatility"], -max_sl)
        ]
        if sl_events.empty:
            row["sl"] = pd.NaT
        else:
            row["sl"] = sl_events.index[0]
        tp_events = path_returns[path_returns > tp * row["onhold_volatility"]]
        if tp_events.empty:
            row["tp"] = pd.NaT
        else:
            row["tp"] = path_returns[
                path_returns > tp * row["onhold_volatility"]
            ].index[0]
        result.append(row)
    return pd.DataFrame(result)
