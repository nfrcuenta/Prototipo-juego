import time
import pygame
import constants
import player
import scoreboard

pygame.init()


# Función para inicializar el juego
def initialize_game():
    #Creación de la ventana con sus respectivas dimensiones predefinido.
    screen_org = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Space survivor")

    #Carga y redimensión de la imagen de fondo predefinido.
    imgbackground_org = pygame.image.load("../assets/images/background/background.jpg").convert_alpha()
    imgbackground_org = pygame.transform.scale(imgbackground_org, (constants.WIDTH, constants.HEIGHT))

    #Carga y redimensión de la bala predefinido.
    imgbullet_org = pygame.image.load("../assets/images/bullets/plasma_bullet.png").convert_alpha()
    imgbullet_org = pygame.transform.scale(imgbullet_org, (imgbullet_org.get_width() * constants.FACTOR_BULLET, imgbullet_org.get_height() * constants.FACTOR_BULLET))

    #Carga de la imagen de los asteroides predefinido.
    asteroids_org = pygame.image.load("../assets/images/asteroids/meteor_sprite0.png").convert_alpha()
    asteroids_org = pygame.transform.scale(asteroids_org, (asteroids_org.get_width() * constants.FACTOR_ASTEROID, asteroids_org.get_height() * constants.FACTOR_ASTEROID))

    #Creación de un scoreboard para llevar registro de la puntuación del Player predefinido.
    scoreboards_org = scoreboard.Scoreboard()

    #Carga y asignación de los sprites del personaje y la creación de este predefinido.
    animations_org = []
    for i in range(9):
        imgcharacter = pygame.image.load(f"../assets/images/characters/character_primary/character_{i + 1}.png").convert_alpha()
        imgcharacter = pygame.transform.scale(imgcharacter, (imgcharacter.get_width() * constants.FACTOR_CHARACTER, imgcharacter.get_height() * constants.FACTOR_CHARACTER))
        animations_org.append(imgcharacter)
    user_player_org = player.Player(screen_org.get_width() / 2, screen_org.get_height() / 2, animations_org, imgbullet_org, asteroids_org, constants.LIFES, scoreboards_org)

    #Imágenes de las vidas predefinidas.
    life_3_org = pygame.image.load("../assets/images/lifes/lifes_3.png").convert_alpha()
    life_2_org = pygame.image.load("../assets/images/lifes/lifes_2.png").convert_alpha()
    life_1_org = pygame.image.load("../assets/images/lifes/lifes_1.png").convert_alpha()

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
imgbackground_game_over = pygame.image.load("../assets/images/background/background_lose.png").convert_alpha()
imgbackground_game_over = pygame.transform.scale(imgbackground_game_over, (constants.WIDTH, constants.HEIGHT))
font_game_over = pygame.font.Font(None, 36)
text_game_over = font_game_over.render("Try again?", True, (255, 255, 255))
text_rect_game_over = text_game_over.get_rect(center=(constants.WIDTH // 2, 700))

#Bucle principal del juego
game_over = False
quit_bool = False
while not game_over:
    running = True
    #Limitando velocidad.
    clock = pygame.time.Clock()

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
    timer = 5
    start_time = time.time()
    while game_over:
        if quit_bool:
            break
        screen.blit(imgbackground_game_over, (0, 0))
        screen.blit(text_game_over, text_rect_game_over)

        #Mostrar el temporizador
        timer = int(6 - (time.time() - start_time))
        text_timer = font_game_over.render(f"{timer}", True, (255, 255, 255))
        timer_rect = text_timer.get_rect(center=(constants.WIDTH // 2, 750))
        screen.blit(text_timer, timer_rect)

        pygame.display.update()

        # Manejar eventos del mouse para salir del "Game Over" y reiniciar el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_over = False
                # Reiniciar juego
                screen, imgbackground, imgbullet, asteroids, animations, user_player, scoreboards, life_3, life_2, life_1, bullets_group, group_enemies, x, font = initialize_game()
                break
        if timer <= 0:
            break
    if game_over: break

pygame.quit()
