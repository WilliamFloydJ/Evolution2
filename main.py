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

for int in range(1500):
    foods.append(Food(random.randint(0, width),random.randint(0, height)))

cells = []

for int in range(200):
    cells.append(Cell(random.randint(0, width),random.randint(0, height), 0.2,0.1,0.1,0.1,20))

def main_loop():
    for cell in list(cells):
        cell.cycle()
        foodInd = cell.rect.collidelist(foods)
        if foodInd != -1:
            foods.remove(foods[foodInd])
            del foods[foodInd]
            cell.energyGain(6)
            cell.extraMass += 0.4
            if cell.extraMass >= 1:
                cell.extraMass = 0.0
                newCell = copy.copy(cell)
                newCell.move(ranDirection())
            
        cell.draw(base_surface)
        if cell.energy <= 0:
            foods.append(Food(cell.rect.x,cell.rect.y))
            cells.remove(cell)
            del cell
    
    for food in foods:
        food.draw(base_surface)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
    base_surface.fill((0,0,0))

    main_loop()

    scaled_surface = pygame.transform.scale(base_surface, (screen_width, screen_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()