import json
import numpy as np
from src.curves.nss import fit_nss, nss_rate, discount_factor

def test_nss_fit_basic():
    ten = np.array([0.5,1,2,5,10,30])
    y = np.array([0.05,0.049,0.047,0.045,0.044,0.045])
    beta = fit_nss(ten, y)
    z = nss_rate(ten, beta)
    assert np.mean((z - y)**2) < 1e-4
