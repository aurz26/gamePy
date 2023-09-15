import pygame
import os
import random

pygame.font.init()

# Definición de constantes
WIDTH, HEIGHT = 500, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IN-vasion!")

LIVES_FONT = pygame.font.SysFont('Arial Black', 20)
WINNER_FONT = pygame.font.SysFont('Arial Black', 30)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 100

EARTH_HIT = pygame.USEREVENT + 1
INVASORY_HIT = pygame.USEREVENT + 2

SPACESHIP_IMG = pygame.image.load(os.path.join('recursos', 'spaceship.png'))
SPACESHIP = pygame.transform.scale(SPACESHIP_IMG, (65, 50))

INVASORY_IMG = pygame.image.load(os.path.join('recursos', 'invasor.png'))
INVASORY = pygame.transform.scale(INVASORY_IMG, (30, 30))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('recursos', 'space.png')), (WIDTH, HEIGHT))

# Variable global para definir un estado para el juego (jugando, pausado, etc.)
game_paused = False


class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 65
        self.height = 50

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - VEL > 0:
            self.x -= VEL
        if keys[pygame.K_RIGHT] and self.x + VEL + self.width < WIDTH:
            self.x += VEL
        if keys[pygame.K_UP] and self.y - VEL > 0:
            self.y -= VEL
        if keys[pygame.K_DOWN] and self.y + VEL + self.height < HEIGHT:
            self.y += VEL

    def draw(self, window):
        window.blit(SPACESHIP, (self.x, self.y))


class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30

    def move(self):
        self.y += 1

    def draw(self, window):
        window.blit(INVASORY, (self.x, self.y))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10

    def move(self):
        self.y -= BULLET_VEL

    def draw(self, window):
        pygame.draw.rect(window, 'red', (self.x, self.y, self.width, self.height))


def generate_random_enemy():
    x = random.randint(0, WIDTH - 30)  # Posición x aleatoria
    y = -30  # Posición y fuera de la pantalla (aparecerá desde arriba)
    return Invader(x, y)


def draw_pause_menu(game_paused):
    WIN.fill((0, 0, 0, 128))  # Fondo semitransparente para el menú de pausa
    pause_text = LIVES_FONT.render("PAUSA", 1, "white")
    resume_text = LIVES_FONT.render("1. Reanudar", 1, "white")
    restart_text = LIVES_FONT.render("2. Reiniciar", 1, "white")
    quit_text = LIVES_FONT.render("3. Salir", 1, "white")

    WIN.blit(pause_text, (WIDTH / 2 - pause_text.get_width() / 2, HEIGHT / 2 - 100))
    WIN.blit(resume_text, (WIDTH / 2 - resume_text.get_width() / 2, HEIGHT / 2 - 50))
    WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2))
    WIN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 50))
    
    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, 'white')
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    global game_paused #Accedemos a variable global para el menu 
    defender = Spaceship(225, 500)
    enemies = []
    lives = 5
    invasor_health = 15
    enemies_reached_planet = 0
    bullets = []
    clock = pygame.time.Clock()
    enemy_spawn_timer = 0  # Inicializa el temporizador para la generación de enemigos
   
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = Bullet(defender.x + defender.width // 2 - 2, defender.y + defender.height)
                    bullets.append(bullet)
            if event.type == EARTH_HIT:
                lives -= 1
            if event.type == INVASORY_HIT:
                invasor_health -= 1

        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 60:
            enemy = generate_random_enemy()
            enemies.append(enemy)
            enemy_spawn_timer = 0

        win_text = ""
        if lives <= 0:
            win_text = "GAME OVER"
        if invasor_health <= 0:
            win_text = "YOU WIN, ENEMY DESTROYED"

        if win_text != "":
            draw_winner(win_text)

        keys_pressed = pygame.key.get_pressed()

        # Comprueba si se presiona la tecla ESC para activar/desactivar el menú de pausa
        if keys_pressed[pygame.K_ESCAPE]:
            game_paused = not game_paused  # Invierte el estado de pausa

        if game_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Reanudar juego
                        game_paused = not game_paused
                    elif event.key == pygame.K_2:  # Reiniciar juego
                        main()  # Llama a la función main para reiniciar el juego
                    elif event.key == pygame.K_3:  # Salir del juego
                        pygame.quit()
                        quit()
            draw_pause_menu(game_paused)
        else:
            defender.move(keys_pressed)

            for enemy in enemies:
                enemy.move()
                # Verifica si un enemigo alcanza el "planeta"
                if enemy.y + enemy.height > HEIGHT:
                    enemies_reached_planet += 1
                    lives -= 1
                    enemies.remove(enemy)

            # Verifica si se alcanza el límite de enemigos que llegan al "planeta"
            if enemies_reached_planet >= 5:
                draw_winner("GAME OVER")
                pygame.time.delay(2000)
                run = False

            for bullet in bullets:
                bullet.move()
                for enemy in enemies:
                    if enemy.x < bullet.x < enemy.x + enemy.width and enemy.y < bullet.y < enemy.y + enemy.height:
                        pygame.event.post(pygame.event.Event(INVASORY_HIT))
                        bullets.remove(bullet)
                        enemies.remove(enemy)

            # Elimina enemigos que están fuera de la pantalla
            enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]

            WIN.fill('black')
            WIN.blit(SPACE, (0, 0))

            lives_text = LIVES_FONT.render("Vidas: " + str(lives), 1, "white")
            enemies_text = LIVES_FONT.render("Enemigos con vida: " + str(invasor_health), 1, "white")
            WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))
            WIN.blit(enemies_text, (10, 10))

            defender.draw(WIN)

            for enemy in enemies:
                enemy.draw(WIN)

            for bullet in bullets:
                bullet.draw(WIN)

            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()