import pygame
import sys
import os
from pygame.locals import *
from PIL import Image

# Inicializar Pygame
pygame.init()

# Colores
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

# Leer el GIF y obtener sus cuadros
gif_level_path = os.path.join("laberintos_imagenes", "level_labyrinth.gif")
background_gif = Image.open(gif_level_path)

gif_select_path = os.path.join("laberintos_imagenes", "select_labyrinth.gif")
labyrinth_select_gif = Image.open(gif_select_path)

frames = []
labyrinth_select_frames = []

try:
    while True:
        frame = background_gif.copy()
        frames.append(frame)
        background_gif.seek(len(frames))
except EOFError:
    pass

try:
    while True:
        frame = labyrinth_select_gif.copy()
        labyrinth_select_frames.append(frame)
        labyrinth_select_gif.seek(len(labyrinth_select_frames))
except EOFError:
    pass

# Convertir cuadros a Surface de Pygame
gif_frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) for frame in frames]
labyrinth_select_gif_frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) for frame in labyrinth_select_frames]

class Node:
    def __init__(self, state, parent, action, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

class GreedyBestFirstFrontier:
    def __init__(self, heuristic):
        self.frontier = []
        self.heuristic = heuristic

    def add(self, node):
        cost = self.heuristic(node)
        self.frontier.append((node, cost))
        self.frontier.sort(key=lambda x: x[1])  # sort by heuristic value

    def contains_state(self, state):
        return any(node.state == state for node, _ in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node, _ = self.frontier.pop(0)
            return node

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("maze must have exactly one start point and one goal")
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self, strategy='gbfs'):
        heuristic = lambda node: abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1])
        frontier = GreedyBestFirstFrontier(heuristic)
        start = Node(state=self.start, parent=None, action=None)
        frontier.add(start)
        self.explored = set()
        while True:
            if frontier.empty():
                raise Exception("no solution")
            node = frontier.remove()
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.explored.add(node.state)
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

