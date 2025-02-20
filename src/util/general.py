from random import randint
from typing import TypeVar

def approach(value: float, target: float, step: float) -> float:
    if value + step < target:
        return min(target, value + step)
    elif value - step > target:
        return max(target, value - step)
    else:
        return target

def randf(start: float, stop: float, step: float) -> float:
    steps = int((stop - start) / step)
    return start + step * randint(0, steps)

T = TypeVar('T')
def get_weighted_choice(available: list[T], weights: dict[T, int]) -> T | None:
    """
    Selects an item from the available list based on weighted probabilities.
    
    Args:
        available (Sequence[T]): A sequence of available items.
        weights (Mapping[T, int]): A mapping of items to their associated weights.
        
    Returns:
        Optional[T]: A randomly selected item from the available items, 
        or None if no items are available with non-zero weights.
    """
    # Filter out items with weights of 0 or non-existent weights
    available = [item for item in available if weights.get(item, 0) > 0]

    if not available:
        return None

    # Calculate the total weight of the available items
    total_weight = sum(weights[item] for item in available)
    key = randint(0, total_weight - 1) if total_weight > 1 else 0

    # Select an item based on the random key and cumulative weights
    counter = 0
    for item in available:
        counter += weights[item]  # Use the weight from the weights dict
        if counter > key:
            return item

    return available[-1]  # Fallback in case no item is selected
