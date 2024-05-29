import pygame
import sys
import os
from multiprocessing import Process
import math

# Constantes de colores mejorados
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HOVER_YELLOW = (255, 255, 153)  # Amarillo claro
HOVER_GREEN = (153, 255, 153)  # Verde claro
HOVER_RED = (255, 153, 153)  # Rojo claro
BUTTON_WIDTH = 0.3  # Ancho relativo del botón respecto al ancho de la pantalla
BUTTON_HEIGHT = 0.1  # Altura relativa del botón respecto a la altura de la pantalla
BORDER_RADIUS = 15  # Radio de las esquinas redondeadas

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)  # Tamaño inicial de la ventana
        pygame.display.set_caption("Menú de Mastermind")
        self.clock = pygame.time.Clock()
        self.selected_option = None
        self.background_image = self.load_background_image(os.path.join("mastermind_imagenes", "fondo1.jpg"))
        self.gif_image = self.load_gif(os.path.join("mastermind_imagenes", "mov.gif"))
        self.gif_rect = self.gif_image.get_rect(topleft=(10, self.screen.get_height() - self.gif_image.get_height() - 10))  # Rectángulo del gif

    def load_background_image(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        return image

    def load_gif(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        return image

    def run(self):
        running = True
        while running:
            self.screen.blit(pygame.transform.scale(self.background_image, self.screen.get_size()), (0, 0))  # Se ajusta el tamaño de la imagen de fondo
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.option_4_rect.collidepoint(mouse_pos):
                        self.selected_option = 4
                        running = False
                    elif self.option_6_rect.collidepoint(mouse_pos):
                        self.selected_option = 6
                        running = False
                    elif self.quit_rect.collidepoint(mouse_pos):
                        running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((max(800, event.w), max(600, event.h)), pygame.RESIZABLE)  # Se ajusta el tamaño de la ventana
                    self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())  # Se ajusta el tamaño de la imagen de fondo
                    self.gif_rect.topleft = (10, self.screen.get_height() - self.gif_image.get_height() - 10)  # Se ajusta la posición del gif

            self.move_gif()  # Mover el gif
            self.draw_buttons(mouse_pos)
            self.screen.blit(self.gif_image, self.gif_rect.topleft)  # Dibuja el GIF en la posición actual
            pygame.display.flip()
            self.clock.tick(30)

    def draw_buttons(self, mouse_pos):
        font = pygame.font.Font(None, int(self.screen.get_height() * 0.04))

        button_width = int(self.screen.get_width() * BUTTON_WIDTH)
        button_height = int(self.screen.get_height() * BUTTON_HEIGHT)

        self.option_4_rect = pygame.Rect(self.screen.get_width() * 0.35, self.screen.get_height() * 0.4, button_width, button_height)  # Se ajusta la posición y el tamaño del botón
        self.option_6_rect = pygame.Rect(self.screen.get_width() * 0.35, self.screen.get_height() * 0.55, button_width, button_height)  # Se ajusta la posición y el tamaño del botón
        self.quit_rect = pygame.Rect(self.screen.get_width() * 0.35, self.screen.get_height() * 0.7, button_width, button_height)  # Se ajusta la posición y el tamaño del botón

        self.draw_button(self.option_4_rect, "Jugar con 4 colores", mouse_pos, font, GREEN, HOVER_GREEN)
        self.draw_button(self.option_6_rect, "Jugar con 6 colores", mouse_pos, font, YELLOW, HOVER_YELLOW)
        self.draw_button(self.quit_rect, "Salir", mouse_pos, font, RED, HOVER_RED)

    def draw_button(self, rect, text, mouse_pos, font, color, hover_color):
        if rect.collidepoint(mouse_pos):
            current_color = hover_color
        else:
            current_color = color
        
        pygame.draw.rect(self.screen, current_color, rect, border_radius=BORDER_RADIUS)

        text_surf = font.render(text, True, BLACK)  # El texto es de color negro
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def move_gif(self):
        # Movimiento sinusoidal del gif
        displacement = 10 * math.sin(pygame.time.get_ticks() * 0.002)
        self.gif_rect.bottom = self.screen.get_height() - 10 + displacement

def run_game(file):
    p = Process(target=os.system, args=(f"python {file}",))
    p.start()
    p.join()

if __name__ == "__main__":
    menu = Menu()
    while True:
        menu.run()

        if menu.selected_option == 4:
            p = Process(target=run_game, args=("mastermind_niveles/mastermind1.py",))
            p.start()
            p.join()
            menu.selected_option = None
        elif menu.selected_option == 6:
            p = Process(target=run_game, args=("mastermind_niveles/mastermind2.py",))
            p.start()
            p.join()
            menu.selected_option = None
        elif menu.selected_option is None:
            break
