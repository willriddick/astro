def approach(value: float, target: float, step: float) -> float:
    if value + step < target:
        return min(target, value + step)
    elif value - step > target:
        return max(target, value - step)
    else:
        return target
