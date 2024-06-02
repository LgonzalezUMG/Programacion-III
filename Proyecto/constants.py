import sys
import pygame
import os

# ---------
# CONSTANTS
# ---------

# --- PIXELS ---

WIDTH = 600
HEIGHT = 600

ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
WIN_LINE_WIDTH = 7
CIRC_WIDTH = 15
CROSS_WIDTH = 20

RADIUS = SQSIZE // 4

OFFSET = 50

# --- COLORS ---

BG_COLOR = (0, 0, 0)  # Black background
WIN_COLORS = [(0, 191, 255), (173, 216, 230), (255, 255, 255), (255, 255, 255), (173, 216, 230), (0, 191, 255)]

# --- IMAGES ---

current_directory = os.path.dirname(os.path.abspath(__file__))
X_IMAGE = os.path.join(current_directory, 'x.jpg')
O_IMAGE = os.path.join(current_directory, 'o.jpg')
V_LINE_IMAGE = os.path.join(current_directory, 'v_line.png')
H_LINE_IMAGE = os.path.join(current_directory, 'h_line.png')

# Initialize images
pygame.init()

def load_image(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image file '{path}' not found.")
    return pygame.image.load(path)

try:
    x_img = load_image(X_IMAGE)
    x_img = pygame.transform.scale(x_img, (SQSIZE - OFFSET, SQSIZE - OFFSET))
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

try:
    o_img = load_image(O_IMAGE)
    o_img = pygame.transform.scale(o_img, (SQSIZE - OFFSET, SQSIZE - OFFSET))
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

try:
    v_line_img = load_image(V_LINE_IMAGE)
    v_line_img = pygame.transform.scale(v_line_img, (LINE_WIDTH, HEIGHT))
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

try:
    h_line_img = load_image(H_LINE_IMAGE)
    h_line_img = pygame.transform.scale(h_line_img, (WIDTH, LINE_WIDTH))
except FileNotFoundError as e:
    print(e)
    sys.exit(1)
