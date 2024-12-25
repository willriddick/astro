def approach(value: float, target: float, acc: float) -> float:
    if value < target:
        return min(target, value + acc)
    elif value > target:
        return max(target, value - acc)
    else:
        return target
    