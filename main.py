import pygame, sys
from pygame.locals import QUIT
from pygame import mixer
import time
import random
import SPRITES
import animate

pygame.init()
mixer.init()
screen = pygame.display.set_mode((425,325))
pygame.display.set_caption('Horace goes skiing')


def draw_text(font,text,col,size,x,y):
  font=pygame.font.Font(font,size)
  img = font.render(text,True,col)
  screen.blit(img,(x,y))
  return img
  
def randColour():
  list = [0,255]
  colour = (list[random.randint(0,1)], list[random.randint(0,1)], list[random.randint(0,1)])
  if colour == (0,0,0) or colour == (255,255,255):
    colour = randColour()
  return colour

def intro():
  startTime = time.time()
  prevTime=startTime
  colour=randColour()
  count=0
  play=True
  text="COPYRIGHT 1982 BEAM SOFTWARE - WRITTEN BY WILLIAM TANG - REMADE BY LACHLAN ANDERSON - "
  mixer.music.load("Start sound.mp3")
  mixer.music.set_volume(5)
  mixer.music.play()
  while play==True:
    if prevTime%1>time.time()%1:
      colour=randColour()
    if prevTime%0.1>time.time()%0.1:
      count+=1
    screen.fill((255,255,255))
    draw_text("MotorolaScreentype.ttf","HORACE",colour,75,115,30)
    draw_text("MotorolaScreentype.ttf","GOES",colour,75,145,115)
    draw_text("MotorolaScreentype.ttf","SKIING",colour,75,120,200)
    draw_text("mainfont.ttf",text[count:count+30],(0,0,255),20,20,285)
    if count==len(text)-30:
      text+=text
    prevTime=time.time()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        play=False
    pygame.display.update()
  mixer.music.pause()
  loading()
  road()
def gameOver():
  global ui
  
  loading()
  ui.gameOver()
  
  startTime = time.time()
  prevTime=startTime
  colour=randColour()
  text="THANKS FOR PLAYING - PRESS ANY BUTTON TO RESTART - "
  count=0
  while True:
    if prevTime%1>time.time()%1:
      colour=randColour()
    if prevTime%0.1>time.time()%0.1:
      count+=1
    screen.fill((255,255,255))
    draw_text("MotorolaScreentype.ttf","GAME",colour,100,115,30)
    draw_text("MotorolaScreentype.ttf","OVER",colour,100,115,150)
    draw_text("mainfont.ttf",text[count:count+30],(0,0,255),20,20,285)
    if count==len(text)-30:
      text+=text
    prevTime=time.time()

    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        ui=UI()
        intro()
    pygame.display.update()
def loading():
  startTime = time.time()
  colour = randColour()#Pick a random colour
  size = (425,325)
  sprite = pygame.image.load("images/square.png")
  sprite = pygame.transform.scale(sprite,size)
  
  var = pygame.PixelArray(sprite)
  var.replace((0,0,0),colour)
  del var
  
  prevTime=startTime
  while time.time()-startTime<10:
    timeNow=time.time()-startTime
    if prevTime%2>timeNow%2:
      prevColour=colour
      while colour==prevColour:
        colour=randColour()#Pick a random colour
      size=(425,325)
      sprite=pygame.image.load("images/square.png")
      sprite=pygame.transform.scale(sprite,size)
      
      var=pygame.PixelArray(sprite)
      var.replace((0,0,0),colour)
      del var
      
    if timeNow%0.2<prevTime%0.2:
      size=(size[0]-42,size[1]-32)
      if size[0]<0 or size[1]<0:
        size=(0.1,0.1)
      #print(size)
      sprite=pygame.transform.scale(sprite,size)
      
      

      #print(size)
      #print("f")
    prevTime=timeNow
    x=425/2-size[0]/2
    y=325/2-size[1]/2                                                                                                      
    #print(x,y)
    screen.fill(prevColour)
    screen.blit(sprite,(x,y))
    pygame.display.update()

def camera(x,y,focus):
  #newX=x-focus.pos[0]+425/2
  newX=x
  newY=y-focus.pos[1]+325/2
  return (newX,newY)


def offscreen(x,y,width,height):
  if x+width<10 or 415<x or y+height<10  or 315<y:
    return True
  else:
    return False
