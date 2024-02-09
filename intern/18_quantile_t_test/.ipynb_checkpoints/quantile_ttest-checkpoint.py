from typing import List
from typing import Tuple

import numpy as np
from scipy.stats import ttest_ind


def quantile_ttest(
    control: List[float],
    experiment: List[float],
    alpha: float = 0.05,
    quantile: float = 0.95,
    n_bootstraps: int = 1000,
) -> Tuple[float, bool]:
    """
    Bootstrapped t-test for quantiles of two samples.
    """
    control_bootstraped_quantiles = []
    experiment_bootstraped_quantiles = []

    for _ in range(n_bootstraps):
        control_sample = np.random.choice(control, len(control), replace=True)
        experiment_sample = np.random.choice(experiment, len(experiment), replace = True)

        control_bootstraped_quantiles.append(np.quantile(control_sample, quantile))
        experiment_bootstraped_quantiles.append(np.quantile(experiment_sample, quantile))

    _, p_value = ttest_ind(control_bootstraped_quantiles, experiment_bootstraped_quantiles)
    result = bool(p_value < alpha)
    
    return p_value, result
