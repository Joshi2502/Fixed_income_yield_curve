def dv01(price_func, bump_bps=1.0):
    base = price_func(0.0)
    up = price_func(bump_bps/10000.0)
    return (up - base) / (bump_bps/10000.0) * (-0.0001)  # price change per 1bp up (negative)
