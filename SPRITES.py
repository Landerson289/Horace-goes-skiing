import pygame
import random



class horaceSprites:
  def __init__(self):
    self.restLeft=pygame.image.load("images/HoraceWalkFront/0.png")
    var = pygame.PixelArray(self.restLeft)
    var.replace((0,0,0),(0,255,0))
    del var
    self.restLeft=pygame.transform.scale(self.restLeft,(32,32))
    
    self.restRight=pygame.transform.flip(self.restLeft,True,False)

    self.carryingLeft=pygame.image.load("images/HoraceCarryingLeft/0.png")
    var = pygame.PixelArray(self.carryingLeft)
    var.replace((0,0,0),(0,150,0))
    del var
    self.carryingLeft=pygame.transform.scale(self.carryingLeft,(48,32))

    self.carryingRight=pygame.transform.flip(self.carryingLeft,True,False)

    self.skiLeft=pygame.image.load("images/Skiing Forward.png")
    var = pygame.PixelArray(self.skiLeft)
    var.replace((0,0,0),(0,0,255))
    del var
    self.skiLeft=pygame.transform.scale(self.skiLeft,(40,40))

    self.skiRight=pygame.transform.flip(self.skiLeft,True,False)
    
class vehicles:
  def __init__(self,vehicle,lane):
    if vehicle==0: #Select type of vehicle
      self.sprite=pygame.image.load("images/Car.png")
      
      randNum=random.randint(0,1)
      if randNum==0:
        var = pygame.PixelArray(self.sprite)
        var.replace((255,0,0),(255,255,0))
        del var
      self.sprite=pygame.transform.scale(self.sprite,(64,36))
      if lane>=3:
        self.sprite=pygame.transform.flip(self.sprite,True,False)

    if vehicle==1:
      self.sprite=pygame.image.load("images/Motorbike.png")
      #var = pygame.PixelArray(self.sprite)
      #var.replace((0,0,0),(150,150,150))
      #del var
      self.sprite=pygame.transform.scale(self.sprite,(32,32))
      if lane>=3:
        self.sprite=pygame.transform.flip(self.sprite,True,False)

    if vehicle==2:
      randNum=random.randint(0,1)
      if randNum==0:
        self.sprite=pygame.image.load("images/Hardware Truck.png")
      else:
        self.sprite=pygame.image.load("images/Software Truck.png")
      #var = pygame.PixelArray(self.sprite)
      #var.replace((0,0,0),(255,0,255))
      #del var
      self.sprite=pygame.transform.smoothscale(self.sprite,(84,36))
      if lane<3:
        self.sprite=pygame.transform.flip(self.sprite,True,False)
      
    

    if vehicle==3:
      self.sprite=pygame.image.load("images/Ambulance.png")
      self.sprite=pygame.transform.scale(self.sprite,(80,34))
      if lane<3:
        self.sprite=pygame.transform.flip(self.sprite,True,False)
class Hut:
  def __init__(self):
    self.sprite=pygame.image.load("images/Ski hut.png")
    self.sprite=pygame.transform.scale(self.sprite,(80,44))
    
    var = pygame.PixelArray(self.sprite)
    var.replace((0,0,0),(0,0,255))
    del var
    
    self.door=pygame.image.load("images/square.png")
    self.door=pygame.transform.scale(self.door,(18,24))

class Tree:
 def __init__(self):
  self.sprite=pygame.image.load("images/Tree.png")
  self.sprite=pygame.transform.scale(self.sprite,(40,44))
class Hill:
  def __init__(self):
    self.sprite=pygame.image.load("images/Hill.png")
    self.sprite=pygame.transform.scale(self.sprite,(40,10))
class Flags:
  def __init__(self):
    self.leftSprite=pygame.image.load("images/Flag.png")
    self.leftSprite=pygame.transform.scale(self.leftSprite,(14,32))

    self.rightSprite=pygame.image.load("images/Flag.png")
    self.rightSprite=pygame.transform.scale(self.rightSprite,(14,32))
    var = pygame.PixelArray(self.rightSprite)
    var.replace((0,255,255),(255,0,0))
    del var
class Finish:
  def __init__(self):
    self.sprite=pygame.image.load("images/Finish line.png")
    self.sprite=pygame.transform.scale(self.sprite,(130,100))
#background=pygame.image.load("images/square.png")
#var = pygame.PixelArray(background)
#var.replace((0,0,0),(255,255,255))
#del var
#background=pygame.transform.scale(background,(405,305))

outline=pygame.image.load("images/Outline.png")
outline=pygame.transform.scale(outline,(425,325))

road=pygame.image.load("images/Road.png")
road=pygame.transform.scale(road,(405,215))