def collide(x1,y1,width1,height1,x2,y2,width2,height2):
  if x1<=x2+width2 and x2<=x1+width1 and y1<=y2+height2 and y2<=y1+height1:
    return True
  else:
    return False

class CameraClass:
  def __init__(self):
    self.pos=[212.5,0]
  def update(self):
    if self.pos[1]!=horace.pos[1]:
      if self.pos[1]>horace.pos[1]:
        #print("h")
        self.pos[1]-=abs(horace.vel[1])
      else:
        self.pos[1]+=abs(horace.vel[1])
    else:
      self.pos[1]+=horace.vel[1]
class UI:
  def __init__(self):
    self.score=0
    self.cash=40
    self.highScore=int(open("HIGHSCORE.txt","r").read())
    self.markerTime=time.time()
    self.lastY=0
  def show(self):
    text="CASH $ "+str(self.cash)+"  SCORE       "+str(self.score)+"  HI       "+str(self.highScore)
    draw_text("mainfont.ttf",text,(0,0,0),15,11,11)
    
    #Place holder values
  def roadUpdate(self):
    if self.cash<=0:
      gameOver()
    if time.time()%(1/6)<self.markerTime%(1/6):
      if 50<=horace.pos[1]<=265:
        self.score+=5
      #self.prevTime=time.time()
  def skiUpdate(self,hillColliderBool):
    if self.cash<=0:
      gameOver()
    #print(self.lastY)
    if hillColliderBool is False:
      if self.lastY%50>horace.pos[1]%50:
        self.score+=20
    self.lastY=horace.pos[1]
  def crash(self,type):
    if type=="road":
      myGeoMockBanner=Banner("** AMBULANCE FEE  $10 **",5)#Car crash...
      myGeoMockBanner.show()
      self.cash-=10
    elif type=="treeFine":
      treeFineBanner=Banner("* LUCKY! SKIS STILL OK *",5)
      treeFineBanner.show()
    elif type=="treeHurt":
      treeHurtBanner=Banner("*BAD LUCK!  SKIS BROKEN*",5)
      treeHurtBanner.show()
      self.cash-=10
  def gameOver(self):
    if self.score>self.highScore:
      self.highScore=self.score
      file=open("HIGHSCORE.txt","w")
      file.write(str(self.score))
