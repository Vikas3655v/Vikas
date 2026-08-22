"""Return indices of two values whose sum equals target."""


def two_sum(numbers: list[int], target: int) -> list[int]:
    """Return the first matching pair of indices, or an empty list."""
    seen: dict[int, int] = {}

    for index, value in enumerate(numbers):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index

    return []


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))
