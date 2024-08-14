import pygame
import math
import constants
import random
import bullet
import enemy


class Player:
    """
    Clase Player es la encargada de dar los atributos y metodos que se utilizan para dar funcionalidad al personaje
    principal.
    """
    def __init__(self, x, y, animations, imgbullet, imgenemigo,imgenemigo2, lifes, scoreboard, shot_sound, explosion_sound,skin):
        #Referencia a la Scoreboard.
        self.scoreboard = scoreboard

        #Atributos enemigos
        self.imgenemigo = imgenemigo
        self.imgenemigo2=imgenemigo2
        self.game = True
        self.cooldownenemies = pygame.time.get_ticks()

        #Atributos de los disparos
        self.shot = True
        self.timeshot = pygame.time.get_ticks()
        self.imgbullet = imgbullet
        self.shot_sound = shot_sound

        #Atributos de animación
        self.animations = animations
        self.nave = skin
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation = self.animations[self.nave][self.frame_index]
        self.angle = 0
        self.x = x
        self.y = y
        self.shape = self.animation.get_rect()
        self.shape.center = (x, y)
        self.shapehit = self.shape
        self.lifes = lifes
        self.expansion = False
        self.explosion_sound = explosion_sound
        self.radius = self.animation.get_width()
    
    def cambio(self, number):
        self.nave=number
    
    def update(self, listaenemigos):
        #Creamos una variable para retornar algo si se ejecuta la acción de disparo o nada en caso contrario
        bullets = None

        #Configuración de las animaciones del Player
        cooldown_animaciones = 250
        self.animation = self.animations[self.nave][self.frame_index]
        if pygame.time.get_ticks()-self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations[self.nave]):
            self.frame_index = 0

        #Configuración de la rotación del Player.
        mouse_pose = pygame.mouse.get_pos()
        dif_x = mouse_pose[0]-self.shape.centerx
        dif_y = -(mouse_pose[1]-self.shape.centery)
        self.angle = math.degrees(math.atan2(dif_y, dif_x))
        self.animation = pygame.transform.rotate(self.animation, self.angle)
        self.shape = self.animation.get_rect()
        self.shape.center = (self.x, self.y)

        #Ejecución de los disparos.
        if pygame.mouse.get_pressed()[0] and not self.expansion:
            if self.shot:
                bullets = bullet.Bullet(self.imgbullet, self.shape.centerx, self.shape.centery, self.angle, constants.BASE_DAMAGE)
                self.shot_sound.play()
                self.shot = False
                self.timeshot = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - self.timeshot) > constants.FREQ_BULLETS:
                self.shot = True

        #Control de impactos
        for one_enemy in listaenemigos:
            if one_enemy.rect.colliderect(self.shape):
                self.lifes -= 1
                one_enemy.kill()
                self.scoreboard.update_score(-25)
                self.expansion = True
                self.radius = self.animation.get_width() / 2
        return bullets

    def enemies(self):
        one_enemy = None
        if self.game:
            x=random.randint(1,100)
            coord = random.choice(constants.COORD)
            cordx = random.choice(coord[0])
            cordy = random.choice(coord[1])
            if x>90:
                one_enemy = enemy.Enemy(self.shape, cordx, cordy, self.imgenemigo2, constants.HEALTH*2, self.scoreboard)
            else:
                one_enemy = enemy.Enemy(self.shape, cordx, cordy, self.imgenemigo, constants.HEALTH, self.scoreboard)
            self.game = False
            self.cooldownenemies = pygame.time.get_ticks()
        if pygame.time.get_ticks()-self.cooldownenemies > constants.DELAY_SPAWN:
            self.game = True
        return one_enemy

    def drawing(self, interfaz):
        a = None
        interfaz.blit(self.animation, self.shape)
        if self.expansion:
            self.explosion_sound.play()
            pygame.draw.circle(interfaz, (57, 255, 20), (self.shape.centerx, self.shape.centery), self.radius, 15)
            pygame.draw.circle(interfaz, (57, 255, 20), (self.shape.centerx, self.shape.centery), self.radius+45, 30)
            self.radius += constants.VEL_EXP
            a = True
            if self.radius > constants.WIDTH/2:
                self.expansion = False
        return a

    def destroy(self): return self.radius
