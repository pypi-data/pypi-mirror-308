import pandas as pd
from odhpy import io
import re


def read(filename: str, **kwargs) -> pd.DataFrame:
    filename_lower = filename.lower()
    df = None
    if filename_lower.endswith(".res.csv"):
        df = io.read_res_csv(filename, **kwargs)
    elif filename_lower.endswith(".csv"):
        df = io.read_ts_csv(filename, **kwargs)
    elif filename_lower.endswith(".idx"):
        df = io.read_idx(filename, **kwargs)
    elif re.search(".[0-9]{2}d$", filename_lower):
        df = io.read_iqqm_lqn_output(filename, **kwargs)
    else:
        raise ValueError(f"Unknown file extension: {filename}")
    assert type(df) == pd.DataFrame
    return df
