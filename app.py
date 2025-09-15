# yield-curve/app.py

import os, sys

# Add project root so "src" package is importable
PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import the actual Streamlit app
from src.dashboard.app import *
