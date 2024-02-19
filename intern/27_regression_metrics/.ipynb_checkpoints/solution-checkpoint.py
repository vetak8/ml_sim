import numpy as np


def mean_squared_error(actual: np.ndarray, predicted: np.ndarray) -> float:
    error = actual - predicted
    return np.mean(error ** 2)

def root_mean_squared_error(actual: np.ndarray, predicted: np.ndarray) -> float:
    error = actual - predicted
    return np.sqrt(np.mean(error ** 2))


def mean_absolute_error(actual: np.ndarray, predicted: np.ndarray) -> float:
    error = actual - predicted
    return np.sum(np.abs(error)) / len(actual)


def mean_absolute_percentage_error(actual: np.ndarray, predicted: np.ndarray) -> float:
    error = actual - predicted
    mape = np.mean(np.abs(error / actual))  * 100
    return mape


def r_squared(actual: np.ndarray, predicted: np.ndarray) -> float:
    numerator = np.sum((actual - predicted) ** 2)
    mean_actual = np.mean(actual)
    denominator = np.sum((actual - mean_actual) ** 2)
    return 1 - numerator / denominator

def test():
    actual = np.array([3, -0.5, 2, 7])
    predicted = np.array([2.5, 0.0, 2, 8])

    assert np.allclose(mean_squared_error(actual, predicted), 0.375)
    assert np.allclose(root_mean_squared_error(actual, predicted), 0.6123724356957945)
    assert np.allclose(mean_absolute_error(actual, predicted), 0.5)
    assert np.allclose(
        mean_absolute_percentage_error(actual, predicted), 32.73809523809524
    )
    assert np.allclose(r_squared(actual, predicted), 0.9486081370449679)

    print("All tests passed.")


if __name__ == "__main__":
    test()
