from time import perf_counter
from .generate import generate_level 
from .display import Display

time1 = perf_counter()

count = 1
for i in range(count):
    seed = 'random' 
    config_path = 'configs/test1.json'
    level = generate_level(config_path)
    display = Display(level)
    print(f'\nLevel: {i+1}:\n{display}')

time2 = perf_counter()
print(f'\nTIME: {str(time2 - time1)}')
