import pygame
import constants
import character
pygame.init()
#Creacion interfaz
ventana=pygame.display.set_mode((constants.ancho,constants.alto))
pygame.display.set_caption("Space survivor")
imgbackground=pygame.image.load("background/spacex.jpg").convert_alpha()
x=0
imgbackground=pygame.transform.scale(imgbackground,(imgbackground.get_width()*(constants.ancho/imgbackground.get_width())*3,imgbackground.get_height()*(constants.alto/imgbackground.get_height())))


#cargar img bala
imgbullet=pygame.image.load("armor/plasma_ball.png").convert_alpha()
imgbullet=pygame.transform.scale(imgbullet,(imgbullet.get_width()*constants.escalabala,imgbullet.get_height()*constants.escalabala))

#Cargar img meteoros
meteoror=[]
meteors=pygame.image.load("meteoro/meteoroo.png")
meteors=pygame.transform.scale(meteors,(meteors.get_width()*constants.escalameteoro,meteors.get_height()*constants.escalameteoro))

#Personaje
animaciones=[]
for i in range(9):
    img_character=pygame.image.load(f"nave/nave_{i+1}.png").convert_alpha()
    img_character=pygame.transform.scale(img_character,(img_character.get_width()*constants.escla,img_character.get_height()*constants.escla))
    animaciones.append(img_character)
personaje=character.character(ventana.get_width()/2,ventana.get_height()/2,animaciones,imgbullet,meteors,constants.vidas)

#vida imgs
vidas_3=pygame.image.load("vidas/vidas_3.png").convert_alpha()
vidas_2=pygame.image.load("vidas/vidas_2.png").convert_alpha()
vidas_1=pygame.image.load("vidas/vidas_1.png").convert_alpha()

#crear grupo de sprites
grupo_balas=pygame.sprite.Group()
grupo_enemigos=pygame.sprite.Group()

#Limitando velocidad
clock=pygame.time.Clock()
#ciclo ejecucion
execute=True
while execute:

    #velocidad regulada
    clock.tick(constants.maxfps)
    x_rel=x%imgbackground.get_rect().width
    ventana.blit(imgbackground,(x_rel-imgbackground.get_rect().width,0))
    if x_rel<constants.ancho:
        ventana.blit(imgbackground,(x_rel,0))
    x-=1



    

    bala=personaje.update(grupo_enemigos)
    if bala:
        grupo_balas.add(bala)

    for bala in grupo_balas:
        bala.dibujo(ventana)
        bala.update(grupo_enemigos)

    revivir=personaje.dibujo(ventana)
    
    if not revivir:
        enemigos=personaje.eneemies()
        if enemigos:
            grupo_enemigos.add(enemigos)

        for enemy in grupo_enemigos:
            enemy.dinujo(ventana)
            enemy.update()
    else:
        a=personaje.destruccion()
        for enemy in grupo_enemigos:
            enemy.dinujo(ventana)
            enemy.destruccion(a)


    if personaje.vidas==3:
        ventana.blit(vidas_3,(constants.ancho-vidas_3.get_width(),constants.alto-vidas_3.get_height()))
    elif personaje.vidas==2:
        ventana.blit(vidas_2,(constants.ancho-vidas_3.get_width(),constants.alto-vidas_3.get_height()))
    elif personaje.vidas==1:
        ventana.blit(vidas_1,(constants.ancho-vidas_3.get_width(),constants.alto-vidas_3.get_height()))
    if personaje.vidas<=0:
        execute=False

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            execute=False

    #actualiza la pantalla
    pygame.display.update()

pygame.quit()