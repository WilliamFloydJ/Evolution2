import pygame
import copy
import random
from screen import width, height
from classes import Cell, Food
from functions import ranDirection

pygame.init()
pygame.display.set_caption("Evolution")
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
screen.blit(background,(0,0))


def reset() :
    pass

foods = []

for int in range(500):
    food = Food(random.randint(0, width),random.randint(0, height), 50, background)
    food.draw(screen)
    foods.append(food)

cells = []

for int in range(1):
    cell = Cell(random.randint(0, width),random.randint(0, height), 0.05,0.15,0.1,0.1,20,0.1,0.1,cells,foods,screen, background)
    cells.append(cell)
    cell.draw(screen)


def main_loop():
    for cell in list(cells):
        cell.cycle()

clock = pygame.time.Clock()  

running = True
while running:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()

    main_loop()
    

pygame.quit()