import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")
DATA_PATH.mkdir(exist_ok=True)

def load_csv(filename, columns):
    path = DATA_PATH / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=columns)

def save_csv(df, filename):
    df.to_csv(DATA_PATH / filename, index=False)
