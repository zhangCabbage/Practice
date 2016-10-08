#coding:utf-8

from random import random

#
#
#
def move_cars(car_positions):
    return map(lambda x: x + 1 if random() > 0.3 else x,
               car_positions)

def output_car(car_position):
    return '-' * car_position

def run_step_of_race(state):
    return {'time': state['time'] - 1,
            'car_positions': move_cars(state['car_positions'])}

def draw(state):
    print ''
    print '\n'.join(map(output_car, state['car_positions']))

def race(state):
    draw(state)
    if state['time']:
        race(run_step_of_race(state))

# race({'time': 5, 'car_positions': [1, 1, 1]})


#
# python中关于pipeline的实现
#
def even_filter(nums):
    return filter(lambda x: x%2==0, nums)

def multiply_by_three(nums):
    return map(lambda x: x*3, nums)

def convert_to_string(nums):
    return map(lambda x: 'The Number: %s' % x,  nums)

def pipeline_func(data, fns):
    # 关于reduce第三个参数是初值
    return reduce(lambda a, x: x(a), fns, data)

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pipeline = pipeline_func(nums, [even_filter, multiply_by_three, convert_to_string])
for num in pipeline:
    print num
