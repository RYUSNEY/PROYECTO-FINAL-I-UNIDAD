import pygame
import sys
import os

# Constantes de colores
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

DARKGREY = (40, 40, 40)
LIGHTGREY = (120, 80, 80)
DARKBROWN = (55, 22, 30)
BLUE = (0, 0, 200)
PINK = (210, 0, 210)
ORANGE = (210, 110, 0)
BGCOLOUR = (118, 50, 42)

def run_game1():
    os.system("python laberintos.py")

def run_game2():
    os.system("python mastermind.py")

def run_game3():
    os.system("python clue.py")

def main():
    pygame.init()

    # Tamaño inicial de la pantalla
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Elegir un juego")

    # Cargar el primer frame del GIF como imagen estática
    first_frame_path = os.path.join("menu_recursos", "menu.gif")
    background_static = pygame.image.load(first_frame_path)
    background_static = pygame.transform.scale(background_static, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Funciones de botón
    buttons = [
        {"text": "Laberintos", "action": run_game1},
        {"text": "Mastermind", "action": run_game2},
        {"text": "Clue", "action": run_game3}
    ]

    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 74)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    rect = font.render(button["text"], True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, 200 + buttons.index(button) * 100))
                    if rect.collidepoint(event.pos):
                        button["action"]()

        screen.fill(WHITE)
        # Mostrar la imagen estática en lugar del GIF
        screen.blit(background_static, (0, 0))

        # Dibujar título
        title_text = "Bienvenido"
        title_surface = title_font.render(title_text, True, WHITE)
        title_x = (SCREEN_WIDTH - title_surface.get_width()) // 2
        title_y = 50
        screen.blit(title_surface, (title_x, title_y))

        # Dibujar botones
        for button in buttons:
            button_rect = pygame.Rect(0, 0, 200, 50)
            button_rect.center = (SCREEN_WIDTH // 2, 200 + buttons.index(button) * 100)
            pygame.draw.rect(screen, GREEN, button_rect, border_radius=10)
            text_surface = font.render(button["text"], True, BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
