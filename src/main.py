import time
import pygame
import constants
import player
import scoreboard

pygame.init()
with open('data/nave.txt', 'r') as archivo:
    nave = int(archivo.read().strip())
archivo.close
with open('data/highscore.txt', 'r') as archivo:
    highscore = int(archivo.read().strip())
archivo.close

# Función para inicializar el juego
def initialize_game():
    #Creación de la ventana con sus respectivas dimensiones predefinido.
    screen_org = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Space survivor")

    #Carga y redimensión de la imagen de fondo predefinido.
    imgbackground_org = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
    imgbackground_org = pygame.transform.scale(imgbackground_org, (constants.WIDTH, constants.HEIGHT))

    #Carga y reproduccion musica de fondo.
    pygame.mixer.music.load("assets/audio/background_music.wav")
    pygame.mixer.music.play(-1)

    #Carga y redimensión de la bala predefinido.
    imgbullet_org = pygame.image.load("assets/images/bullets/plasma_bullet.png").convert_alpha()
    imgbullet_org = pygame.transform.scale(imgbullet_org, (imgbullet_org.get_width() * constants.FACTOR_BULLET, imgbullet_org.get_height() * constants.FACTOR_BULLET))

    #Carga de la imagen de los asteroides predefinido.
    asteroids_org = []
    iron_asteroids_org=[]
    for i in range(5):
        asteroid = pygame.image.load("assets/images/asteroids/stone_asteroid/meteor_sprite{}.png".format(i)).convert_alpha()
        asteroid = pygame.transform.scale(asteroid, (asteroid.get_width() * constants.FACTOR_ASTEROID, asteroid.get_height() * constants.FACTOR_ASTEROID))
        asteroid_metal = pygame.image.load("assets/images/asteroids/iron_asteroid/iron_meteor{}.png".format(i)).convert_alpha()
        asteroid_metal = pygame.transform.scale(asteroid_metal, (asteroid_metal.get_width() * constants.FACTOR_ASTEROID/4, asteroid_metal.get_height() * constants.FACTOR_ASTEROID/4))
        iron_asteroids_org.append(asteroid_metal)
        asteroids_org.append(asteroid)

    #Creación de un scoreboard para llevar registro de la puntuación del Player predefinido.
    scoreboards_org = scoreboard.Scoreboard(highscore)

    #Carga del sonido de disparo y explosiones.
    explosion_sound_org = pygame.mixer.Sound("assets/audio/explosion.mp3")
    shot_sound_org = pygame.mixer.Sound("assets/audio/shot_blaster.mp3")
    shot_sound_org.set_volume(0.1)

    #Carga y asignación de los sprites del personaje y la creación de este predefinido.
    animations_org = []
    for c in range(2):
        temp = []
        for i in range(9):
            imgcharacter = pygame.image.load(f"assets/images/characters/character_{c}/character_{i + 1}.png").convert_alpha()
            imgcharacter = pygame.transform.scale(imgcharacter, (imgcharacter.get_width() * constants.FACTOR_CHARACTER, imgcharacter.get_height() * constants.FACTOR_CHARACTER))
            temp.append(imgcharacter)
        animations_org.append(temp)
    temp = []
    for i in range(9):
            imgcharacter = pygame.image.load(f"assets/images/characters/character_2/character_{i + 1}.png").convert_alpha()
            imgcharacter = pygame.transform.scale(imgcharacter, (imgcharacter.get_width() * constants.FACTOR_CHARACTER*2, imgcharacter.get_height() * constants.FACTOR_CHARACTER*2))
            temp.append(imgcharacter)    
    animations_org.append(temp)
    user_player_org = player.Player(screen_org.get_width() / 2, screen_org.get_height() / 2, animations_org, imgbullet_org, asteroids_org,iron_asteroids_org, constants.LIFES, scoreboards_org, shot_sound_org, explosion_sound_org,nave)

    #Imágenes de las vidas predefinidas.
    life_3_org = pygame.image.load("assets/images/lifes/lifes_3.png").convert_alpha()
    life_2_org = pygame.image.load("assets/images/lifes/lifes_2.png").convert_alpha()
    life_1_org = pygame.image.load("assets/images/lifes/lifes_1.png").convert_alpha()

    #Crear grupo de sprites predefinidos.
    bullets_group_org = pygame.sprite.Group()
    group_enemies_org = pygame.sprite.Group()

    #Posición inicial del fondo.
    x_org = 0
    font_org = pygame.font.Font(None, 36)

    return screen_org, imgbackground_org, imgbullet_org, asteroids_org, animations_org, user_player_org, scoreboards_org, life_3_org, life_2_org, life_1_org, bullets_group_org, group_enemies_org, x_org, font_org


#Inicialización del juego
screen, imgbackground, imgbullet, asteroids, animations, user_player, scoreboards, life_3, life_2, life_1, bullets_group, group_enemies, x, font = initialize_game()

#Configuración de la pantalla de "Game Over".
imgbackground_game_over = pygame.image.load("assets/images/background/background_lose.png").convert_alpha()
imgbackground_game_over = pygame.transform.scale(imgbackground_game_over, (constants.WIDTH, constants.HEIGHT))

#Bucle principal del juego
game_over = False
quit_bool = False
menu=True
skiny=False

