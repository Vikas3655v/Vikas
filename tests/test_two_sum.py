from python.algorithms.two_sum import two_sum


def test_two_sum_finds_pair() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_two_sum_handles_duplicate_values() -> None:
    assert two_sum([3, 3], 6) == [0, 1]


def test_two_sum_returns_empty_when_missing() -> None:
    assert two_sum([1, 2, 3], 10) == []
