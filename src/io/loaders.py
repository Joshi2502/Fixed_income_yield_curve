import pandas as pd

def load_ust_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"date","tenor","quote_type","value"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV missing columns: {required - set(df.columns)}")
    return df

def load_portfolio_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"cusip","settl_date","coupon","mat_date","face","clean_price","frequency","dcf"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV missing columns: {required - set(df.columns)}")
    return df