inicio=pygame.image.load("assets/images/buttons/button_play.png")
skins=pygame.image.load("assets/images/buttons/button_skins.png")
salida=pygame.image.load("assets/images/buttons/button_exit.png")
back=pygame.image.load("assets/images/buttons/button_back.png") 
again=pygame.image.load("assets/images/buttons/button_tryagain.png")
again_rect = again.get_rect(topleft=(800,600))
inicio_rect = inicio.get_rect(topleft=(constants.WIDTH/2-220, 200))
skins_rect = skins.get_rect(topleft=(constants.WIDTH/2-220, 336))
salida_rect = salida.get_rect(topleft=(constants.WIDTH/2-220-5, 472))
back_rect = back.get_rect(topleft=(10,25))
back_rect_go = back.get_rect(topleft=(300,600))
nave_1=pygame.transform.scale(animations[0][0],(300,300))
nave_2=pygame.transform.scale(animations[1][0],(300,300))
nave_3=pygame.transform.scale(animations[2][0],(300,300))
nave_10=nave_1.get_rect(topleft=(250,constants.HEIGHT/2-150))
nave_20=nave_1.get_rect(topleft=(650,constants.HEIGHT/2-150))
nave_30=nave_1.get_rect(topleft=(1050,constants.HEIGHT/2-150))

def menus():
    screen.blit(imgbackground,(0,0))
    screen.blit(inicio,(constants.WIDTH/2-220, 200))
    screen.blit(skins,(constants.WIDTH/2-220, 336))
    screen.blit(salida,(constants.WIDTH/2-220-5, 472))
    
    pygame.display.update()

def skin():
    screen.blit(imgbackground,(0,0))
    screen.blit(back, (10,25))
    screen.blit(nave_1,(250,constants.HEIGHT/2-150))
    screen.blit(nave_2,(650,constants.HEIGHT/2-150))
    screen.blit(nave_3,(1050,constants.HEIGHT/2-150))
    if nave == 0:
        pygame.draw.rect(screen, (255, 255, 0), (245,constants.HEIGHT/2-170, 305, 345), 5)
    elif nave == 1:
        pygame.draw.rect(screen, (255, 255, 0), (635,constants.HEIGHT/2-170, 305, 345), 5)
    else: pygame.draw.rect(screen, (255, 255, 0), (1045,constants.HEIGHT/2-170, 305, 345), 5)

    pygame.display.update()

while not game_over:
    running = True
    #Limitando velocidad.
    clock = pygame.time.Clock()
    if menu:
        menus()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                if inicio_rect.collidepoint(event.pos):
                    menu=False
                if skins_rect.collidepoint(event.pos):
                    menu=False
                    skiny=True
                if salida_rect.collidepoint(event.pos):
                    game_over=True
    elif skiny:
        skin()  
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    menu=True
                    skiny=False 
                    user_player.cambio(nave)
                    with open('data/nave.txt', 'w') as archivo:
                        archivo.write(str(nave))
                    archivo.close
                if nave_10.collidepoint(event.pos):
                    nave=0
                if nave_20.collidepoint(event.pos):
                    nave=1 
                if nave_30.collidepoint(event.pos):
                    nave=2      
                pygame.display.update()     
    else:
        while running:
            clock.tick(constants.FPS)

            #Configuración del movimiento del fondo de pantalla.
            x_rel = x % imgbackground.get_rect().width
            screen.blit(imgbackground, (x_rel - imgbackground.get_rect().width, 0))
            if x_rel < constants.WIDTH:
                screen.blit(imgbackground, (x_rel, 0))
            x -= 1

            one_bullet = user_player.update(group_enemies)
            if one_bullet:
                bullets_group.add(one_bullet)

            for one_bullet in bullets_group:
                one_bullet.drawing(screen)
                one_bullet.update(group_enemies)

            revive = user_player.drawing(screen)

            if not revive:
                enemies = user_player.enemies()
                if enemies:
                    group_enemies.add(enemies)

                for enemy in group_enemies:
                    enemy.drawing(screen)
                    enemy.update()
            else:
                radius = user_player.destroy()
                for enemy in group_enemies:
                    enemy.drawing(screen)
                    enemy.destroy(radius)

            if user_player.lifes == 3:
                screen.blit(life_3, (constants.WIDTH - life_3.get_width(), constants.HEIGHT - life_3.get_height()))
            elif user_player.lifes == 2:
                screen.blit(life_2, (constants.WIDTH - life_3.get_width(), constants.HEIGHT - life_3.get_height()))
            elif user_player.lifes == 1:
                screen.blit(life_1, (constants.WIDTH - life_3.get_width(), constants.HEIGHT - life_3.get_height()))
            if user_player.lifes <= 0:
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit_bool = True

            #Actualiza la pantalla y el scoreboard.
            scoreboards.render(screen)
            pygame.display.update()

        #Configuración del bucle de "Game Over".
        game_over = True
        if highscore < scoreboards.score:
            highscore = scoreboards.score
            with open('data/highscore.txt', 'w') as archivo:
                archivo.write(str(highscore))
            archivo.close
        while game_over:
            if quit_bool:
                break
            screen.blit(imgbackground_game_over, (0, 0))
            screen.blit(back, (300, 600))
            screen.blit(again, (800, 600))

            pygame.display.update()

            # Manejar eventos del mouse para salir del "Game Over" y reiniciar el juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    quit_bool = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect_go.collidepoint(event.pos):
                        game_over = False
                        running = False
                        menu = True
                        screen, imgbackground, imgbullet, asteroids, animations, user_player, scoreboards, life_3, life_2, life_1, bullets_group, group_enemies, x, font = initialize_game()
                    if again_rect.collidepoint(event.pos):
                        game_over = False
                        screen, imgbackground, imgbullet, asteroids, animations, user_player, scoreboards, life_3, life_2, life_1, bullets_group, group_enemies, x, font = initialize_game()
        if game_over: break

pygame.quit()
