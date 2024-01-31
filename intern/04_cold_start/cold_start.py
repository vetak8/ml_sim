import pandas as pd
import numpy as np

def fillna_with_mean(df: pd.DataFrame, target: str, group: str) -> pd.DataFrame:
    '''Filling target nans mean by category'''
    df = df.copy()

    def get_filled_target(group, target, grouped_mean_by_category):
        '''Returns mean for every target by category'''
        if pd.isna(target):  # Check if target is NaN
            return np.floor(grouped_mean_by_category[group])
        return target

    grouped_mean_by_category = df.groupby(group)[target].mean().to_dict()
    df[target] = df.apply(lambda row: get_filled_target(row[group],
                                                        row[target],
                                                        grouped_mean_by_category), axis=1)
    return df

