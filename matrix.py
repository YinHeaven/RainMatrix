import pygame
import random
import sys
import time

# --- Configuración ---
WIDTH, HEIGHT = 800, 600  
FONT_SIZE = 16
COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
TRAIL_OPACITY = 10  # disminuye el numero aqui para dejar un ratro masl argo
SPEED_FACTOR = 0.9
DELAY_FACTOR = 2

# --- Caracteres nota: aqui si quieren agragarle otro idioma cren una variable nueva con lso coracteres que quieren usar pasado como una array y concatenar en matrix_char
latin_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzç1234567890!@#$%^&*()-_=+[]{}|;:',.<>?/`~¡™£¢∞§¶•ªº–≠œ∑´®†¥¨ˆøπ“‘åß∂ƒ©˙∆˚¬Ω≈ç√∫˜µ≤≥÷"
japanese_chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん一二三四五六七八九十零"
matrix_chars = latin_chars + japanese_chars
characters = list(matrix_chars)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Matrix Rain (Python)")

# tryhardea la fuente mono space o si no la que tenga alaverga
try:
    font = pygame.font.SysFont("monospace", FONT_SIZE)
except pygame.error:
    font = pygame.font.Font(None, FONT_SIZE) 

#Variables de la animación
current_width, current_height = screen.get_size()
columns = current_width // FONT_SIZE
drops = [0] * columns
delays = [1] * columns # Retraso de columnas

#Bucle principal del juego/animación
running = True
last_update_time = time.time()

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            #redimensionamiento de la ventana
            current_width, current_height = event.size
            screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            columns = current_width // FONT_SIZE
            #  drops y delays si el número de columnas cambia
            if len(drops) != columns:
                drops = [0] * columns
                delays = [1] * columns

    #Aqui configuran la animacion (fps/vel/fondo/render...)
    current_time = time.time()
    # Controlar la velocidad de actualización (simula requestAnimationFrame)
    # Ajusta el valor 0.03 para cambiar la velocidad general de la animación
    if current_time - last_update_time > 0.03: # Aproximadamente 30 FPS
        last_update_time = current_time

        # Dibujar el rastro (fondo semi-transparente)
        trail_surface = pygame.Surface((current_width, current_height))
        trail_surface.set_alpha(TRAIL_OPACITY)
        trail_surface.fill(BACKGROUND_COLOR)
        screen.blit(trail_surface, (0, 0))

        # Dibujar los caracteres
        for i in range(columns):
            #si la ventana se redimensiona rápidamente asegura que el índice esté dentro de los limites 
            if i >= len(drops):
                continue

            text = random.choice(characters)
            x = i * FONT_SIZE
            y = drops[i] * FONT_SIZE

            # Renderizar el texto
            text_surface = font.render(text, True, COLOR)
            screen.blit(text_surface, (x, y))

            # Mover la gota hacia abajo basado en el retraso
            if delays[i] <= 0:
                drops[i] += 1 # Mover hacia abajo una posición
                # Reiniciar retraso con factor de retraso
                delays[i] = random.random() * (DELAY_FACTOR / SPEED_FACTOR)
            else:
                delays[i] -= 1 # Reducir retraso

            # Reiniciar gota en la parte superior aleatoriamente
            # Usamos current_height para la altura actual de la ventana
            if y > current_height and random.random() > 0.975:
                drops[i] = 0 # Reiniciar en la parte superior

        # --- Actualizar la pantalla ---
        pygame.display.flip() # O display.update()

pygame.quit()
sys.exit()
