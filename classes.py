import pygame
import math
import copy
from functions import ranDirection
from utilities import chance, clamp
from screen import width, height

milliwatts = 1.35

class Food:
    def __init__(self, x, y, energy, surface):
        self.rect = pygame.Rect(x,y,1,1)
        self.energy = energy
    
    def draw(self, surface) :
        pygame.draw.rect(surface, (3, 252, 82), self.rect)
        pygame.display.update(self.rect)

    def unDraw(self, surface) :
        surface.fill((0,0,0),self.rect)
        pygame.display.update(self.rect)

class Cell:
    def __init__(self , x , y, moveRate, growthRate, absorption, mutationRate, maxEnergy, motabolism, massRate, cells, foods, surface):
        self.rect = pygame.Rect(x,y,1,1)
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

    def draw(self, surface):
        pygame.draw.rect(surface,(255,255,255),self.rect)
        pygame.display.update(self.rect)
        
    def unDraw(self, surface, rect):
        surface.fill((0,0,0),rect)
        pygame.display.update(rect)

    def cycle(self):
        if self.energy < self.maxEnergy :
            self.energy += self.absorption * milliwatts
        if chance(self.moveRate):
            self.move(ranDirection())
        self.eat()
        self.massGain(self.massRate)
        self.deathCheck()

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
            self.cells.append(newCell)
            newCell.move(ranDirection())

    def move(self, vector2):
        self.surface.fill((255,255,255),self.rect)
        self.energyUse(1)
        self.rect.x += vector2.x
        self.rect.x = clamp(self.rect.x,0,width)
        self.rect.y += vector2.y
        self.rect.y = clamp(self.rect.y,0,height)
        self.unDraw(self.surface, self.rect)
        self.draw(self.surface)


    def eat(self):
        foodInd = self.rect.collidelist(self.foods)
        if foodInd != -1:
            food = self.foods[foodInd]
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
            self.surface.fill((255,255,255),self.rect)
            pygame.display.update(self.rect)
            del self

