import pandas as pd

def price_rating(df:pd.DataFrame, price_column='close',num_daily_bars=10):
    # Short-term rating:
    daily_rolling_mean = df[price_column].rolling(num_daily_bars, min_periods=num_daily_bars).mean()
    daily_rolling_pct_mean = df[price_column].pct_change().rolling(num_daily_bars, min_periods=num_daily_bars).mean()
    daily_rolling_std = df[price_column].rolling(num_daily_bars, min_periods=num_daily_bars).std()
    daily_rolling_std = daily_rolling_std.replace(0,0.001)
    daily_rolling_std = daily_rolling_std.fillna(0.001)
    absolute_rating = daily_rolling_mean/daily_rolling_mean

    information_ratio = daily_rolling_pct_mean/daily_rolling_std
    df[f'short_term_{price_column}_absolute_rating'] = daily_rolling_mean.rolling(10*num_daily_bars,min_periods=10*num_daily_bars).rank(pct=True)
    df[f'short_term_{price_column}_momentum_rating'] = daily_rolling_pct_mean.rolling(10*num_daily_bars,min_periods=10*num_daily_bars).rank(pct=True)
    df[f'short_term_{price_column}_volatility_rating'] = daily_rolling_std.rolling(10*num_daily_bars,min_periods=10*num_daily_bars).rank(pct=True)
    df[f'short_term_{price_column}_absolute_information_ratio_rating'] = absolute_rating.rolling(10*num_daily_bars,min_periods=10*num_daily_bars).rank(pct=True)
    df[f'short_term_{price_column}_information_ratio_rating'] = information_ratio.rolling(10*num_daily_bars,min_periods=10*num_daily_bars).rank(pct=True)
    # Mid-term rating:
    two_week_rolling_mean = df[price_column].rolling(num_daily_bars*10, min_periods=num_daily_bars).mean()
    two_week_rolling_pct_mean = df[price_column].pct_change().rolling(num_daily_bars*10, min_periods=num_daily_bars).mean()
    two_week_rolling_std = df[price_column].rolling(num_daily_bars*10, min_periods=num_daily_bars).std()
    absolute_rating = two_week_rolling_mean/two_week_rolling_std
    information_ratio = two_week_rolling_pct_mean/two_week_rolling_std
    df[f'mid_term_{price_column}_absolute_rating'] = two_week_rolling_mean.rolling(100*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'mid_term_{price_column}_momentum_rating'] = two_week_rolling_std.rolling(100*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'mid_term_{price_column}_volatility_rating'] = two_week_rolling_std.rolling(100*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'mid_term_{price_column}_information_ratio_rating'] = information_ratio.rolling(100*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'mid_term_{price_column}_absolute_information_ratio_rating'] = absolute_rating.rolling(100*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)

    # Long-term rating:
    two_week_rolling_mean = df[price_column].rolling(num_daily_bars*10*4, min_periods=num_daily_bars).mean()
    two_week_rolling_pct_mean = df[price_column].pct_change().rolling(num_daily_bars*10*4, min_periods=num_daily_bars).mean()
    two_week_rolling_std = df[price_column].rolling(num_daily_bars*10*4, min_periods=num_daily_bars).std()
    absolute_rating = two_week_rolling_mean/two_week_rolling_std
    information_ratio = two_week_rolling_pct_mean/two_week_rolling_std
    df[f'long_term_{price_column}_absolute_rating'] = two_week_rolling_mean.rolling(100*2*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'long_term_{price_column}_momentum_rating'] = two_week_rolling_std.rolling(100*2*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'long_term_{price_column}_volatility_rating'] = two_week_rolling_std.rolling(100*2*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'long_term_{price_column}_information_ratio_rating'] = information_ratio.rolling(100*2*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)
    df[f'long_term_{price_column}_absolute_information_ratio_rating'] = absolute_rating.rolling(100*2*num_daily_bars, min_periods=10*num_daily_bars).rank(pct=True)

    return df
