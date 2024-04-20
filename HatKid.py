from Movement import *
import pygame
import random
from constants import *
from GameSprite import *

class Hitbox(GameSprite):
    colour =(255,255,255,100)
    def __init__(self,x,y,screen=None):
        super().__init__(x,y,None,screen)
        #pygame.draw.rect(screen,(100,100,100),(x,y))
    def draw(self):
        pygame.draw.rect(self.screen, Hitbox.colour,self.rect)

class HatKid(GameSprite):
    def __init__(self,x,y,screen,map):
        hatkid_filename = "sprite/HatKid/walk/walk1.png"
        size = (TILE_SIZE,TILE_SIZE)
        super().__init__(x,y,hatkid_filename,screen,size)
        self.hitbox=Hitbox(x,y,screen)
        self.walks=[]
        self.walk=Walk(map,self)
        self.jump=Jump(map,self)
        self.dive=Dive(map,self)
        self.walkright=self.walk.sprites_right
        self.walkleft=self.walk.sprites_left
        self.idleright=self.load_idle("sprite/HatKid/idle",Movement.Direction.RIGHT)
        self.idleleft=self.load_idle("sprite/HatKid/idle",Movement.Direction.LEFT)
        self.diveright=self.dive.diveright
        self.diveleft=self.dive.diveleft
        self.climbright=self.load_climb("sprite/HatKid/climb",Movement.Direction.RIGHT)
        self.climbleft=self.load_climb("sprite/HatKid/climb",Movement.Direction.LEFT)

        self.direction=Movement.Direction.RIGHT
        self.x_speed = 0
        self.current_frame = self.idleright[0]
        self.walk_index= 0
        self.is_on_ground= True
        self.has_jumped_in_air= False
        self.y_speed=0
        self.canjump= True

    def load_idle(self,spritedir,direction):
        idles=[]
        for counter in range (1,4):
            idle= pygame.image.load(spritedir+"/idle"+str(counter)+".png")
            idle=pygame.transform.scale(idle,HATKIDSIZEIDLE)
            if direction==Movement.Direction.LEFT:
                idle=pygame.transform.flip(idle,True,False)
            idles.append(idle)
        return tuple(idles)
    
    # def load_dive(self,spritedir,direction):
    #     dives=[]
    #     for counter in range (1,3):
    #         dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
    #         dive=pygame.transform.scale(dive,HATKIDSIZEDIVE)
    #         if direction==Movement.Direction.LEFT:
    #             dive=pygame.transform.flip(dive,True,False)
    #         dives.append(dive)
    #     return tuple(dives)
    
    def load_climb(self,spritedir,direction):
        climbs=[]
        for counter in range (1,2):
            climb= pygame.image.load(spritedir+"/climb"+str(counter)+".png")
            climb=pygame.transform.scale(climb,HATKIDSIZECLIMB)
            if direction==Movement.Direction.LEFT:
                climb=pygame.transform.flip(climb,True,False)
            climbs.append(climb)
        return tuple(climbs)    


    #def dive(self):
        # if self.has_dived==False:
        #     if self.is_on_ground:
        #         if pygame.key.get_pressed()[pygame.K_d]:
        #             print("right ground dive")
        #             self.x_speed=MAXXSPEED+3
        #             #self.rect.y-=10
        #             self.has_dived=True
        #         if pygame.key.get_pressed()[pygame.K_a]:
        #             print("left ground dive")
        #             self.x_speed=-(MAXXSPEED+3)
        #             #self.rect.y-=10
        #             self.has_dived=True
        #     else:
        #         if self.direction== Movement.Direction.RIGHT:
        #             print("right air dive")
        #             self.x_speed=MAXXSPEED+3
        #             self.has_dived=True
        #         if self.direction== Movement.Direction.LEFT:
        #             print("left air dive")
        #             self.x_speed=-(MAXXSPEED+3)
        #             self.has_dived=True
    #def dive_cancel(self):
        #TODO:only reset has dived once dive canceled, cool down, change effects

        # if self.has_dived:
        #     self.rect.y-=5
        #     self.has_jumped_in_air=True
        #     self.y_speed=MAXXSPEED
        #     print("dive cancel")

    def check5pixel(self,map):
        """checks for doublejump"""
        self.rect.move_ip([0,-MAXYSPEED])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([0,MAXYSPEED])
        return hitlist

    def update(self,map1):
        #update hitbox pos
        self.hitbox.rect.center=self.rect.center

        #gravity
        if self.y_speed <= MAXYSPEED:
            self.y_speed +=0.2

        #checks if theres a tile
        if self.tilesabove(map1):
            #print ("cant double jump")
            self.canjump=False

        #if on ground does this
        if tilesunder:= self.tilesunder(map1):
            #print("tile under")
            self.jumpdirection=False
            self.jump.count=0
            self.is_on_ground= True
            self.has_jumped_in_air= False
            self.has_dived=False
            if self.y_speed >= 0:
                #print("not space")
                self.y_speed=0
                self.hitbox.rect.bottom=tilesunder[0].rect.top
                self.rect.bottom=tilesunder[0].rect.top
        else:
            self.is_on_ground= False

        if (tilesabove:= self.tilesabove(map1)) and self.y_speed <= 0:
            self.y_speed=0
            self.hitbox.rect.top=tilesabove[0].rect.bottom
            self.rect.top=tilesabove[0].rect.bottom
            self.canjump=False

        # and pygame.key.get_pressed()[pygame.K_a]
        if (tilesleft:= self.tilesleft(map1)) and self.x_speed <= 0:
            self.x_speed=0
            self.hitbox.rect.left=tilesleft[0].rect.right

            
        if (tilesright:= self.tilesright(map1)) and self.x_speed >= 0:
            self.x_speed=0
            self.hitbox.rect.right=tilesright[0].rect.left
        #walking sprite
        
        #set up display frame
        

    


        keyspressedlist=pygame.key.get_pressed()
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_LCTRL]:
            self.dive.cancel()
            print ("space or left control")
        if keyspressedlist[pygame.K_LCTRL] and keyspressedlist[pygame.K_a]:
            self.dive.start()
            #print("L dived")


        elif keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
            self.walk.stop()
        elif keyspressedlist[pygame.K_d]:
            if self.direction == Movement.Direction.LEFT:
                self.walk.stop()
            elif self.x_speed <-0.1:
                self.walk.stop()
            elif self.jump.count == 2 and self.jumpdirection == False:
                self.jumpdirection=True
            self.walk.set_direction(Movement.Direction.RIGHT)
            self.walk.start()
        elif keyspressedlist[pygame.K_a]:
            if self.direction == Movement.Direction.RIGHT:
                self.walk.stop()
            elif self.x_speed >0.1:
                self.walk.stop()  
            elif self.jump.count == 2 and self.jumpdirection == False:
                self.jumpdirection=True
            self.walk.set_direction(Movement.Direction.LEFT)
            self.walk.start()
        else:
            self.walk.stop()

        if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
            self.dive.cancel()
            print ("w or space")
            if self.jump.count <2 and self.canjump:
                self.jump.start()
            
        else:
            self.canjump=True
        
        
        if(self.ispastleft()):
            if 0>=self.x_speed:
                self.x_speed=0
                #self.hitbox.left=0

        if(self.ispastright()):
            if 0<=self.x_speed:
                self.x_speed=0
                #self.hitbox.rect.right=SCREEN_WIDTH
                #print(self.hitbox.right,self.hitbox.x)
        if(self.ispastbottom()):
            self.rect.x,self.rect.y=100,100

