import pygame
import random

ANCHO, ALTURA = 600, 600
FILAS, COLUMNAS = 8, 8
TAMAGNO_CUADRADO = ANCHO // COLUMNAS

MARRON_OSCURO = (139, 69, 19)
KHAKI = (240, 230, 140)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
AZUL = (59, 131, 189)
CORONA = pygame.transform.scale(pygame.image.load("corona.jpeg"), (45, 25))

class Piezas:
    RELLENO = 15
    BORDE = 2

    def __init__(self, color, fil, col):
        self.fil = fil
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = TAMAGNO_CUADRADO * self.col + TAMAGNO_CUADRADO // 2
        self.y = TAMAGNO_CUADRADO * self.fil + TAMAGNO_CUADRADO // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radio = TAMAGNO_CUADRADO // 2 - self.RELLENO
        pygame.draw.circle(win, GRIS, (self.x, self.y), radio + self.BORDE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radio)
        if self.king:
            win.blit(CORONA, (self.x - CORONA.get_width() // 2, self.y - CORONA.get_height() // 2))

    def move(self, fil, col):
        self.fil = fil
        self.col = col
        self.calc_pos()

class Tablero:
    def __init__(self):
        self.tablero = []
        self.ROJO_left = self.NEGRO_left = 12
        self.ROJO_Kings = self.NEGRO_kings = 0
        self.crear_tablero()

    def draw_cuadrados(self, win):
        win.fill(KHAKI)
        for fil in range(FILAS):
            for col in range(fil % 2, COLUMNAS, 2):
                pygame.draw.rect(win, MARRON_OSCURO, (col * TAMAGNO_CUADRADO, fil * TAMAGNO_CUADRADO, TAMAGNO_CUADRADO, TAMAGNO_CUADRADO))

    def crear_tablero(self):
        for fil in range(FILAS):
            self.tablero.append([])
            for col in range(COLUMNAS):
                if col % 2 == ((fil + 1) % 2):
                    if fil < 3:
                        self.tablero[fil].append(Piezas(NEGRO, fil, col))
                    elif fil > 4:
                        self.tablero[fil].append(Piezas(ROJO, fil, col))
                    else:
                        self.tablero[fil].append(0)
                else:
                    self.tablero[fil].append(0)

    def draw(self, win):
        self.draw_cuadrados(win)
        for fil in range(FILAS):
            for col in range(COLUMNAS):
                pieza = self.tablero[fil][col]
                if pieza != 0:
                    pieza.draw(win)

    def move(self, pieza, fil, col):
        self.tablero[pieza.fil][pieza.col], self.tablero[fil][col] = self.tablero[fil][col], self.tablero[pieza.fil][pieza.col]
        pieza.move(fil, col)

    def obtener_movimientos_validos(self, pieza):
        movimientos = {}
        fil, col = pieza.fil, pieza.col
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        movimientos.update(self._explorar(pieza, fil, col, direcciones))
        return movimientos

    def _explorar(self, pieza, fil, col, direcciones):
        movimientos = {}
        for dfil, dcol in direcciones:
            f, c = fil + dfil, col + dcol
            if 0 <= f < FILAS and 0 <= c < COLUMNAS:
                casilla_destino = self.tablero[f][c]
                if casilla_destino == 0:
                    # Movimiento simple
                    movimientos[(f, c)] = []
                elif casilla_destino.color != pieza.color:
                    # Detectar salto
                    salto_f, salto_c = f + dfil, c + dcol
                    if (
                        0 <= salto_f < FILAS
                        and 0 <= salto_c < COLUMNAS
                        and self.tablero[salto_f][salto_c] == 0
                    ):
                        # Movimiento de salto
                        movimientos[(salto_f, salto_c)] = [(f, c)]
        return movimientos

class Juego:
    def __init__(self, win):
        self.win = win
        self._init()

    def _init(self):
        self.selected = None
        self.tablero = Tablero()
        self.turn = ROJO
        self.movimientos_validos = {}

    def update(self):
        self.tablero.draw(self.win)
        self.draw_movimientos_validos(self.movimientos_validos)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, fil, col):
        if self.selected:
            result = self._move(fil, col)
            if not result:
                self.selected = None
                self.select(fil, col)
        pieza = self.tablero.tablero[fil][col]
        if pieza != 0 and pieza.color == self.turn:
            self.selected = pieza
            self.movimientos_validos = self.tablero.obtener_movimientos_validos(pieza)
            return True
        return False

    def _move(self, fil, col):
        if (fil, col) in self.movimientos_validos:
            self.tablero.move(self.selected, fil, col)
            if self.movimientos_validos[(fil, col)]:
                for f, c in self.movimientos_validos[(fil, col)]:
                    self.tablero.tablero[f][c] = 0
            # Verificar promoción a reina
            if (self.selected.color == ROJO and fil == 0) or (self.selected.color == NEGRO and fil == FILAS - 1):
                self.selected.make_king()
            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.selected = None
        self.movimientos_validos = {}
        self.turn = NEGRO if self.turn == ROJO else ROJO

    def draw_movimientos_validos(self, movimientos):
        for mov in movimientos:
            fil, col = mov
            pygame.draw.circle(self.win, AZUL, (col * TAMAGNO_CUADRADO + TAMAGNO_CUADRADO // 2, fil * TAMAGNO_CUADRADO + TAMAGNO_CUADRADO // 2), 15)

def get_fil_col_from_mouse(pos):
    x, y = pos
    fil = y // TAMAGNO_CUADRADO
    col = x // TAMAGNO_CUADRADO
    return fil, col

def backtracking(juego):
    movimientos_posibles = {}
    for fil in range(FILAS):
        for col in range(COLUMNAS):
            pieza = juego.tablero.tablero[fil][col]
            if pieza != 0 and pieza.color == NEGRO:
                movimientos_validos = juego.tablero.obtener_movimientos_validos(pieza)
                if movimientos_validos:
                    movimientos_posibles[(fil, col)] = movimientos_validos

    if movimientos_posibles:
        pieza_inicio, movimientos = random.choice(list(movimientos_posibles.items()))
        pieza = juego.tablero.tablero[pieza_inicio[0]][pieza_inicio[1]]
        destino = random.choice(list(movimientos.keys()))
        juego.tablero.move(pieza, destino[0], destino[1])
        for f, c in movimientos[destino]:
            juego.tablero.tablero[f][c] = 0
        # Promoción para piezas negras
        if destino[0] == FILAS - 1:
            pieza.make_king()
        juego.change_turn()

def main():
    pygame.init()
    win = pygame.display.set_mode((ANCHO, ALTURA))
    pygame.display.set_caption("Damas Chinas")
    juego = Juego(win)
    running = True

    while running:
        juego.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fil, col = get_fil_col_from_mouse(pos)
                if not juego.select(fil, col):
                    juego.select(fil, col)
        if juego.turn == NEGRO:
            backtracking(juego)

    pygame.quit()

if __name__ == "__main__":
    main()
