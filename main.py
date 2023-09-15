import pygame
import os
pygame.font.init()

#definicion de constantes
WIDTH, HEIGHT = 500, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kodland First Game!")

LIVES_FONT = pygame.font.SysFont('Arial Black', 20)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

EARTH_HIT = pygame.USEREVENT + 1
INVASORY_HIT = pygame.USEREVENT + 2 

SPACESHIP_IMG = pygame.image.load(os.path.join('recursos', 'spaceship.png'))
SPACESHIP = pygame.transform.scale(SPACESHIP_IMG, (65,50))

INVASORY_IMG = pygame.image.load(os.path.join('recursos', 'invasor.png'))
INVASORY = pygame.transform.scale(INVASORY_IMG, (30,30))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('recursos', 'space.png')),(WIDTH, HEIGHT))


def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)

#Funcion que me dibuja y actualiza la ventana del juego
def draw_window(ship, invasor, bullets, lives, invasor_health):
    WIN.fill('black')
    WIN.blit(SPACE,(0, 0))

    lives_text = LIVES_FONT.render("Vidas: " + str(lives), 1, "white")
    enemies_text = LIVES_FONT.render("Enemigos con vida:" + str(invasor_health),  1, "white")
    WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))
    WIN.blit(enemies_text, (10,10))

    WIN.blit(SPACESHIP, (ship.x, ship.y))
    WIN.blit(INVASORY, (invasor.x , invasor.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, 'red', bullet)

    pygame.display.update()

#Funcion que mueve la nave
def move_spaceship(keys, nave):
    if keys[pygame.K_LEFT] and nave.x - VEL > 0:
        nave.x -= VEL
    if keys[pygame.K_RIGHT] and nave.x + VEL + nave.width < WIDTH:
        nave.x += VEL
    if keys[pygame.K_UP] and nave.y - VEL > 0:
        nave.y -= VEL
    if keys[pygame.K_DOWN] and nave.y + VEL + nave.height < HEIGHT:
        nave.y += VEL

#Funcion que hace aparecer los invasores
def move_invasories(enemy):
    enemy.y += 1

def handle_bullets(bullets, spaceship, enemy):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if enemy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(INVASORY_HIT))
            bullets.remove(bullet)
        elif bullet.y < 0:
            bullets.remove(bullet)

def main():
    defender = pygame.Rect(225, 500, 65, 50)
    enemy = pygame.Rect(100, 00, 30, 30)
    lives = 3
    invasor_health = 3

    bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(defender.x + defender.width//2 - 2, defender.y + defender.height, 5, 10)
                    bullets.append(bullet)

            if event.type == EARTH_HIT:
                life -= 1
            
            if event.type == INVASORY_HIT:
                invasor_health -= 1
        win_text =""
        if lives <= 0:
            win_text = "GAME OVER"

        if invasor_health <= 0:
            win_text = "YOU WIN, ENEMY DESTROYED"
        
        if win_text != "":
            pass #Win or not



        keys_pressed = pygame.key.get_pressed()
        move_spaceship(keys_pressed, defender)
        move_invasories(enemy)

        handle_bullets(bullets, defender, enemy)
        draw_window(defender, enemy, bullets, 
                    lives, invasor_health)
        
    pygame.quit()

if __name__ == '__main__':
    main()