import pandas as pd

def load_csv(file):
    try:
        df = pd.read_csv(file, encoding='ISO-8859-1')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")
