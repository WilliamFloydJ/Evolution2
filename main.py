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

pixel_size = 5

cells = []
foods = []

def reset() :

    foods.clear()
    screen.blit(background, (0, 0))
    pygame.display.update()

    for int in range(500):
        food = Food(random.randint(0, width),random.randint(0, height), 50, 4 , pixel_size, background)
        food.draw(screen)
        foods.append(food)

    cells.clear()

    for int in range(20):
        cell = Cell(random.randint(0, width),random.randint(0, height),
                     random.random(),random.random(),0.1,
                     random.random(), random.random(), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)),
                     25,0.1, 0.001, pixel_size,
                     cells,foods,screen, background)
        cells.append(cell)
        cell.draw(screen)


def main_loop(pressed, pressed_pos):
    all_dirty = []
    if(len(cells) == 0):
        reset()
    for cell in list(cells):
        if pressed:
            cell.click_check(pressed_pos)
        dirty = cell.cycle()
        if dirty:
            all_dirty += dirty
    pygame.display.update(all_dirty)


clock = pygame.time.Clock()  

running = True
reset()
while running:
    clock.tick(1020)
    pressed = False
    pos = (0,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_l:
                print(len(cells))
            if event.key == pygame.K_e:
                for cell in cells:
                    if cell.canEat:
                        pygame.mouse.set_pos(cell.rect.x, cell.rect.y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pressed = True
                pos = event.pos
        
                

    main_loop(pressed, pos)
    

pygame.quit()