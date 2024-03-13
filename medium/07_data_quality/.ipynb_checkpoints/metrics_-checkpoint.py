from typing import Dict, Union, List, Any
from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy import stats
import datetime

class Metric:
    def __call__(self, df: pd.DataFrame) -> Dict[str, float]:
        return {}


@dataclass
class CountTotal(Metric):
    """Total number of rows in DataFrame"""

    def __call__(self, df: pd.DataFrame) -> Dict[str, float]:
        return {"total": len(df)}


@dataclass
class CountZeros(Metric):
    """Number of zeros in chosen column"""
    column: str

    def __call__(self, df: pd.DataFrame) -> Dict[str, float]:
        n = len(df)
        k = sum(df[self.column] == 0)
        return {"total": n, "count": k, "delta": k / n}

@dataclass
class CountNull(Metric):
    """Number of empty values in chosen columns"""

    columns: List[str]
    aggregation: str = "any"  # either "all", or "any"

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.aggregation == 'all':
            k = sum(df[self.columns].isna().all(axis=1))
        else:
            k = sum(df[self.columns].isna().any(axis=1))
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountDuplicates(Metric):
    """Number of duplicates in choosen columns"""

    columns: List[str]

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = len(df[df.duplicated(subset=self.columns)])
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountValue(Metric):
    """Number of values in chosen column"""

    column: str
    value: Union[str, int, float]

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = (df[self.column] == self.value).sum()
        return {"total": n, "count": k, "delta": k / n}

@dataclass
class CountBelowValue(Metric):
    """Number of values below threshold"""

    column: str
    value: float
    strict: bool = False

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.strict:
            count_below = (df[self.column] < self.value).sum()
        else:
            count_below = (df[self.column] <= self.value).sum()
        return {"total": n, "count": count_below, "delta": count_below / n}

@dataclass
class CountBelowColumn(Metric):
    """Count how often column X is below column Y"""

    column_x: str
    column_y: str
    strict: bool = False

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.strict:
            count_below = (df[self.column_x] < df[self.column_y]).sum()
        else:
            count_below = (df[self.column_x] <= df[self.column_y]).sum()
        return {"total": n, "count": count_below, "delta": count_below / n}

@dataclass
class CountCB(Metric):
    """Calculate lower/upper bounds for N%-confidence interval"""

    column: str
    conf: float = 0.95

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        q_lower = (1 - self.conf) / 2
        q_upper = 1 - q_lower
        lcb = df[self.column].quantile(q_lower)
        ucb = df[self.column].quantile(q_upper)
        return {"lcb": lcb, "ucb": ucb}

@dataclass
class CountRatioBelow(Metric):
    """Count how often X / Y is below Z"""

    column_x: str
    column_y: str
    column_z: str
    strict: bool = False

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.strict:
            count_below = ((df[self.column_x] / df[self.column_y]) < df[self.column_z]).sum()
        else:
            count_below = ((df[self.column_x] / df[self.column_y]) <= df[self.column_z]).sum()
        return {"total": n, "count": count_below, "delta": count_below / n}

@dataclass
class CountLag(Metric):
    """A lag between latest date and today"""

    column: str
    fmt: str = "%Y-%m-%d"

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        today = datetime.datetime.now().strftime(self.fmt)
        df[self.column] = pd.to_datetime(df[self.column], format=self.fmt)
        last_day = df[self.column].max().strftime(self.fmt)
        last_day_datetime = df[self.column].max()
        lag = (datetime.datetime.strptime(today, self.fmt) - last_day_datetime).days
        return {"today": today, "last_day": last_day, "lag": lag}
        