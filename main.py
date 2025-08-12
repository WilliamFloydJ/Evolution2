import pygame
from screen import width, height, screen_width, screen_height

pygame.init()
pygame.display.set_caption("Evolution")
base_surface = pygame.Surface((width, height))
screen = pygame.display.set_mode((screen_width, screen_height))
screen_scale = screen_width / width
