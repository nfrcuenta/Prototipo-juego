import pygame
import constants
import random
import time


class Enemy(pygame.sprite.Sprite):
    """
    Clase Enemy, es la encargada de crear a los enemigos que debe eliminar el Player.
    """
    def __init__(self, player, enemix, enemiy, images, health, scoreboard):
        pygame.sprite.Sprite.__init__(self)
        self.scoreboard = scoreboard
        self.angle = random.randint(0, 360)
        self.images = list(map(self.rotation, images))
        self.image = images[0]
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.center = (enemix, enemiy)
        self.delta_x = self.player.centerx - self.rect.centerx
        self.delta_y = self.player.centery - self.rect.centery
        self.health = health
        self.creation_time = time.time()

    def rotation(self, image):
        image = pygame.transform.rotate(image, self.angle)
        return image

    def update(self):
        #Configuracion de las texturas del Asteroide.
        if self.rect.right < 0 or self.rect.left > constants.WIDTH or self.rect.bottom < 0 or self.rect.top > constants.HEIGHT:
            self.kill()
        if self.health == 100:
            self.image = self.images[0]
        if self.health == 80:
            self.image = self.images[1]
        if self.health == 60:
            self.image = self.images[2]
        if self.health == 40:
            self.image = self.images[3]
        if self.health == 20:
            self.image = self.images[4]
        if self.health <= 0:
            self.scoreboard.update_score(int(10-(time.time()-self.creation_time)))
            self.kill()

        #Configuración del movimiento del Asteroide.
        move_x = 0
        move_y = 0
        if self.delta_x > 0:
            move_x = self.delta_x / constants.DELAY_ASTEROID
        elif self.delta_x < 0:
            move_x = (self.delta_x / constants.DELAY_ASTEROID)
        if self.delta_y > 0:
            move_y = self.delta_y / constants.DELAY_ASTEROID
        elif self.delta_y < 0:
            move_y = (self.delta_y / constants.DELAY_ASTEROID)
        self.moving(move_x, move_y)

    def moving(self, delta_x, delta_y):
        self.rect.centerx += delta_x
        self.rect.centery += delta_y

    def destroy(self, radius):
        if abs(self.delta_x) <= radius and abs(self.delta_y) <= radius:
            self.kill()

    def drawing(self, interfaz):
        interfaz.blit(self.image, self.rect)