class Banner:
  def __init__(self,text,duration):
    self.text=text
    self.duration=duration
    self.charSize=15
    
    text=draw_text("mainfont.ttf",self.text,(255,255,255),self.charSize,1000,1000)
    self.width=text.get_width()+4
    self.height=text.get_height()+4
    self.bg=pygame.image.load("images/square.png")
    self.bg=pygame.transform.scale(self.bg,(self.width,self.height))
    
    var = pygame.PixelArray(self.bg)
    var.replace((0,0,0),(0,0,255))
    self.pos=[425//2-self.width//2,50]
    self.startTime=time.time()
    
  def show(self):
    while time.time()<self.startTime+self.duration:
      
      screen.blit(self.bg,(self.pos[0]-2,self.pos[1]-2))
      draw_text("mainfont.ttf",self.text,(255,255,255),self.charSize,self.pos[0],self.pos[1])
      pygame.display.update()
    
class Horace:
  def __init__(self):
    self.sprite=SPRITES.horaceSprites().restLeft
    self.animation=animate.Animation("images/HoraceWalkSide",(32,32))
    self.pos=[425/2,0]
    self.vel=[0,0]
    self.state="fine"
    self.got_skis=False
    self.road_side="Top"#The last road side they were on
    self.prevTime=time.time()
    self.animationGap=0.5
  def roadShow(self):
    ##if time for an update-
    if time.time()>=self.prevTime+self.animationGap:
      self.prevTime=time.time()
      if self.got_skis is False:
        if self.vel[0]==0:
          if self.vel[1]>=0:
            if self.animation.folder!="images/HoraceWalkFront":#Needed because otherwise it was reinitiallised every time
              self.animation=animate.Animation("images/HoraceWalkFront",(32,32))
          else:
            if self.animation.folder!="images/HoraceWalkBack":
              self.animation=animate.Animation("images/HoraceWalkBack",(32,32))
        elif self.vel[0]>0:
          if self.animation.folder!="images/HoraceWalkSide":
            self.animation=animate.Animation("images/HoraceWalkSide",(32,32))
        else:
          if self.animation.folder!="images/HoraceWalkSide":
            self.animation=animate.Animation("images/HoraceWalkSide",(32,32))
            for i in range(len(self.animation.sprites)):
              self.animation.sprites[i]=pygame.transform.flip(self.animation.sprites[i],True,False)
      else:
        if self.vel[0]==0:
          if self.vel[1]>=0:
            if self.animation.folder!="images/HoraceCarryingFront":#Needed because otherwise it was reinitiallised every time
              self.animation=animate.Animation("images/HoraceCarryingFront",(48,32))
          else:
            if self.animation.folder!="images/HoraceCarryingBack":
              self.animation=animate.Animation("images/HoraceCarryingBack",(48,32))
        elif self.vel[0]>0:
          if self.animation.folder!="images/HoraceCarryingRight":
            self.animation=animate.Animation("images/HoraceCarryingRight",(48,32))
        else:
          if self.animation.folder!="images/HoraceCarryingLeft":
            self.animation=animate.Animation("images/HoraceCarryingLeft",(48,32))
            #for i in range(len(self.animation.sprites)):
            #  self.animation.sprites[i]=pygame.transform.flip(self.animation.sprites[i],True,False)
      if self.vel!=[0,0]:
        self.sprite=self.animation.update()
    ##End if
    screen.blit(self.sprite,(self.pos[0],self.pos[1]))
  def roadUpdate(self):
    self.roadShow()
    
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]

    for i in cars:
      if collide(i.x,i.y,i.dims[0],i.dims[1],self.pos[0],self.pos[1],32,32):
        self.state="hit"

    if self.state=="hit":
      #effects()
      ui.crash("road")
      if self.road_side=="top":
        self.pos[1]=1
        self.state="fine"
      else:
        self.pos[1]=270
        self.state="fine"
    
    if self.pos[1]+32<=10 and self.got_skis==True:
      goal=True
    else:
      goal=False

    if self.pos[1]<10 and self.got_skis==False:
      self.pos[1]=10
    if self.pos[1]+32>315:
      self.pos[1]=315-32
    if self.pos[0]<0:
      self.pos[0]=0
    if self.pos[0]+32>415:
      self.pos[0]=415-32

    if self.pos[1]<=50:
      self.road_side="top"
    if self.pos[1]>=265:
      self.road_side="bottom"
    
    return goal
  def skiShow(self):
    if self.vel[0]==0:
      self.sprite=pygame.image.load("images/Skiing Forward.png")
      self.sprite=pygame.transform.scale(self.sprite,(32,42))
    elif self.vel[0]>0:
      self.sprite=pygame.image.load("images/Skiing Side.png")
      self.sprite=pygame.transform.scale(self.sprite,(40,40))
    elif self.vel[0]<0:
      self.sprite=pygame.image.load("images/Skiing Side.png")
      self.sprite=pygame.transform.scale(self.sprite,(40,40))
      self.sprite=pygame.transform.flip(self.sprite,True,False)
    screen.blit(self.sprite,camera(self.pos[0],self.pos[1],camObj))
  def skiUpdate(self):
    self.skiShow()

    hillColliderBool=False
    for i in obstacles:
      if collide(self.pos[0],self.pos[1],32,32,i.pos[0],i.pos[1],i.dims[0],32):
        if i.type=="Tree":
          number=random.randint(0,1)
          mixer.music.load("hitting tree sound.wav")
          mixer.music.set_volume(5)
          mixer.music.play()
          if number==0:#Skis fine
            ui.crash("treeFine")
            skiing()
          else:#Skis not fine
            ui.crash("treeHurt")
            road()
        else:
          if self.pos[1]+32<=i.pos[1]+8:
            mixer.music.load("Blip sound.mp3")
            mixer.music.set_volume(5)
            mixer.music.play()
            for num in range(300):
              self.pos[1]-=0.05
              hillColliderBool=True
              screen.fill((255,255,255))
              
              for j in obstacles:
                screen.blit(j.sprite,camera(j.pos[0],j.pos[1],camObj))
              screen.blit(self.sprite,camera(self.pos[0],self.pos[1],camObj))
              pygame.display.update()
            mixer.music.stop()
          else:
            if self.pos[0]>i.pos[0]:
              self.pos[0]=i.pos[0]+i.dims[0]
            else:
              self.pos[0]=i.pos[0]-32
      #else:
        #if i.type=="Hill":
          #if #collide(self.pos[0],self.pos[1],32,32,i.pos[0],i.pos[1]-30,i.dims[0],i.dims[1]):#Collider in front of the hill
            #self.vel[1]=0.02
          #else:
          #self.vel[1]=0.1
          #camObj.pos[1]-=30
    
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]

    return hillColliderBool
