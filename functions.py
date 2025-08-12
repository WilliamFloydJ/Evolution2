import random
from utilities import Vector2

def ranDirection():
    direction = random.random()
    if direction <= 0.25:
        return Vector2(1,0)
    elif direction <= 0.5:
        return Vector2(-1,0)
    elif direction <= 0.75:
        return Vector2(0,1)
    elif direction <= 1:
        return Vector2(0,-1)