"""
Pac-Man - Versão final revisada (corredores + fantasma mais rápido)
Só foram alterados:
- raio do Pac-Man e do Fantasma para permitir passar nos corredores
- velocidade do fantasma aumentada
- função de vitória separada (win_screen) para mostrar "VOCÊ VENCEU!" sem cair em GAME OVER
"""

import pygame
import sys
import time
import math
import random
from collections import deque

pygame.init()

# -------------- Configurações --------------
WIDTH, HEIGHT = 480, 384
TILE = 24
COLS = WIDTH // TILE
ROWS = HEIGHT // TILE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PYc-Man - Médio")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 20)
BIGFONT = pygame.font.SysFont("consolas", 36)

COLOR_BG = (8, 10, 30)
COLOR_WALL = (16, 60, 160)
COLOR_PELLET = (230, 230, 230)
COLOR_PAC = (250, 220, 40)
COLOR_GHOST = (230, 70, 70)
COLOR_TEXT = (210, 210, 230)

# -------------- Labirinto --------------
raw = [
    "11111111111111111111",
    "1..0...00..00...0..1",
    "1.111.111.11.111.1.1",
    "1.0..0....0....0..01",
    "1.0.11.11111.11.0.01",
    "1....0..0..0..0....1",
    "1.111.11.11.11.111.1",
    "1.0....0....0....0.1",
    "1.0.11.11111.11.0.01",
    "1..0...0..00...0...1",
    "1.111.111.11.111.1.1",
    "1.0....0....0....0.1",
    "1.0.11111.11.111.0.1",
    "1....0.......0.....1",
    "1.111.111111.11111.1",
    "11111111111111111111",
]

maze = []
for row in raw:
    maze.append([1 if ch == "1" else 0 for ch in row])

# -------------- Pellets --------------
def build_pellets():
    return {(x, y) for y in range(ROWS) for x in range(COLS) if maze[y][x] == 0}

pellets = build_pellets()

# -------------- Utilities --------------
def tile_center(tx, ty):
    return tx * TILE + TILE/2, ty * TILE + TILE/2

def px_to_tile(px, py):
    return int(px // TILE), int(py // TILE)

def point_is_wall(px, py):
    tx, ty = px_to_tile(px, py)
    if 0 <= tx < COLS and 0 <= ty < ROWS:
        return maze[ty][tx] == 1
    return True

# -------------- Pac-Man --------------
class Pacman:
    def __init__(self):
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 0:
                    self.tx, self.ty = x, y
                    break
            else:
                continue
            break

        cx, cy = tile_center(self.tx, self.ty)
        self.x = cx
        self.y = cy

        self.radius = TILE//2 - 5   # <<< CORREDORES FUNCIONANDO
        self.speed = 3.0
        self.lives = 3

    def move(self, dx, dy):
        if dx == dy == 0:
            return

        nx = self.x + dx * self.speed
        ny = self.y + dy * self.speed

        r = self.radius - 1
        checks = [
            (nx - r, ny - r), (nx + r, ny - r),
            (nx - r, ny + r), (nx + r, ny + r)
        ]
        for px, py in checks:
            if point_is_wall(px, py):
                return

        self.x = nx
        self.y = ny

    def tile(self):
        return px_to_tile(self.x, self.y)

    def draw(self):
        pygame.draw.circle(screen, COLOR_PAC, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (30,30,30),
                           (int(self.x + self.radius/3), int(self.y - self.radius/3)), 3)

# -------------- Fantasma Vermelho --------------
class RedGhost:
    def __init__(self):
        for y in range(ROWS-1, -1, -1):
            for x in range(COLS-1, -1, -1):
                if maze[y][x] == 0:
                    self.tx, self.ty = x, y
                    break
            else:
                continue
            break

        cx, cy = tile_center(self.tx, self.ty)
        self.x = cx
        self.y = cy

        self.radius = TILE//2 - 5   # <<< MESMO AJUSTE
        self.speed = 3.8            # <<< FANTASMA MAIS RÁPIDO
        self.last_calc = 0
        self.path = []

    def bfs(self, start, goal):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur = queue.popleft()
            if cur == goal:
                break
            cx, cy = cur
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if maze[ny][nx] == 0 and (nx, ny) not in visited:
                        visited[(nx, ny)] = cur
                        queue.append((nx, ny))

        if goal not in visited:
            return []

        path = []
        p = goal
        while p != start:
            path.append(p)
            p = visited[p]
        path.reverse()
        return path

    def update(self, pac_pos):
        now = time.time()
        if now - self.last_calc > 1.0:
            self.last_calc = now
            start = px_to_tile(self.x, self.y)
            goal = px_to_tile(*pac_pos)
            self.path = self.bfs(start, goal)
            if len(self.path) > 2:
                self.path = self.path[:2]

        if self.path:
            tx, ty = self.path[0]
            txc, tyc = tile_center(tx, ty)
            dx = txc - self.x
            dy = tyc - self.y
            dist = math.hypot(dx, dy)
            if dist == 0:
                self.path.pop(0)
                return
            step_x = (dx/dist) * self.speed
            step_y = (dy/dist) * self.speed

            newx = self.x + step_x
            newy = self.y + step_y

            r = self.radius - 1
            pts = [(newx - r, newy - r),(newx + r, newy - r),
                   (newx - r, newy + r),(newx + r, newy + r)]
            for px, py in pts:
                if point_is_wall(px, py):
                    return

            self.x = newx
            self.y = newy

            if abs(self.x - txc) < 3 and abs(self.y - tyc) < 3:
                self.path.pop(0)

    def draw(self):
        pygame.draw.circle(screen, COLOR_GHOST, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255,255,255), (int(self.x - 6), int(self.y - 6)), 3)
        pygame.draw.circle(screen, (255,255,255), (int(self.x + 6), int(self.y - 6)), 3)

