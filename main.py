import pygame
import copy
import random
from screen import width, height, screen_width, screen_height
from classes import Cell, Food
from functions import ranDirection

pygame.init()
pygame.display.set_caption("Evolution")
base_surface = pygame.Surface((width, height))
screen = pygame.display.set_mode((screen_width, screen_height))
screen_scale = screen_width / width

def reset() :
    pass

foods = []

for int in range(2500):
    food = Food(random.randint(0, width),random.randint(0, height), 50, base_surface)
    food.draw(base_surface)
    foods.append(food)

cells = []

for int in range(200):
    cells.append(Cell(random.randint(0, width),random.randint(0, height), 0.05,0.15,0.1,0.1,20,0.1,0.01,cells,foods,base_surface))

def main_loop():
    for cell in list(cells):
        cell.cycle()            

base_surface.fill((255,255,255))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()

    main_loop()

    scaled_surface = pygame.transform.scale(base_surface, (screen_width, screen_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.time.delay(100)

pygame.quit()