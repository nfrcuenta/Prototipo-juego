import pygame
import math
import constants


class Bullet(pygame.sprite.Sprite):
    """
    Clase Bullet, en la que se establecen los atributos y métodos de las proyectiles que dispara el Player.
    """
    def __init__(self, image, x, y, angle, damage):
        pygame.sprite.Sprite.__init__(self)
        self.img_org = image
        self.damage = damage
        self.angle = angle
        self.img = pygame.transform.rotate(self.img_org, self.angle)
        self.rect = self.img.get_rect()
        self.rect.center = (x-(self.img_org.get_width()/2), y-(self.img_org.get_height()/2))
        self.deltax = math.cos(math.radians(self.angle))*constants.VEL_BULLET
        self.deltay = -math.sin(math.radians(self.angle))*constants.VEL_BULLET

    def update(self, group_enemies):
        self.rect.x += self.deltax
        self.rect.y += self.deltay

        #Determinar límites de las Bullets.
        if self.rect.right < 0 or self.rect.left > constants.WIDTH or self.rect.bottom < 0 or self.rect.top > constants.HEIGHT:
            self.kill()

        #Comprobador de impactos de las Bullets.
        for enemigo in group_enemies:
            if enemigo.rect.colliderect(self.rect):
                damage = self.damage
                enemigo.health -= damage
                self.kill()
                break

    def drawing(self, interfaz):
        interfaz.blit(self.img, (self.rect.centerx, self.rect.centery))
