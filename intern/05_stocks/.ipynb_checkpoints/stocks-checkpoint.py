import pandas as pd
import numpy as np

def limit_gmv(df: pd.DataFrame) -> pd.DataFrame:
    '''Returns recalculated gmv'''
    df= df.copy()
    condition = df['gmv'] / df['price']

    # Use numpy functions to efficiently calculate the adjusted GMV
    df['gmv'] = np.where(condition > df['stock'],
                         df['price'] * df['stock'],
                         df['price'] * np.floor(condition))

    return df