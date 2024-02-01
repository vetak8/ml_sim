import metrics


def test_profit() -> None:
    '''
    Testing profit function
    '''
    assert metrics.profit([1, 2, 3], [1, 1, 1]) == 3


def test_margin() -> None:
    '''
    Testing margin function
    '''
    assert metrics.margin([4, 4, 4], [2, 2, 2]) == 0.5


def test_markup() -> None:
    '''
    Testing markup function
    '''
    assert metrics.markup([4, 4, 4], [2, 2, 2]) == 1