#check 1,2,3,4,5 but with y_speed and makes it not over shoot
            

        self.rect.x+=self.x_speed
        self.rect.y+=self.y_speed

        self.hitbox.rect.x+=self.x_speed
        self.hitbox.rect.y+=self.y_speed

    def tilesunder(self,map):
        """return a list of tiles below the kid"""
        checkahead=MAXYSPEED
        self.hitbox.rect.move_ip([0,checkahead])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        self.hitbox.rect.move_ip([0,-checkahead])
        return hitlist
    def tilesabove(self,map):
        """return a list of tiles above the kid"""
        #self.rect.move_ip([0,-(self.y_speed+1)])
        self.hitbox.rect.move_ip([0,-1])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        #self.rect.move_ip([0,self.y_speed+1])
        self.hitbox.rect.move_ip([0,1])
        return hitlist    
    def tilesleft(self,map):
        """return a list of tiles above the kid"""
        self.hitbox.rect.move_ip([-MAXXSPEED,0])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        self.hitbox.rect.move_ip([MAXXSPEED,0])
        return hitlist 
    def tilesright(self,map):
        self.hitbox.rect.move_ip([3,0])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        self.hitbox.rect.move_ip([-3,0])
        return hitlist   
    
    def ispastleft(self):
        checkahead=MAXXSPEED
        self.rect.move_ip([0,-checkahead])
        #check=self.rect.x <= 0
        check=self.hitbox.rect.left <= 0
        self.rect.move_ip([0,checkahead])
        return check

    def ispastright(self):
        self.rect.move_ip([0,self.x_speed])
        #check=self.rect.x+TILE_SIZE >= WIDTHINTILES*TILE_SIZE
        check=self.hitbox.rect.right >= WIDTHINTILES*TILE_SIZE
        self.rect.move_ip([0,-self.x_speed])
        return check


    def ispastbottom(self):
        """true or false if touching barrier on bottom"""
        return self.rect.y+TILE_SIZE >= HEIGHTINTILES*TILE_SIZE

    def draw(self):
        self.hitbox.draw()
        #pygame.draw.rect(self.screen, Hitbox.colour,self.rect).
        #self.hitbox=pygame.draw.rect(self.screen,(255,255,255,100),(self.rect.center[0]-self.hitbox.width/2,self.rect.bottomright[1]-self.hitbox.height,self.hitbox.width,self.hitbox.height))
        self.screen.blit(self.current_frame,self.rect)

