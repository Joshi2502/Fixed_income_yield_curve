import numpy as np
from scipy.interpolate import CubicSpline

def spline_zero_rate(tenors_years, yields):
    ten = np.asarray(tenors_years, dtype=float)
    y = np.asarray(yields, dtype=float)
    order = np.argsort(ten)
    cs = CubicSpline(ten[order], y[order], bc_type='natural')
    return cs
