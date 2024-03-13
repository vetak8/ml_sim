"""Metrics."""

from typing import Any, Dict, Union, List
from dataclasses import dataclass
import datetime

import pandas as pd
import pyspark.sql as ps


@dataclass
class Metric:
    """Base class for Metric"""

    def __call__(self, df: Union[pd.DataFrame, ps.DataFrame]) -> Dict[str, Any]:
        if isinstance(df, pd.DataFrame):
            return self._call_pandas(df)

        if isinstance(df, ps.DataFrame):
            return self._call_pyspark(df)

        msg = (
            f"Not supported type of arg 'df': {type(df)}. "
            "Supported types: pandas.DataFrame, "
            "pyspark.sql.dataframe.DataFrame"
        )
        raise NotImplementedError(msg)

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        return {}


@dataclass
class CountTotal(Metric):
    """Total number of rows in DataFrame"""

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {"total": len(df)}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        return {"total": df.count()}


@dataclass
class CountZeros(Metric):
    """Number of zeros in choosen column"""

    column: str

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = sum(df[self.column] == 0)
        return {"total": n, "count": k, "delta": k / n}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col, count

        n = df.count()
        k = df.filter(col(self.column) == 0).count()
        return {"total": n, "count": k, "delta": k / n}

@dataclass
class CountNull(Metric):
    columns: List[str]
    aggregation: str = "any"

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.aggregation == 'all':
            k = sum(df[self.columns].isna().all(axis=1))
        else:
            k = sum(df[self.columns].isna().any(axis=1))
        return {"total": n, "count": k, "delta": k / n}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col, isnan, isnull
        
        n = df.count()
        
        # Проверка наличия всех NULL/NaN значений в указанных колонках
        if self.aggregation == 'all':
            condition = isnull(col(self.columns[0])) | isnan(col(self.columns[0]))
            for column in self.columns[1:]:
                condition &= (isnull(col(column)) | isnan(col(column)))
        else:
            # Проверка наличия хотя бы одного NULL/NaN значения в указанных колонках
            condition = isnull(col(self.columns[0])) | isnan(col(self.columns[0]))
            print(condition)
            for column in self.columns[1:]:
                
                condition |= (isnull(col(column)) | isnan(col(column)))
                print(condition)
    
        count_null = df.filter(condition).count()
        
        return {"total": n, "count": count_null, "delta": count_null / n}


    

@dataclass
class CountDuplicates(Metric):
    """Number of duplicates in chosen columns"""

    columns: List[str]

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = len(df[df.duplicated(subset=self.columns)])
        return {"total": n, "count": k, "delta": k / n}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import count, col, window
        
        n = df.count()
        duplicates_count = n - df.select(self.columns).dropDuplicates().count()
        return {"total": n, "count": duplicates_count, "delta": duplicates_count / n}


@dataclass
class CountValue(Metric):
    """Number of values in chosen column"""

    column: str
    value: Union[str, int, float]

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = (df[self.column] == self.value).sum()
        return {"total": n, "count": k, "delta": k / n}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col
        n = df.count()
        k = df.filter(col(self.column) == self.value).count()
        return {"total": n, "count": k, "delta": k / n}

@dataclass
class CountBelowValue(Metric):
    """Number of values below threshold"""

    column: str
    value: float
    strict: bool = False

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.strict:
            count_below = (df[self.column] < self.value).sum()
        else:
            count_below = (df[self.column] <= self.value).sum()
        return {"total": n, "count": count_below, "delta": count_below / n}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col

        n = df.count()
        if self.strict:
            count_below = df.filter(col(self.column) < self.value).count()
        else:
            count_below = df.filter(col(self.column) <= self.value).count()
            
        return {"total": n, "count": count_below, "delta": count_below / n}

@dataclass
class CountBelowColumn(Metric):
    """Count how often column X is below column Y"""

    column_x: str
    column_y: str
    strict: bool = False

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.strict:
            count_below = (df[self.column_x] < df[self.column_y]).sum()
        else:
            count_below = (df[self.column_x] <= df[self.column_y]).sum()
        return {"total": n, "count": count_below, "delta": count_below / n}

    def _call_pyspark(self, df: pd.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col

        n = df.count()
        if self.strict:
            count_below = df.filter(col(self.column_x) < col(self.column_y)).count()
        else:
            count_below = df.filter(col(self.column_x) <= col(self.column_y)).count()
        return {"total": n, "count": count_below, "delta": count_below / n}


@dataclass
class CountCB(Metric):
    """Calculate lower/upper bounds for N%-confidence interval"""

    column: str
    conf: float = 0.95

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        q_lower = (1 - self.conf) / 2
        q_upper = 1 - q_lower
        lcb = df[self.column].quantile(q_lower)
        ucb = df[self.column].quantile(q_upper)
        return {"lcb": lcb, "ucb": ucb}
        
    def _call_pyspark(self, df: pd.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col

        n = df.count()
        quantiles = df.approxQuantile(self.column, [0.5 - self.conf/2, 0.5 + self.conf/2], 0.0)
        lcb, ucb = quantiles[0], quantiles[1]
        return {"lcb": lcb, "ucb": ucb}


@dataclass
class CountRatioBelow(Metric):
    """Count how often X / Y is below Z"""

    column_x: str
    column_y: str
    column_z: str
    strict: bool = False

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.strict:
            count_below = ((df[self.column_x] / df[self.column_y]) < df[self.column_z]).sum()
        else:
            count_below = ((df[self.column_x] / df[self.column_y]) <= df[self.column_z]).sum()
        return {"total": n, "count": count_below, "delta": count_below / n}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import col
    
        # Создаем новый столбец с отношением column_x / column_y
        df = df.withColumn("ratio", col(self.column_x) / col(self.column_y))
    
        # Применяем фильтр к новому столбцу
        n = df.count()
        if self.strict:
            count_below = df.filter(col("ratio") < col(self.column_z)).count()
        else:
            count_below = df.filter(col("ratio") <= col(self.column_z)).count()
    
        return {"total": n, "count": count_below, "delta": count_below / n}


@dataclass
class CountLag(Metric):
    """A lag between latest date and today"""

    column: str
    fmt: str = "%Y-%m-%d"

    def _call_pandas(self, df: pd.DataFrame) -> Dict[str, Any]:
        today = datetime.datetime.now().strftime(self.fmt)
        df[self.column] = pd.to_datetime(df[self.column], format=self.fmt)
        last_day = df[self.column].max().strftime(self.fmt)
        last_day_datetime = df[self.column].max()
        lag = (datetime.datetime.strptime(today, self.fmt) - last_day_datetime).days
        return {"today": today, "last_day": last_day, "lag": lag}

    def _call_pyspark(self, df: ps.DataFrame) -> Dict[str, Any]:
        from pyspark.sql.functions import max, to_date, col

        today = datetime.datetime.now().strftime(self.fmt)

        # Преобразование столбца к типу данных DateType()
        df = df.withColumn(self.column, to_date(col(self.column), self.fmt))

        last_day = df.agg(max(col(self.column))).first()[0].strftime(self.fmt)
        last_day_datetime = datetime.datetime.strptime(last_day, self.fmt)

        # Исправление имени переменной
        today_datetime = datetime.datetime.strptime(today, self.fmt)

        lag = (today_datetime - last_day_datetime).days
        return {"today": today, "last_day": last_day, "lag": lag}








