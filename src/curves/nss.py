import numpy as np
from scipy.optimize import least_squares

# Nelson–Siegel–Svensson zero rate model
def nss_rate(tau, beta):
    beta0, beta1, beta2, beta3, lam1, lam2 = beta
    tau = np.asarray(tau, dtype=float)
    x1 = (1 - np.exp(-tau/lam1)) / (tau/lam1 + 1e-12)
    x2 = x1 - np.exp(-tau/lam1)
    x3 = (1 - np.exp(-tau/lam2)) / (tau/lam2 + 1e-12) - np.exp(-tau/lam2)
    return beta0 + beta1 * x1 + beta2 * x2 + beta3 * x3

def fit_nss(tenors_years, yields, beta0_init=0.03):
    tenors = np.asarray(tenors_years, dtype=float)
    y = np.asarray(yields, dtype=float)

    # Initial guess: [beta0, beta1, beta2, beta3, lam1, lam2]
    x0 = np.array([beta0_init, -0.02, -0.02, 0.0, 1.5, 5.0])

    def residuals(b):
        z = nss_rate(tenors, b)
        return z - y

    bounds = ([-0.05,-1.0,-1.0,-1.0, 0.1, 0.1], [0.15,1.0,1.0,1.0, 10.0, 10.0])
    res = least_squares(residuals, x0, bounds=bounds, max_nfev=20000)
    return res.x

def discount_factor(tau, beta):
    z = nss_rate(tau, beta)
    return np.exp(-z * tau)
