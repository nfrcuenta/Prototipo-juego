import pygame
import math
import constants
import random

class character():
    def __init__(self,x,y,image,bullet,imgenemigo,lives):
        #variables enemigos
        self.imgenemigo=imgenemigo
        self.game=True
        self.cooldownenemies=pygame.time.get_ticks()

        #variables disparo bala
        self.shoy=True
        self.timeshot=pygame.time.get_ticks()
        self.imgbullet=bullet

        #variables para animacion
        self.animaciones=image
        self.frame_index=0
        self.update_time=pygame.time.get_ticks()
        self.animacion=self.animaciones[self.frame_index]
        self.angulo=0
        self.x=x
        self.y=y
        self.shape=self.animacion.get_rect()
        self.shape.center=(x,y)
        self.shapehit=self.shape
        self.vidas=lives
        self.expansion=False
        self.radius=self.animacion.get_width()
    
    def update(self,listaenemigos):
        bala=None
        cooldown_animaciones=250
        self.animacion=self.animaciones[self.frame_index]
        if pygame.time.get_ticks()-self.update_time>=cooldown_animaciones:
            self.frame_index+=1
            self.update_time=pygame.time.get_ticks()
        if self.frame_index>=len(self.animaciones):
            self.frame_index=0

        mouse_pose=pygame.mouse.get_pos()
        difx=mouse_pose[0]-self.shape.centerx
        dify=-(mouse_pose[1]-self.shape.centery)
        self.angulo=math.degrees(math.atan2(dify,difx))
        self.animacion=pygame.transform.rotate(self.animacion,self.angulo)
        self.shape=self.animacion.get_rect()
        self.shape.center=(self.x,self.y)
        #detectar si mouse esta siendo presionado
        if pygame.mouse.get_pressed()[0]:
            if self.shoy==True:
                bala=plasma_armos(self.imgbullet,self.shape.centerx,self.shape.centery,self.angulo,constants.damage)
                self.shoy=False
                self.timeshot=pygame.time.get_ticks()
            if pygame.time.get_ticks()-self.timeshot>constants.frecbalas:
                self.shoy=True

        #control de impactos

        for enemy in listaenemigos:
            if enemy.recto.colliderect(self.shape):
                self.vidas-=1
                enemy.kill()
                self.expansion=True
                self.radius=self.animacion.get_width()/2


        return bala

        
        
    
    def eneemies(self):
        enemigo=None
        if self.game==True:
            coord=random.choice(constants.cord)
            self.cordx=random.choice(coord[0])
            self.cordy=random.choice(coord[1])
            enemigo=enemies(self.shape,self.cordx,self.cordy,self.imgenemigo,constants.salud)
            self.game=False
            self.cooldownenemies=pygame.time.get_ticks()
        if pygame.time.get_ticks()-self.cooldownenemies>constants.demorareaparicion:
            self.game=True
        return enemigo

    def dibujo(self,interfaz):
        a=None
        interfaz.blit(self.animacion,self.shape)
        #pygame.draw.rect(interfaz,(0,255,255),self.shape,1)
        pygame.draw.rect(interfaz,(255,0,0),self.shapehit,1)
        if self.expansion==True:
            pygame.draw.circle(interfaz,(57,255,20),(self.shape.centerx,self.shape.centery),self.radius,15)
            pygame.draw.circle(interfaz,(57,255,20),(self.shape.centerx,self.shape.centery),self.radius+45,30)
            self.radius+=constants.velocidad_expansion
            a=True
            if self.radius>constants.ancho/2:
                self.expansion=False
        return a

    def destruccion(self):
         return self.radius

class plasma_armos(pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle,damage):
        pygame.sprite.Sprite.__init__(self)
        self.img_org=image
        self.dano=damage
        self.angle=angle
        self.img=pygame.transform.rotate(self.img_org,self.angle)
        self.rect=self.img.get_rect()
        self.rect.center=(x-(self.img_org.get_width()/2),y-(self.img_org.get_height()/2))
        self.deltax=math.cos(math.radians(self.angle))*constants.velocidadbala
        self.deltay=-math.sin(math.radians(self.angle))*constants.velocidadbala

    def update(self,listaenemigos):
        self.rect.x+=self.deltax
        self.rect.y+=self.deltay
        #determinar inexsistencia
        if self.rect.right<0 or self.rect.left>constants.ancho or self.rect.bottom<0 or self.rect.top>constants.alto:
            self.kill()

        for enemigo in listaenemigos:
            if enemigo.recto.colliderect(self.rect):
                damage=self.dano
                enemigo.vida-=damage
                self.kill()
                break


    def dibujo(self,interfaz):
        interfaz.blit(self.img,(self.rect.centerx,self.rect.centery))

class enemies(pygame.sprite.Sprite):
    def __init__(self,jugador,enemix,enemiy,image,health):
        pygame.sprite.Sprite.__init__(self)
        self.image_org=image
        self.angulo=0
        self.jugador=jugador
        self.recto=self.image_org.get_rect()
        self.recto.center=(enemix,enemiy)
        self.deltax=self.jugador.centerx-self.recto.centerx
        self.deltay=self.jugador.centery-self.recto.centery
        self.image=pygame.transform.rotate(self.image_org,self.angulo)
        self.vida=health
    
    def update(self):

        if self.recto.right<0 or self.recto.left>constants.ancho or self.recto.bottom<0 or self.recto.top>constants.alto or self.vida<=0:
            self.kill()
        #self.image=pygame.transform.rotate(self.image,self.angulo)
        movix=0
        moviy=0
        if self.deltax>0:
            movix=self.deltax/constants.demorameteoro
        elif self.deltax<0:
            movix=(self.deltax/constants.demorameteoro)
        if self.deltay>0:
            moviy=self.deltay/constants.demorameteoro
        elif self.deltay<0:
            moviy=(self.deltay/constants.demorameteoro)
        self.movimiento(movix,moviy)
        
    def movimiento(self,deltax,deltay):
        self.recto.centerx+=deltax
        self.recto.centery+=deltay
    
    def destruccion(self,radio):
        if abs(self.deltax)<=radio and abs(self.deltay)<=radio:
            self.kill()


    
    def dinujo(self,interfaz):
        interfaz.blit(self.image,self.recto)
        pygame.draw.circle(interfaz,(255,0,255),(self.recto.centerx,self.recto.centery),self.image_org.get_width()/2,1)
