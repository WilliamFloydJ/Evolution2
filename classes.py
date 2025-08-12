import pygame
import math
from functions import ranDirection
from utilities import chance, clamp
from screen import width, height

milliwatts = 1.35

class Food:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,1,1)
    
    def draw(self, surface) :
        pygame.draw.rect(surface, (3, 252, 82), self.rect)

class Cell:
    def __init__(self , x , y, moveRate, growthRate, absorption, mutationRate, maxEnergy):
        self.rect = pygame.Rect(x,y,1,1)
        self.energy = maxEnergy
        self.extraMass = 0.0
        self.maxEnergy = maxEnergy
        self.moveRate = moveRate
        self.growthRate = growthRate
        self.absorption = absorption
        self.mutationRate = mutationRate

    def draw(self, surface):
        pygame.draw.rect(surface,(255,255,255),self.rect)

    def cycle(self):
        if self.energy < self.maxEnergy :
            self.energy += self.absorption * milliwatts
        if chance(self.moveRate):
            self.move(ranDirection())

    def energyGain(self, amount):
        if self.energy + amount <= self.maxEnergy :
            self.energy += amount
        else:
            self.energy = self.maxEnergy

    def energyUse(self, amount):
        self.energy -= amount

    def move(self, vector2):
        self.energyUse(1)
        self.rect.x += vector2.x
        self.rect.x = clamp(self.rect.x,0,width)
        self.rect.y += vector2.y
        self.rect.y = clamp(self.rect.y,0,height)

