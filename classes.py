import pygame
import math
import copy
from functions import ranDirection
from utilities import chance, clamp
from screen import width, height

milliwatts = 1.35
pixel_size = 5

class Food:
    def __init__(self, x, y, energy, background):
        self.rect = pygame.Rect(x,y,pixel_size,pixel_size)
        self.energy = energy
        self.background = background
        self.dirty = []
    
    def draw(self, surface) :
        pygame.draw.rect(surface, (3, 252, 82), self.rect)
        pygame.display.update(self.rect)

    def unDraw(self, surface) :
        surface.blit(self.background, self.rect, area=self.rect)

class Cell:
    def __init__(self , x , y, moveRate, growthRate, absorption, mutationRate, maxEnergy, motabolism, massRate, cells, foods, surface, background):
        self.rect = pygame.Rect(x,y,pixel_size,pixel_size)
        self.energy = maxEnergy
        self.extraMass = 0.0
        self.maxEnergy = maxEnergy
        self.moveRate = moveRate
        self.growthRate = growthRate
        self.absorption = absorption
        self.mutationRate = mutationRate
        self.motabolism = motabolism
        self.massRate = massRate
        self.cells = cells
        self.foods = foods
        self.surface = surface
        self.background = background
        self.dirty = []

    def draw(self, surface):
        pygame.draw.rect(surface,(255,255,255),self.rect)
        self.dirty.append(self.rect.copy())
        
    def update(self):
        pygame.display.update(self.dirty)
        self.dirty.clear()

    def unDraw(self, rect):
        self.surface.blit(self.background, rect, area=rect)
        self.dirty.append(rect)

    def cycle(self):
        if self.energy < self.maxEnergy :
            self.energy += self.absorption * milliwatts
        if chance(self.moveRate):
            self.move(ranDirection())
        self.eat()
        self.massGain(self.massRate)
        self.deathCheck()
        self.update()

    def energyGain(self, amount):
        if self.energy + amount <= self.maxEnergy :
            self.energy += amount
        else:
            self.energy = self.maxEnergy

    def energyUse(self, amount):
        self.energy -= amount

    def massGain(self, amount):
        self.extraMass += amount
        if self.extraMass >= 1:
            self.extraMass -= 1
            newCell = copy.copy(self)
            print(newCell)
            self.cells.append(newCell)
            newCell.draw(self.surface)
            newCell.move(ranDirection())

    def move(self, vector2):
        self.surface.fill((255,255,255),self.rect)
        old_rect = self.rect.copy()
        self.energyUse(1)
        self.rect.x += vector2.x
        self.rect.x = clamp(self.rect.x,0,width)
        self.rect.y += vector2.y
        self.rect.y = clamp(self.rect.y,0,height)
        self.unDraw(old_rect)
        self.draw(self.surface)


    def eat(self):
        foodInd = self.rect.collidelist(self.foods)
        if foodInd != -1:
            food = self.foods[foodInd]
            print(food)
            self.foods.remove(food)
            food.unDraw(self.surface)
            self.energyGain(food.energy * self.motabolism)
            del food
            self.massGain(0.4)

    def locationCheck(self):
        cellList = self.cells.copy()
        if self in cellList:
            cellList.remove(self)
        cellInd = self.rect.collidelist(cellList)
        if cellInd != -1:
            self.move(ranDirection())
    
    def deathCheck(self):
        if self.energy <= 0:
            self.foods.append(Food(self.rect.x, self.rect.y, self.maxEnergy * 0.1, self.surface))
            self.cells.remove(self)
            self.unDraw(self.rect)
            del self