class Vehicle:
  def __init__(self):
    lane=random.randint(0,5)
    self.type=random.randint(0,3)#0 for car, 1 for motorbike, 2 for lorry, 3 for Ambulance

    if self.type==0:
      self.dims=[64,32]
    if self.type==1:
      self.dims=[32,32]
    if self.type==2:
      self.dims=[84,32]
    if self.type==3:
      self.dims=[80,32]
    if lane<3:
      x=10-self.dims[0]
      y=50+lane*36
      self.vel=1
      for i in cars:
        while collide(x,y,self.dims[0],self.dims[1],i.x,i.y,i.dims[0],i.dims[1]):
          lane=random.randint(0,5)
          y=50+lane*36
          if lane<3:
            x=10-self.dims[0]
            self.vel=1
          else:
            x=325+self.dims[0]
            self.vel=-1
      self.x=x
      self.y=y
      self.lane=lane
    else:
      x=325+self.dims[0]
      y=50+lane*36
      self.vel=-1
      for i in cars:
        while collide(x,y,self.dims[0],self.dims[1],i.x,i.y,i.dims[0],i.dims[1]):
          #print(lane)
          lane=random.randint(0,5)
          y=50+lane*36
          if lane<3:
            x=10-self.dims[0]
            self.vel=1
          else:
            x=325+self.dims[0]
            self.vel=-1
      self.x=x
      self.y=y
      self.lane=lane
    
    if self.type==1:
      self.vel*=1.5
    if self.type==2:
      self.vel*=0.75
      
    self.sprite=SPRITES.vehicles(self.type,self.lane).sprite
    
  def update(self):
    self.y=50+self.lane*36
    #if cameraBool is False:
    if not offscreen(self.x,self.y,self.dims[0],self.dims[1]):
      screen.blit(self.sprite,(self.x,self.y))
    #else:
    #  screen.blit(self.sprite,camera(self.x,self.y,horace))
    self.x+=self.vel

    if offscreen(self.x,self.y,self.dims[0],self.dims[1]):
      self.__init__()   

    for i in cars:
      if i!=self:
        if collide(self.x,self.y,self.dims[0],self.dims[1],i.x,i.y,i.dims[0],i.dims[1]):
          if self.vel>0:
            if self.x<=i.x:
              if self.lane!=2:
                
                laneFree=True
                for j in cars:
                  if collide(self.x,self.y+36,self.dims[0],self.dims[1],j.x,j.y,j.dims[0],j.dims[1]):
                    laneFree=False
                    
                if laneFree is True:
                  self.lane+=1
                else:
                  if i.vel<self.vel:
                    self.vel=i.vel
                  self.x=i.x-self.dims[0]-1
              else:

                laneFree=True
                for j in cars:
                  if collide(self.x,self.y-36,self.dims[0],self.dims[1],j.x,j.y,j.dims[0],j.dims[1]):
                    laneFree=False
                    
                if laneFree is True:
                  self.lane-=1
                else:
                  if i.vel<self.vel:
                    self.vel=i.vel
                  self.x=i.x-self.dims[0]-1

                
                

          else:
            if self.x>=i.x:
              if self.lane!=3:
                
                laneFree=True
                for j in cars:
                  if collide(self.x,self.y-36,self.dims[0],self.dims[1],j.x,j.y,j.dims[0],j.dims[1]):
                    laneFree=False
                    
                if laneFree is True:
                  self.lane-=1
                else:
                  if i.vel<self.vel:
                    self.vel=i.vel
                  self.x=i.x+i.dims[0]+1
              else:
                laneFree=True
                for j in cars:
                  if collide(self.x,self.y+36,self.dims[0],self.dims[1],j.x,j.y,j.dims[0],j.dims[1]):
                    laneFree=False
                    
                if laneFree is True:
                  self.lane+=1
                else:
                  if i.vel<self.vel:
                    self.vel=i.vel
                  self.x=i.x+i.dims[0]+1
