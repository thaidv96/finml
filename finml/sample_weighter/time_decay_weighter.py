def time_decay_weighter(df, clf_last_w=1):
    clf_w = df['timestamp'].argsort().cumsum()
    # if clf_last_w > 0:
    slope = (1 - clf_last_w)/(clf_w.iloc[-1])
# else:
#         slope = ((1 + clf_last_w)/(clf_w.iloc[-1]))
    const = 1 - slope * clf_w.iloc[-1]
    clf_w = const + slope * clf_w
    clf_w[clf_w < 0] = 0
    return clf_w
