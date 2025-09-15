import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

def year_fraction_30_360(start, end):
    d1 = start.day; d2 = end.day
    m1 = start.month; m2 = end.month
    y1 = start.year; y2 = end.year
    d1 = min(d1, 30); d2 = 30 if d2 == 31 and d1 == 30 else min(d2, 30)
    return ((360*(y2-y1) + 30*(m2-m1) + (d2-d1)))/360.0

def cashflow_dates(settl_date, mat_date, freq):
    dates = []
    d = mat_date
    while d > settl_date:
        dates.append(d)
        d = d - relativedelta(months=int(12/freq))
    dates.sort()
    return dates

def accrued_interest(settl_date, last_coupon_date, coupon_rate, face, freq):
    yf = year_fraction_30_360(last_coupon_date, settl_date)
    return face * coupon_rate/freq * yf * freq

def price_coupon_bond(settl_date, mat_date, coupon_rate, face, freq, df_func):
    # df_func takes time in years -> discount factor
    cfs = []
    dates = cashflow_dates(settl_date, mat_date, freq)
    last = settl_date
    pv = 0.0
    for d in dates:
        yf = year_fraction_30_360(last, d)
        t = year_fraction_30_360(settl_date, d)  # time from settlement
        cf = face * coupon_rate/freq
        if d == dates[-1]:
            cf += face
        pv += cf * df_func(t)
        last = d
    return pv

def modified_duration(price_func, bump_bps=1.0):
    # Numerical duration around current curve using parallel shift
    base = price_func(0.0)
    bump = bump_bps/10000.0
    up = price_func(bump)
    down = price_func(-bump)
    dur = (down - up) / (2*base*bump)
    return dur

def convexity(price_func, bump_bps=1.0):
    base = price_func(0.0)
    bump = bump_bps/10000.0
    up = price_func(bump)
    down = price_func(-bump)
    conv = (up + down - 2*base) / (base * bump*bump)
    return conv