class Hut:
  def __init__(self):
    self.pos=[425//2-80/2,315-44]
    self.sprite=SPRITES.Hut().sprite
    #self.door=SPRITES.Hut().door
    self.doorOffSet=[10,21]
    self.doorDims=[18,24]
  def update(self):
    if collide(horace.pos[0],horace.pos[1],32,32,self.pos[0]+10,self.pos[1]+21,18,24):
      if horace.got_skis==False:
        horace.got_skis=True
        mixer.music.load("Blip sound.mp3")
        mixer.music.set_volume(5)
        mixer.music.play()
    #else:
    #  goal=False
    screen.blit(self.sprite,(self.pos[0],self.pos[1]))
    #screen.blit(self.door,(self.pos[0]+10,self.pos[1]+21))
    return goal
class Tree:
  def __init__(self):
    self.dims=[40,44]
    self.pos=None
    while self.pos==None:
      pos=[random.randint(25,400),random.randint(200,2000)]
      collideBool=False
      for i in obstacles:
        if collide(pos[0],pos[1],self.dims[0],self.dims[1],i.pos[0],i.pos[1],i.dims[0],i.dims[1]):
          collideBool=True
      if collideBool==False:
        self.pos=pos
    self.sprite=SPRITES.Tree().sprite
    self.type="Tree"
  def update(self):
    if cameraBool==False:
      screen.blit(self.sprite,(self.pos[0],self.pos[1]))
    else:
      screen.blit(self.sprite,camera(self.pos[0],self.pos[1],camObj))
class Hill:
  def __init__(self):
    self.dims=[40,10]
    self.pos=None
    while self.pos==None:
      pos=[random.randint(25,400),random.randint(200,2000)]
      collideBool=False
      for i in obstacles:
        if collide(pos[0],pos[1],self.dims[0],self.dims[1],i.pos[0],i.pos[1],i.dims[0],i.dims[1]):
          collideBool=True
      if collideBool==False:
        self.pos=pos
    self.sprite=SPRITES.Hill().sprite
    self.type="Hill"
    
  def update(self):
    if cameraBool==False:
      screen.blit(self.sprite,(self.pos[0],self.pos[1]))
    else:
      screen.blit(self.sprite,camera(self.pos[0],self.pos[1],camObj))
class Flags:
  def __init__(self):
    if len(flags)==0:#If this is the first flag
      self.pos=[random.randint(25,300),random.randint(200,800)]
    else:
      newStreak=random.randint(0,5)#random number to decide whether of not to break up the streak
      if newStreak==0:#If it is a new streak 
        if flags[-1].pos[1]<700:
          self.pos=[random.randint(25,400),random.randint(flags[-1].pos[1]+100,800)]
        else:
          self.pos=[flags[-1].pos[0],flags[-1].pos[1]+50]
      else:
        y=flags[-1].pos[1]+50
        distanceChoice=random.randint(0,2)
        if distanceChoice==0:
          x=flags[-1].pos[0]
          self.pos=[x,y]
        elif distanceChoice==1:
          x=flags[-1].pos[0]+20
          self.pos=[x,y]
        else:
          x=flags[-1].pos[0]-20
          self.pos=[x,y]
    self.gap=100
    self.leftSprite=SPRITES.Flags().leftSprite
    self.rightSprite=SPRITES.Flags().rightSprite
    self.activated=False
  def update(self):
    if cameraBool is True:
      screen.blit(self.leftSprite,camera(self.pos[0],self.pos[1],camObj))
      screen.blit(self.rightSprite,camera(self.pos[0]+self.gap,self.pos[1],camObj))
    else:
      screen.blit(self.leftSprite,(self.pos[0],self.pos[1]))
      screen.blit(self.rightSprite,(self.pos[0]+self.gap,self.pos[1]))

    if self.activated==False:
      if horace.pos[1]>=self.pos[1]:
        self.activated=True
        if self.pos[0]<=horace.pos[0]<=self.pos[0]+self.gap:
          pass
        else:
          mixer.music.load("missing flag.wav")
          mixer.music.set_volume(5)
          mixer.music.play()
          ui.score-=400
          time.sleep(1)
          mixer.music.stop()
class FinishLine:
  def __init__(self):
    self.pos=[100,2000]
    self.width=128
    self.sprite=SPRITES.Finish().sprite
  def update(self):
    mixer.music.load("Blip sound.mp3")
    mixer.music.set_volume(10)
    mixer.music.play()

    screen.blit(self.sprite, camera(self.pos[0],self.pos[1],camObj))

    if horace.pos[1]>=self.pos[1]:
      if self.pos[0]<=horace.pos[0]<=self.pos[0]+self.width:#Condition checking horace is under the banner
        ui.score+=100
        bonusPoints=Banner("**  BONUS 100 POINTS  **",5)
        bonusPoints.show()
      loading()
      road()
cameraBool=False

ui=UI()

def road():
  global horace
  global cars
  global goal

  cameraBool=False
  
  hut=Hut()
  horace=Horace()
  horace.sprite=SPRITES.horaceSprites().restLeft
  cars=[]
  
  for i in range(6):
    cars.append(Vehicle())
  goal=False
  while goal is False:
    
    screen.fill((255,255,255))
    #screen.blit(SPRITES.background,(10,10))
    screen.blit(SPRITES.road,(10,50))
    
    hut.update()
    goal=horace.roadUpdate()
    for i in cars:
      i.update()

    ui.roadUpdate()
    ui.show()
    
    screen.blit(SPRITES.outline,(0,0))
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key==pygame.K_UP:
          horace.vel[1]=-1
        if event.key==pygame.K_DOWN:
          horace.vel[1]=1
        if event.key==pygame.K_LEFT:
          horace.vel[0]=-1
        if event.key==pygame.K_RIGHT:
          horace.vel[0]=1
      if event.type == pygame.KEYUP:
        if event.key==pygame.K_UP:
          horace.vel[1]=0
        if event.key==pygame.K_DOWN:
          horace.vel[1]=0
        if event.key==pygame.K_LEFT:
          horace.vel[0]=0
        if event.key==pygame.K_RIGHT:
          horace.vel[0]=0
    pygame.display.update()
  loading()
  skiing()
def skiing():
  global horace
  global obstacles
  global flags
  global cameraBool
  global camObj

  cameraBool=True
  camObj=CameraClass()
  
  horace=Horace()
  camObj.pos[1]=horace.pos[1]
  horace.sprite=SPRITES.horaceSprites().skiLeft
  horace.vel=[0,0.5]
  obstacles=[]
  flags=[]
  for i in range(6):
    flags.append(Flags())
  finish=FinishLine()
  for i in range(6):
    number=random.randint(0,1)#Adjust to change the likelyhood of each
    if number==0:#^^^
      obstacles.append(Tree())
    else:
      obstacles.append(Hill())

  goal=False

  while goal is False:
    #print(horace.pos[1])
    screen.fill((255,255,255))
    hillColiderBool=horace.skiUpdate()
    camObj.update()
    for i in obstacles:
      i.update()

    for i in flags:
      i.update()
    finish.update()

    ui.skiUpdate(hillColiderBool)
    ui.show()
    
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_LEFT:
          horace.vel[0]=-0.3
        if event.key==pygame.K_RIGHT:
          horace.vel[0]=0.3
          
      if event.type==pygame.KEYUP:
        if event.key==pygame.K_LEFT:
          horace.vel[0]=0
        if event.key==pygame.K_RIGHT:
          horace.vel[0]=0
    pygame.display.update()
#loading()
#road()
#skiing()
intro()
#gameOver()
    
'''
test=Banner("TEST THIS IS TEST TEXT",10)
count=0
while True:
  screen.fill((255,255,255))
  if count==0:
    test.show()
  count+=1
  pygame.display.update()
'''

'''
walk=animate.Animation("images/HoraceWalkSide")
count=0
while True:
  screen.fill((255,255,255))
  if count%100==0:
    sprite=walk.update()

  screen.blit(sprite,(10,10))
  
  count+=1
  pygame.display.update()
'''
