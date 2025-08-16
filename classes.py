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
    def __init__(self, x, y, energy, mass, background):
        self.rect = pygame.Rect(x,y,pixel_size,pixel_size)
        self.energy = energy
        self.mass = mass
        self.background = background
        self.dirty = []
        self.color = (clamp(252 - self.energy * 4,0,255), 252, 82)
    
    def draw(self, surface) :
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.display.update(self.rect)
    
    def draw_without(self, surface) :
        pygame.draw.rect(surface, self.color, self.rect)

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

    def __str__(self):
        return f"energy = {self.energy}; color = {self.color}; moveRate = {self.moveRate}; growthRate = {self.growthRate}; absorption = {self.absorption}; mutationRate = {self.mutationRate}; mutationAmount = {self.mutationAmount}; maxEnergy = {self.maxEnergy}; motabolism = {self.motabolism}; massRate = {self.massRate}; extraMass = {self.extraMass}"

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
                if chance(0.5):
                    self.moveRate -= self.mutationAmount
                else:
                    self.moveRate += self.mutationAmount
                self.moveRate = clamp(self.moveRate, 0.0001, 1)
            case 1:
                if chance(0.5):
                    self.growthRate -= self.mutationAmount
                else:
                    self.growthRate += self.mutationAmount
                self.growthRate = clamp(self.growthRate, 0.0001, 1)
            case 2:
                if chance(0.5):
                    self.absorption -= self.mutationAmount
                else:
                    self.absorption += self.mutationAmount
                self.absorption = clamp(self.absorption, 0.0001, 1)
            case 3:
                if chance(0.5):
                    self.mutationRate -= self.mutationAmount
                else:
                    self.mutationRate += self.mutationAmount
                self.mutationRate = clamp(self.mutationRate, 0.0001, 1)
            case 4:
                if chance(0.5):
                    self.mutationAmount -= self.mutationAmount
                else:
                    self.mutationAmount += self.mutationAmount
                self.mutationAmount = clamp(self.mutationAmount, 0.0001, 1)
            case 5:
                if chance(0.5):
                    self.maxEnergy -= self.mutationAmount
                else:
                    self.maxEnergy += self.mutationAmount
                self.maxEnergy = clamp(self.maxEnergy, 1, 1000)
            case 6:
                if chance(0.5):
                    self.motabolism -= self.mutationAmount /4
                else:
                    self.motabolism += self.mutationAmount /4
                self.motabolism = clamp(self.motabolism, 0.0001, 0.2)
            case 7:
                if chance(0.5):
                    self.massRate -= self.mutationAmount / 10
                else:
                    self.massRate += self.mutationAmount / 10
                self.massRate = clamp(self.massRate, 0.0001, 0.01)
            case _:
                pass
        R = clamp(self.color[0] + random.randint(-20, 20),0, 255)
        G = clamp(self.color[1] + random.randint(-20, 20),0, 255)
        B = clamp(self.color[2] + random.randint(-20, 20),0, 255)
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
        if self.extraMass >= 1 and self.energy > 5:
            self.extraMass -= 1
            newCell = copy.copy(self)
            self.energy /= 2
            newCell.energy /= 2
            newCell.rect = pygame.Rect(self.rect.x,self.rect.y,pixel_size, pixel_size)
            if chance(newCell.mutationRate):
                newCell.mutate()
            self.cells.append(newCell)
            newCell.draw(self.surface)
            newCell.move(ranDirection(), pixel_size)

    def move(self, vector2, amount):
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
            self.massGain((food.mass / 2) * self.motabolism)
            del food

    def locationCheck(self):
        cellList = self.cells.copy()
        if self in cellList:
            cellList.remove(self)
        cellInd = self.rect.collidelist(cellList)
        if cellInd != -1:
            self.move(ranDirection(),pixel_size/2)

    def click_check(self, position):
        if self.rect.collidepoint(position):
            print(self)
        
    
    def deathCheck(self):
        if self.energy <= 0:
            food = Food(self.rect.x, self.rect.y, self.maxEnergy * 0.1, self.extraMass, self.surface)
            food.draw_without(self.surface)
            self.dirty.append(food.rect)
            self.foods.append(food)
            self.alive = False



