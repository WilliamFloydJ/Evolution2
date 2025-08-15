import random

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        self.x += other.x
        self.y += other.y

def chance(percent):
    if random.random() <= percent:
        return True
    return False

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def rangeDec(amount):
    range_arr = []
    inctament = 1/amount
    for i in range(amount):
         range_arr.append(round(i*inctament,2))
    return range_arr