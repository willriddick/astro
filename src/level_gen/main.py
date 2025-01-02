from time import perf_counter
from .level_builder import LevelBuilder 
from .display import Display
from .export import export

time1 = perf_counter()

count = 1
for i in range(count):
    seed = 'random' 
    config_path = 'src/level_gen/configs/test2.json'
    level = LevelBuilder.generate_level(config_path)
    display = Display(level)
    print(f'\nLevel: {i+1}:\n{display}')

time2 = perf_counter()
print(f'\nTIME: {str(time2 - time1)}')
