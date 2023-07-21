import os
import pygame

class Animation:
  def __init__(self,folder,size):
    self.folder=folder
    files=os.listdir(folder)
    for i in range(len(files)):
      files[i]=folder+"/"+files[i]
      
    self.sprites=[]
    for i in files:
      sprite=pygame.image.load(i)
      sprite=pygame.transform.scale(sprite,size)
      self.sprites.append(sprite)
      
    self.spriteNum=0
    self.length=len(self.sprites)
  def update(self):
    self.spriteNum+=1
    return self.sprites[self.spriteNum%self.length]
