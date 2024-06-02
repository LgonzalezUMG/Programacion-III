import copy
import sys
import pygame
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import graphviz
import os
import json
from datetime import datetime
from constants import *

# Definir rutas absolutas para los archivos de sonido
current_directory = os.path.dirname(os.path.abspath(__file__))
MUSIC_FILE = os.path.join(current_directory, 'cancioncita.mp3')
WIN_SOUND_FILE = os.path.join(current_directory, 'gana.mp3')
LOSE_SOUND_FILE = os.path.join(current_directory, 'pierde.mp3')
DRAW_SOUND_FILE = os.path.join(current_directory, 'empate.mp3')
GRAPHICS_DIR = os.path.join(current_directory, 'GraficosDePartidas')
HISTORY_FILE = os.path.join(current_directory, 'game_history.json')

# Crear el directorio para gráficos de partidas si no existe
if not os.path.exists(GRAPHICS_DIR):
    os.makedirs(GRAPHICS_DIR)

# --- PYGAME SETUP ---
pygame.init()

# --- SOUND SETUP ---
pygame.mixer.init()
try:
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.set_volume(0.3)  # 30% volume
    pygame.mixer.music.play(-1)  # Loop the background music
except pygame.error as e:
    print(f"Error cargando música de fondo: {e}")
    sys.exit(1)

try:
    win_sound = pygame.mixer.Sound(WIN_SOUND_FILE)
    lose_sound = pygame.mixer.Sound(LOSE_SOUND_FILE)
    draw_sound = pygame.mixer.Sound(DRAW_SOUND_FILE)
except pygame.error as e:
    print(f"Error cargando efectos de sonido: {e}")
    sys.exit(1)

# --- CLASSES ---

