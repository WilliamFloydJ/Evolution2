import pygame
import math
import random
import copy
from functions import ranDirection
from utilities import chance, clamp, rangeDec
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
        pygame.display.update(self.rect)

class Cell:
    def __init__(self , x , y, moveRate, growthRate, absorption, mutationRate, mutationAmount, color, maxEnergy, motabolism, massRate, cells, foods, surface, background):
        self.rect = pygame.Rect(x,y,pixel_size,pixel_size)
        self.energy = maxEnergy
        self.extraMass = 0.0
        self.color = color
        self.maxEnergy = maxEnergy
        self.moveRate = moveRate
        self.growthRate = growthRate
        self.absorption = absorption
        self.mutationAmount = mutationAmount
        self.mutationRate = mutationRate
        self.motabolism = motabolism
        self.massRate = massRate
        self.cells = cells
        self.foods = foods
        self.surface = surface
        self.background = background
        self.alive = True
        self.dirty = []

    def draw(self, surface):
        pygame.draw.rect(surface,self.color,self.rect,self.rect.width,2)
        self.dirty.append(self.rect.copy())
        
    def update(self):
        dirty = self.dirty.copy()
        self.dirty.clear()
        return dirty

    def unDraw(self, rect):
        self.surface.blit(self.background, rect, area=rect)
        self.dirty.append(rect)

    def cycle(self):
        if not self.alive :
            self.cells.remove(self)
            del self
        else:
            if self.energy < self.maxEnergy :
                self.energy += self.absorption * milliwatts
            if chance(self.moveRate):
                self.move(ranDirection(), 1)
            self.eat()
            self.massGain(self.massRate)
            self.locationCheck()
            self.deathCheck()
            return self.update()
        
    def mutate(self):
        select = random.random()
        range_arr = rangeDec(8)
        iter = 0
        for ran in range_arr:
            if select < ran:
                break
            iter += 1
        match iter:
            case 0:
                self.moveRate += self.mutationAmount
            case 1:
                self.growthRate += self.mutationAmount
            case 2:
                self.absorption += self.mutationAmount
            case 3:
                self.mutationRate += self.mutationAmount
            case 4:
                self.mutationAmount += self.mutationAmount
            case 5:
                self.maxEnergy += self.mutationAmount
            case 6:
                self.motabolism += self.mutationAmount
            case 7:
                self.massRate += self.mutationAmount
            case _:
                pass
        R = clamp(self.color[0] + random.randint(-2, 2),0, 255)
        G = clamp(self.color[1] + random.randint(-2, 2),0, 255)
        B = clamp(self.color[2] + random.randint(-2, 2),0, 255)
        self.color = (R,G,B)

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
            newCell.rect = pygame.Rect(self.rect.x,self.rect.y,pixel_size, pixel_size)
            if chance(newCell.mutationRate):
                newCell.mutate()
            self.cells.append(newCell)
            newCell.draw(self.surface)
            newCell.move(ranDirection(), pixel_size)

    def move(self, vector2, amount):
        self.surface.fill((255,255,255),self.rect)
        old_rect = self.rect.copy()
        self.energyUse(1)
        self.rect.x += vector2.x * amount
        self.rect.x = clamp(self.rect.x,0,width)
        self.rect.y += vector2.y * amount
        self.rect.y = clamp(self.rect.y,0,height)
        self.unDraw(old_rect)
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
            self.move(ranDirection(),pixel_size)
    
    def deathCheck(self):
        if self.energy <= 0:
            self.foods.append(Food(self.rect.x, self.rect.y, self.maxEnergy * 0.1, self.surface))
            self.unDraw(self.rect)
            self.alive = False



