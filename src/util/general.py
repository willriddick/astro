from random import randrange

def approach(value: float, target: float, step: float) -> float:
    if value + step < target:
        return min(target, value + step)
    elif value - step > target:
        return max(target, value - step)
    else:
        return target

def randf(start: float, stop: float, step: float) -> float:
    return randrange(int(start / step), int(stop / step)) * step
