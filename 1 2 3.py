import pygame
import random
import os
import sys

pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {"wall": load_image("box.png"), "empty": load_image("grass.png")}
player_image = load_image('mar.png', colorkey=-1)
tile_width = tile_height = 50


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, "."), level_map))


def terminate():
    pygame.quit()
    sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


def start_screen():
    sprite = pygame.sprite.Group()
    image = pygame.sprite.Sprite()
    image.image = load_image("fon.jpg")
    image.image = pygame.transform.scale(image.image, (550, 550))
    image.rect = image.image.get_rect()
    sprite.add(image)
    sprite.draw(screen)

    intro_text = ["ЗАСТАВКА", " ",
                  "Правила игры",
                  "Если в правилах несколько строк, ",
                  "приходится выводить их построчно"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == "@":
                Tile("empty", x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = width // 2 - (target.rect.x + target.rect.w // 2) + sx
        self.dy = height // 2 - (target.rect.y + target.rect.h // 2) + sy


start_screen()
sx = sy = 0
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(load_level("level1.txt"))
run = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sy = 1
            if event.key == pygame.K_UP:
                sy = -1
            if event.key == pygame.K_RIGHT:
                sx = 1
            if event.key == pygame.K_LEFT:
                sx = -1
            run = True
        elif event.type == pygame.KEYUP:
            sx = sy = 0
            run = False
    if run:
        player.update(sx, sy)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()