# -------------- Draw --------------
def draw_maze():
    screen.fill(COLOR_BG)
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, COLOR_WALL, (x*TILE, y*TILE, TILE, TILE))
            elif (x,y) in pellets:
                cx, cy = tile_center(x, y)
                pygame.draw.circle(screen, COLOR_PELLET, (int(cx), int(cy)), 3)

def draw_hud(score, lives, elapsed):
    screen.blit(FONT.render(f"Pontos: {score}", True, COLOR_TEXT), (8, 6))
    screen.blit(FONT.render(f"Vidas: {lives}", True, COLOR_TEXT), (8, 28))
    screen.blit(FONT.render(f"Tempo: {elapsed:.1f}s", True, COLOR_TEXT), (WIDTH - 150, 6))

# -------------- Start / Game Over --------------
def start_screen():
    while True:
        screen.fill(COLOR_BG)
        t = BIGFONT.render("PYC-MAN", True, COLOR_PAC)
        h = FONT.render("ENTER para iniciar", True, COLOR_TEXT)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 40))
        screen.blit(h, (WIDTH//2 - h.get_width()//2, HEIGHT//2 + 10))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                return

def game_over_screen(score):
    while True:
        screen.fill(COLOR_BG)
        g = BIGFONT.render("GAME OVER", True, COLOR_GHOST)
        s = FONT.render(f"Pontos: {score}", True, COLOR_TEXT)
        p = FONT.render("ENTER reinicia / ESC sai", True, COLOR_TEXT)
        screen.blit(g, (WIDTH//2 - g.get_width()//2, HEIGHT//2 - 50))
        screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2))
        screen.blit(p, (WIDTH//2 - p.get_width()//2, HEIGHT//2 + 40))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN: return True
                if ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

# -------------- Win screen (separada) --------------
def win_screen(score):
    while True:
        screen.fill(COLOR_BG)
        w = BIGFONT.render("VOCÊ VENCEU!", True, COLOR_PAC)
        s = FONT.render(f"Pontos: {score}", True, COLOR_TEXT)
        p = FONT.render("ENTER reinicia / ESC sai", True, COLOR_TEXT)
        screen.blit(w, (WIDTH//2 - w.get_width()//2, HEIGHT//2 - 50))
        screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2))
        screen.blit(p, (WIDTH//2 - p.get_width()//2, HEIGHT//2 + 40))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN: return True
                if ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        clock.tick(30)

# -------------- Main Loop --------------
def game_loop():
    global pellets
    pellets = build_pellets()

    pac = Pacman()
    if pac.tile() in pellets: pellets.remove(pac.tile())

    ghost = RedGhost()
    gtile = px_to_tile(ghost.x, ghost.y)
    if gtile in pellets: pellets.remove(gtile)

    score = 0
    start_time = time.time()
    dx = dy = 0
    running = True

    while running:
        dt = clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  dx, dy = -1, 0
        elif keys[pygame.K_RIGHT]: dx, dy = 1, 0
        elif keys[pygame.K_UP]:    dx, dy = 0, -1
        elif keys[pygame.K_DOWN]:  dx, dy = 0, 1
        else: dx = dy = 0

        pac.move(dx, dy)

        ptx, pty = pac.tile()
        if (ptx, pty) in pellets:
            cx, cy = tile_center(ptx, pty)
            if abs(pac.x - cx) < TILE*0.45 and abs(pac.y - cy) < TILE*0.45:
                pellets.remove((ptx, pty))
                score += 10

        ghost.update((pac.x, pac.y))

        if math.hypot(pac.x - ghost.x, pac.y - ghost.y) < (pac.radius + ghost.radius)*0.75:
            pac.lives -= 1

            # reset pac
            for y in range(ROWS):
                for x in range(COLS):
                    if maze[y][x] == 0:
                        pac.x, pac.y = tile_center(x, y)
                        break
                else: continue
                break

            # reset ghost
            for y in range(ROWS-1, -1, -1):
                for x in range(COLS-1, -1, -1):
                    if maze[y][x] == 0:
                        ghost.x, ghost.y = tile_center(x, y)
                        break
                else: continue
                break

            dx = dy = 0
            time.sleep(0.35)

            if pac.lives <= 0:
                running = False

        draw_maze()
        pac.draw()
        ghost.draw()
        draw_hud(score, pac.lives, time.time() - start_time)
        pygame.display.flip()

        if not pellets:
            # show win screen instead of falling through to game over
            return win_screen(score)

    return game_over_screen(score)

# -------------- Run --------------
if __name__ == "__main__":
    while True:
        pellets = build_pellets()
        start_screen()
        restart = game_loop()
        if not restart:
            break
