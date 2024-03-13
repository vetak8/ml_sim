"""DQ Report."""

from typing import Dict, List, Tuple, Union
from dataclasses import dataclass
from user_input.metrics import Metric

import pandas as pd
import pyspark.sql as ps

LimitType = Dict[str, Tuple[float, float]]
CheckType = Tuple[str, Metric, LimitType]


@dataclass
class Report:
    """DQ report class."""

    checklist: List[CheckType]
    engine: str = "pandas"
    _results = {}
    def fit(self, tables: Dict[str, Union[pd.DataFrame, ps.DataFrame]]) -> Dict:
        """Calculate DQ metrics and build report."""

        if self.engine == "pandas":
            return self._fit_pandas(tables)

        if self.engine == "pyspark":
            return self._fit_pyspark(tables)

        raise NotImplementedError("Only pandas and pyspark APIs currently supported!")

    def _fit_pandas(self, tables: Dict[str, pd.DataFrame]) -> Dict:
        """Calculate DQ metrics and build report.  Engine: Pandas"""
        self.report_ = {}
        report = self.report_

        results = []
        report['title'] = f"DQ Report for tables {sorted(list(tables.keys()))}"
        for table_name, metric, limits in self.checklist:
            key = hash(str(tables[table_name].values.tobytes()))
            if key in self._results:
                result = self._results[key]
            else:
                result = {}
                result['table_name'] = table_name
                result['metric'] = str(metric)
                result['limits'] = str(limits)
                try:
                    values = metric(tables[table_name])
                    result['values'] = values
                    passed = True
                    for key, (lower, upper) in limits.items():
                        if key not in values:
                            passed = False
                            break
                        value = values[key]
                        if not (lower <= value <= upper):
                            passed = False
                            break
                    if passed:
                        result['status'] = '.'
                        result['error'] = ''
                    else:
                        result['status'] = 'F'
                        result['error'] = ''
                except Exception as e:
                    result['status'] = 'E'
                    result['error'] = type(e).__name__
                
                results.append(result)

        report['result'] = pd.DataFrame.from_records(results)

        total_checks = len(report['result'])
        passed_checks = report['result']['status'].eq('.').sum()
        failed_checks = report['result']['status'].eq('F').sum()
        errors = report['result']['status'].eq('E').sum()

        report['passed'] = passed_checks
        report['failed'] = failed_checks
        report['errors'] = errors
        report['total'] = total_checks
        report['passed_pct'] = (passed_checks / total_checks) * 100 if total_checks != 0 else 0
        report['failed_pct'] = (failed_checks / total_checks) * 100 if total_checks != 0 else 0
        report['errors_pct'] = (errors / total_checks) * 100 if total_checks != 0 else 0

        return report

    def _fit_pyspark(self, tables: Dict[str, pd.DataFrame]) -> Dict:
        """Calculate DQ metrics and build report.  Engine: PySpark"""
        self.report_ = {}
        report = self.report_

        results = []
        report['title'] = f"DQ Report for tables {sorted(list(tables.keys()))}"
        for table_name, metric, limits in self.checklist:
            key = hash(str(tables[table_name].collect()))
            if key in self._results:
                result = self._results[key]
            else:
                result = {}
                result['table_name'] = table_name
                result['metric'] = str(metric)
                result['limits'] = str(limits)
                try:
                    values = metric(tables[table_name])
                    result['values'] = values
                    passed = True
                    for key, (lower, upper) in limits.items():
                        if key not in values:
                            passed = False
                            break
                        value = values[key]
                        if not (lower <= value <= upper):
                            passed = False
                            break
                    if passed:
                        result['status'] = '.'
                        result['error'] = ''
                    else:
                        result['status'] = 'F'
                        result['error'] = ''
                except Exception as e:
                    result['status'] = 'E'
                    result['error'] = type(e).__name__
                
                results.append(result)

        report['result'] = pd.DataFrame.from_records(results)

        total_checks = len(report['result'])
        passed_checks = report['result']['status'].eq('.').sum()
        failed_checks = report['result']['status'].eq('F').sum()
        errors = report['result']['status'].eq('E').sum()

        report['passed'] = passed_checks
        report['failed'] = failed_checks
        report['errors'] = errors
        report['total'] = total_checks
        report['passed_pct'] = (passed_checks / total_checks) * 100 if total_checks != 0 else 0
        report['failed_pct'] = (failed_checks / total_checks) * 100 if total_checks != 0 else 0
        report['errors_pct'] = (errors / total_checks) * 100 if total_checks != 0 else 0

        return report

    def to_str(self) -> str:
        """Convert report to string format."""
        report = self.report_

        msg = (
            "This Report instance is not fitted yet. "
            "Call 'fit' before using this method."
        )

        assert isinstance(report, dict), msg

        pd.set_option("display.max_rows", 500)
        pd.set_option("display.max_columns", 500)
        pd.set_option("display.max_colwidth", 20)
        pd.set_option("display.width", 1000)

        return (
            f"{report['title']}\n\n"
            f"{report['result']}\n\n"
            f"Passed: {report['passed']} ({report['passed_pct']}%)\n"
            f"Failed: {report['failed']} ({report['failed_pct']}%)\n"
            f"Errors: {report['errors']} ({report['errors_pct']}%)\n"
            "\n"
            f"Total: {report['total']}"
        )
