def aggregate_bar(tick_df, price_col: str = "price"):
    """
    Aggregates tick data into a single bar.

    Args:
        tick_df (pandas.DataFrame): DataFrame containing tick data.

    Returns:
        dict: A dictionary containing the aggregated bar data.
            The dictionary contains the following keys:
            - timestamp (int): The timestamp of the last tick in the bar.
            - open (float): The price of the first tick in the bar.
            - high (float): The highest price in the bar.
            - low (float): The lowest price in the bar.
            - close (float): The price of the last tick in the bar.
            - volume (float): The total volume of the bar.
            - value (float): The total value of the bar.
    """
    record = {}
    record["timestamp"] = tick_df.iloc[-1]["timestamp"]
    record["relative_timestamp"] = tick_df.iloc[-1]["relative_timestamp"]
    record["open"] = tick_df.iloc[0][price_col]
    record["high"] = tick_df[price_col].max()
    record["low"] = tick_df[price_col].min()
    record["close"] = tick_df.iloc[-1][price_col]
    record["volume"] = tick_df["volume"].sum()
    record["value"] = tick_df["value"].sum()
    return record