def draw_button(screen, rect, color, text, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def main():
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Selector de Nivel de Laberintos")

    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

    easy_button = pygame.Rect(0, 0, 200, 50)
    medium_button = pygame.Rect(0, 0, 200, 50)
    hard_button = pygame.Rect(0, 0, 200, 50)

    running = True
    frame_index = 0

    while running:
        screen.fill(WHITE)
        #cambiooooo
        # Dibujar el fondo del GIF
        screen.blit(pygame.transform.scale(gif_frames[frame_index], screen.get_size()), (0, 0))
        frame_index = (frame_index + 1) % len(gif_frames)

        width, height = screen.get_size()

        title_surf = title_font.render("Elige el Nivel de Laberinto", True, BLACK)
        title_rect = title_surf.get_rect(center=(width // 2, height // 4))
        screen.blit(title_surf, title_rect)

        # Actualizar posiciones de botones para estar centrados
        easy_button.center = (width // 2, height // 2)
        medium_button.center = (width // 2, height // 2 + 70)
        hard_button.center = (width // 2, height // 2 + 140)

        draw_button(screen, easy_button, YELLOW, "Fácil", BLACK)
        draw_button(screen, medium_button, GREEN, "Medio", BLACK)
        draw_button(screen, hard_button, RED, "Difícil", BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    select_maze("easy")
                if medium_button.collidepoint(event.pos):
                    select_maze("medium")
                if hard_button.collidepoint(event.pos):
                    select_maze("hard")

        pygame.display.flip()
        pygame.time.wait(100)  # Controlar la velocidad del GIF

def select_maze(level):
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption(f"Seleccionar Laberinto - Nivel {level.capitalize()}")

    font = pygame.font.Font(None, 46)

    maze1_button = pygame.Rect(0, 0, 200, 50)
    maze2_button = pygame.Rect(0, 0, 200, 50)
    maze3_button = pygame.Rect(0, 0, 200, 50)
    back_button = pygame.Rect(0, 0, 200, 50)

    running = True
    frame_index = 0  # Definir frame_index aquí

    while running:
        screen.fill(WHITE)
        #cambio4
        screen.blit(pygame.transform.scale(labyrinth_select_gif_frames[frame_index], screen.get_size()), (0, 0))
        frame_index = (frame_index + 1) % len(labyrinth_select_gif_frames)
        
        width, height = screen.get_size()
        title_surf2 = font.render("Elige el laberinto", True, WHITE)
        title_rect2 = title_surf2.get_rect(center=(width // 2, height // 4))
        screen.blit(title_surf2, title_rect2)

        maze1_button.center = (width // 2, height // 2 - 35)
        maze2_button.center = (width // 2, height // 2 + 35)
        maze3_button.center = (width // 2, height // 2 + 105)
        back_button.center = (width // 2, height // 2 + 175)
        #cambio 2

        draw_button(screen, maze1_button, PINK, "Laberinto 1", BLACK)
        draw_button(screen, maze2_button, ORANGE, "Laberinto 2", BLACK)
        draw_button(screen, maze3_button, GREEN, "Laberinto 3", BLACK)
        draw_button(screen, back_button, RED, "Volver", WHITE)

        maze1_path = os.path.join("laberintos_niveles", f"{level}1.txt")
        maze2_path = os.path.join("laberintos_niveles", f"{level}2.txt")
        maze3_path = os.path.join("laberintos_niveles", f"{level}3.txt")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if maze1_button.collidepoint(event.pos):
                    maze_game(maze1_path)
                if maze2_button.collidepoint(event.pos):
                    maze_game(maze2_path)
                if maze3_button.collidepoint(event.pos):
                    maze_game(maze3_path)
                if back_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        pygame.time.wait(100)  # Controlar la velocidad del GIF

def show_winning_screen(screen):
    # Guardar las dimensiones originales de la pantalla
    original_width, original_height = screen.get_size()

    # Crear la pantalla de "Ganaste"
    winning_screen = pygame.display.set_mode((400, 300), pygame.RESIZABLE)

    font = pygame.font.Font(None, 36)

    # Cargar el GIF como fondo
    winning_gif = pygame.image.load("winx.gif")

    running = True
    while running:
        winning_screen.fill(WHITE)

        # Mostrar el GIF de fondo
        winning_screen.blit(pygame.transform.scale(winning_gif, (400, 300)), (0, 0))

        # Botón para volver al inicio
        back_button = pygame.Rect(150, 250, 100, 40)
        pygame.draw.rect(winning_screen, RED, back_button, border_radius=10)
        back_text = font.render("Volver", True, WHITE)
        text_rect = back_text.get_rect(center=back_button.center)
        winning_screen.blit(back_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    # Restaurar las dimensiones originales de la pantalla
                    screen = pygame.display.set_mode((original_width, original_height), pygame.RESIZABLE)
                    return  # Volver a la pantalla anterior

        pygame.display.flip()


def maze_game(maze_file):
    maze = Maze(maze_file)
    maze.solve()

    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Juego de Laberintos")

    player_pos = list(maze.start)
    clock = pygame.time.Clock()

    running = True
    show_solution = False
    won = False
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_s:
                    show_solution = not show_solution
                if event.key == K_UP and player_pos[0] > 0 and not maze.walls[player_pos[0] - 1][player_pos[1]]:
                    player_pos[0] -= 1
                if event.key == K_DOWN and player_pos[0] < maze.height - 1 and not maze.walls[player_pos[0] + 1][player_pos[1]]:
                    player_pos[0] += 1
                if event.key == K_LEFT and player_pos[1] > 0 and not maze.walls[player_pos[0]][player_pos[1] - 1]:
                    player_pos[1] -= 1
                if event.key == K_RIGHT and player_pos[1] < maze.width - 1 and not maze.walls[player_pos[0]][player_pos[1] + 1]:
                    player_pos[1] += 1
                if tuple(player_pos) == maze.goal:
                    show_winning_screen(screen)
                    return  # Volver a la ventana de selección de laberintos
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if draw_back_button(screen, font).collidepoint(event.pos):
                        return  # Return to maze selection screen

        screen.fill(BLACK)
        draw_maze(screen, maze, player_pos, show_solution)
        #cambio 6
        draw_back_button(screen, font)
        pygame.display.flip()
        clock.tick(30)

def draw_maze(screen, maze, player_pos, show_solution=False):
    width, height = screen.get_size()
    maze_width = maze.width
    maze_height = maze.height
    cell_size = min(width // maze_width, height // maze_height)
    offset_x = (width - maze_width * cell_size) // 2
    offset_y = (height - maze_height * cell_size) // 2 
    for i, row in enumerate(maze.walls):
        for j, col in enumerate(row):
            color = BLACK if col else WHITE
            pygame.draw.rect(screen, color, (offset_x + j * cell_size, offset_y + i * cell_size, cell_size, cell_size))
            if (i, j) == maze.start:
                pygame.draw.circle(screen, GREEN, (offset_x + j * cell_size + cell_size // 2, offset_y + i * cell_size + cell_size // 2), cell_size // 2 - 5)
            if (i, j) == maze.goal:
                pygame.draw.circle(screen, RED, (offset_x + j * cell_size + cell_size // 2, offset_y + i * cell_size + cell_size // 2), cell_size // 2 - 5)
            if show_solution and maze.solution and (i, j) in maze.solution[1]:
                pygame.draw.circle(screen, BLUE, (offset_x + j * cell_size + cell_size // 2, offset_y + i * cell_size + cell_size // 2), 5)
    pygame.draw.circle(screen, GRAY, (offset_x + player_pos[1] * cell_size + cell_size // 2, offset_y + player_pos[0] * cell_size + cell_size // 2), cell_size // 2 - 5)

def draw_back_button(screen, font):
    back_button = pygame.Rect(5, 5, 100, 20)
    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    back_text = font.render("Volver", True, WHITE)
    text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, text_rect)
    return back_button


if __name__ == "__main__":
    main()