class Board:
    def __init__(self, screen=None):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_sqrs = 0
        self.screen = screen

    def final_state(self, show=False):
        '''
            @return 0 si no hay un ganador aún
            @return 1 si el jugador 1 gana
            @return 2 si Glad0s gana
            @return -1 si es un empate
        '''

        # Ganancias verticales
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show and self.screen:
                    self.draw_win_line((col * SQSIZE + SQSIZE // 2, 20), (col * SQSIZE + SQSIZE // 2, HEIGHT - 20))
                return self.squares[0][col]

        # Ganancias horizontales
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show and self.screen:
                    self.draw_win_line((20, row * SQSIZE + SQSIZE // 2), (WIDTH - 20, row * SQSIZE + SQSIZE // 2))
                return self.squares[row][0]

        # Diagonal descendente
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show and self.screen:
                self.draw_win_line((20, 20), (WIDTH - 20, HEIGHT - 20))
            return self.squares[1][1]

        # Diagonal ascendente
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show and self.screen:
                self.draw_win_line((20, HEIGHT - 20), (WIDTH - 20, 20))
            return self.squares[1][1]

        # No hay ganador y el tablero está lleno
        if self.isfull():
            return -1  # Empate

        # No hay ganador aún
        return 0

    def draw_win_line(self, start_pos, end_pos):
        for i in range(len(WIN_COLORS)):
            pygame.draw.line(self.screen, WIN_COLORS[i], start_pos, end_pos, WIN_LINE_WIDTH)

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

    def get_state(self):
        return tuple(map(tuple, self.squares))

    def copy(self):
        board_copy = Board()
        board_copy.squares = np.copy(self.squares)
        board_copy.marked_sqrs = self.marked_sqrs
        return board_copy

class AI:
    def __init__(self, player=2):
        self.player = player
        self.moves = 0  # Contador de movimientos de la IA

    def minimax(self, board, maximizing):
        # Caso terminal
        case = board.final_state()

        # Jugador 1 gana
        if case == 1:
            return 1, None

        # Glad0s gana
        if case == 2:
            return -1, None

        # Empate
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = board.copy()
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = board.copy()
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.player == 2:
            # Minimax algorithm choice
            eval, move = self.minimax(main_board, False)

            print(f'Glad0s ha elegido marcar la casilla en la posición {move} con una evaluación de: {eval}')
            self.moves += 1  # Incrementar el contador de movimientos de Glad0s
            return move
        else:
            # Elección aleatoria
            empty_sqrs = main_board.get_empty_sqrs()
            idx = random.randrange(0, len(empty_sqrs))
            return empty_sqrs[idx]

class Game:
    def __init__(self, screen):
        self.board = Board(screen)
        self.ai = AI()
        self.player = 1  # 1-cruz  #2-círculo
        self.gamemode = 'ai'  # pvp o ai
        self.running = True
        self.screen = screen
        self.show_lines()
        self.moves = []
        self.start_time = datetime.now()  # Guardar la hora de inicio del juego

    def show_lines(self):
        # Fondo
        self.screen.fill(BG_COLOR)

        # Líneas verticales
        for i in range(1, COLS):
            self.screen.blit(v_line_img, (i * SQSIZE - LINE_WIDTH // 2, 0))

        # Líneas horizontales
        for i in range(1, ROWS):
            self.screen.blit(h_line_img, (0, i * SQSIZE - LINE_WIDTH // 2))

    def draw_fig(self, row, col):
        if self.player == 1:
            # Dibujar cruz
            self.screen.blit(x_img, (col * SQSIZE + OFFSET // 2, row * SQSIZE + OFFSET // 2))
        elif self.player == 2:
            # Dibujar círculo
            self.screen.blit(o_img, (col * SQSIZE + OFFSET // 2, row * SQSIZE + OFFSET // 2))

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.moves.append(self.board.get_state())
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        result = self.board.final_state(show=True)
        if result != 0 or self.board.isfull():
            pygame.display.update()
            return True
        return False

    def reset(self):
        self.board = Board(self.screen)
        self.ai.moves = 0  # Reiniciar contador de movimientos de Glad0s
        self.player = 1
        self.running = True
        self.moves = []
        self.show_lines()
        pygame.display.update()  # Actualizar la pantalla después de reiniciar el juego
        self.start_time = datetime.now()  # Reiniciar la hora de inicio del juego

    def show_game_over_dialog(self, winner):
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter

        end_time = datetime.now()
        elapsed_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

        if winner == "Draw":
            message = f"¡Juego terminado!\nHora: {elapsed_time}\nResultado: Empate\nMovimientos Glad0s: {self.ai.moves}\n¿Jugar de nuevo?"
            pygame.mixer.Sound.play(draw_sound)
        else:
            message = f"¡Juego terminado!\nHora: {elapsed_time}\nResultado: {winner} gana!\nMovimientos Glad0s: {self.ai.moves}\n¿Jugar de nuevo?"
            if winner == "Player 1":
                pygame.mixer.Sound.play(win_sound)
            else:
                pygame.mixer.Sound.play(lose_sound)

        response = messagebox.askyesno("Juego terminado", message)
        root.destroy()

        # Detener los sonidos de victoria, derrota y empate
        win_sound.stop()
        lose_sound.stop()
        draw_sound.stop()

        # Guardar historial de la partida en JSON
        self.save_game_history(winner, elapsed_time)

        # Generar y guardar el gráfico del árbol de juego
        self.generate_game_tree_svg(elapsed_time)

        if not response:
            on_closing()

        return response

    def save_game_history(self, winner, end_time):
        result = "Empate"
        if winner == "Player 1":
            result = "Victoria"
        elif winner == "Glad0s":
            result = "Derrota"

        history = {
            "Hora": end_time,
            "Jugador": result,
            "Movimientos Glad0s": self.ai.moves
        }

        try:
            with open(HISTORY_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(history)

        with open(HISTORY_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def generate_game_tree_svg(self, end_time):
        dot = graphviz.Digraph(comment='Árbol del juego Tic Tac Toe')

        for i, state in enumerate(self.moves):
            dot.node(str(i), str(state).replace('),', '),\n'))

        for i in range(len(self.moves) - 1):
            dot.edge(str(i), str(i + 1))

        timestamp = end_time.replace(":", "-").replace(" ", "_")
        filename = os.path.join(GRAPHICS_DIR, f'game_tree_{timestamp}')
        dot.render(filename, format='svg')

    def run(self):
        # --- BUCLE PRINCIPAL ---
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on_closing()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE

                    if self.board.empty_sqr(row, col) and self.running:
                        self.make_move(row, col)

                        if self.isover():
                            self.running = False
                            winner = "Player 1" if self.board.final_state() == 1 else "Glad0s" if self.board.final_state() == 2 else "Draw"
                            play_again = self.show_game_over_dialog(winner)
                            if play_again:
                                self.reset()
                            else:
                                on_closing()

            if self.gamemode == 'ai' and self.player == self.ai.player and self.running:
                row, col = self.ai.eval(self.board)
                self.make_move(row, col)

                if self.isover():
                    self.running = False
                    winner = "Player 1" if self.board.final_state() == 1 else "Glad0s" if self.board.final_state() == 2 else "Draw"
                    play_again = self.show_game_over_dialog(winner)
                    if play_again:
                        self.reset()
                    else:
                        on_closing()

            pygame.display.update()

def main():
    # Crear ventana de Tkinter
    root = tk.Tk()
    root.title("Tic Tac Toe IA")

    def on_closing():
        pygame.mixer.music.stop()
        root.destroy()
        pygame.quit()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un contenedor para el lienzo de pygame
    embed = tk.Frame(root, width=WIDTH, height=HEIGHT)
    embed.pack(side=tk.TOP)

    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    # Inicializar la pantalla de pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game(screen)

    # Crear barra de botones
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM)

    def show_team_members():
        team_root = tk.Toplevel(root)
        team_root.title("Integrantes")
        tk.Label(team_root, text="Luis Eduardo González Alvarado\n9490-22-14408\nSección B\n").pack(pady=10)
        tk.Label(team_root, text="Keily Andrea Tobar Morales\n9490-22-4796\nSección B\n").pack(pady=10)
        tk.Label(team_root, text="Diego Antonio Beteta García \n9490-22-12878\nSección B\n").pack(pady=10)
        tk.Label(team_root, text="Alan Billy Baten Guigui\n9490-22-17906\nSección B\n").pack(pady=10)
        tk.Button(team_root, text="Cerrar", command=team_root.destroy).pack(pady=10)
        team_root.transient(root)
        team_root.grab_set()
        root.wait_window(team_root)

    def show_history():
        try:
            with open(HISTORY_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        history_root = tk.Toplevel(root)
        history_root.title("Historial de Partidas")
        history_root.geometry(f"{WIDTH}x{HEIGHT}")

        tree = ttk.Treeview(history_root, columns=("Hora", "Jugador", "Movimientos"), show="headings")
        tree.heading("Hora", text="Hora")
        tree.heading("Jugador", text="Jugador")
        tree.heading("Movimientos", text="Movimientos")
        tree.pack(fill=tk.BOTH, expand=True)

        for game in data:
            tree.insert("", "end", values=(game["Hora"], game["Jugador"], game["Movimientos Glad0s"]))

    integrantes_button = tk.Button(button_frame, text="Integrantes", command=show_team_members)
    integrantes_button.pack(side=tk.LEFT)

    history_button = tk.Button(button_frame, text="Historial", command=show_history)
    history_button.pack(side=tk.LEFT)

    def show_welcome_message():
        welcome_root = tk.Toplevel(root)
        welcome_root.title("Bienvenido")
        tk.Label(welcome_root, text="Proyecto Final Programación III\n\nUniversidad Mariano Galvez de Guatemala\nSede el Naranjo\n\nSección B\n\n1 de junio de 2024").pack(pady=10)
        tk.Button(welcome_root, text="Comenzar", command=welcome_root.destroy).pack(pady=10)
        welcome_root.transient(root)
        welcome_root.grab_set()
        root.wait_window(welcome_root)
        game.reset()

    # Mostrar mensaje de bienvenida antes de iniciar el juego
    show_welcome_message()

    # Forzar el dibujo inicial del tablero
    game.show_lines()
    pygame.display.update()

    # Ejecutar el juego en un hilo separado
    import threading
    threading.Thread(target=game.run).start()

    # Ejecutar el bucle principal de Tkinter
    root.mainloop()

main()
