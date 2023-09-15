# gamePy
Repositorio creacion de un juego utilizando la libreria PyGame
# IN-vasion!

Este es un juego simple llamado "IN-vasion!" creado con Pygame. En el juego, se controla una nave espacial que debe defender la Tierra de invasores alienígenas. A continuación, se describe la estructura y los aspectos clave del código:

## Descripción General
El objetivo del juego es eliminar a los invasores antes de que lleguen a la Tierra y agoten tus vidas. También puedes pausar el juego en cualquier momento haciendo uso de la tecla ESC.

## Constantes
- `WIDTH` y `HEIGHT` definen el tamaño de la ventana del juego.
- `WIN` es la ventana de juego de Pygame.
- `LIVES_FONT` y `WINNER_FONT` son fuentes para mostrar la cantidad de vidas y el mensaje de ganador, respectivamente.
- `FPS` establece la velocidad de fotogramas por segundo.
- `VEL` controla la velocidad de movimiento de la nave.
- `BULLET_VEL` determina la velocidad de las balas.
- `MAX_BULLETS` es la cantidad máxima de balas permitidas en pantalla.
- `EARTH_HIT` e `INVASORY_HIT` son eventos personalizados para gestionar colisiones y eventos en el juego.
- `SPACESHIP_IMG`, `INVASORY_IMG` y `SPACE` son las imágenes utilizadas en el juego.

## Clases
- `Spaceship` representa la nave espacial que se debe controlar.
- `Invader` representa a los invasores alienígenas.
- `Bullet` representa las balas disparadas desde la nave.

## Funciones
- `generate_random_enemy` crea un nuevo enemigo en una posición aleatoria en la parte superior de la pantalla.
- `draw_pause_menu` muestra un menú de pausa si el juego está en pausa.
- `draw_winner` muestra un mensaje de ganador o perdedor al final del juego.
- `main` es la función principal que ejecuta el bucle del juego.

## Uso
Para jugar, controla la nave espacial con las teclas de dirección y dispara balas con la barra espaciadora. Puedes pausar el juego en cualquier momento presionando la tecla "ESC".
