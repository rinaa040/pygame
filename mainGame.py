import pygame
import sys
import os
import random as rd
from PIL import Image

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.music.load("again.mp3")
pygame.mixer.music.play(-1)
s = pygame.mixer.Sound("cut_sound.wav")
size = width, height = 250, 400
screen = pygame.display.set_mode(size)
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
result_group = pygame.sprite.Group()

fps = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def split_animated_gif(gif_file_path, colorkey=None):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode)
        if colorkey is not None:
            pygame_image = pygame_image.convert()
            if colorkey == -1:
                colorkey = pygame_image.get_at((0, 0))
            pygame_image.set_colorkey(colorkey)
        else:
            pygame_image = pygame_image.convert_alpha()
        ret.append(pygame_image)
    return ret


frames = []
for frame in split_animated_gif("cut1.gif"):
    frames.append(frame)

tile_images = {
    'mess': load_image('grass.jpg'),
    'lawn': load_image('good_grass.jpg'),
    'flower': load_image('flower.jpg'),
    'box': load_image('grass_box.jpg')
}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Result(pygame.sprite.Sprite):
    def __init__(self, count):
        super().__init__(result_group, all_sprites)
        self.count = count
        self.image = load_image('result.jpg')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect().move(0, 0)

    def display(self):
        font = pygame.font.Font("7fonts.ru_Sniglet.ttf", 60)
        textSurf = font.render(str(self.count), 1, (233, 174, 126))
        W = textSurf.get_width()
        H = textSurf.get_height()
        self.image.blit(textSurf, [width / 2 - W / 2, height / 2 - 0.2 * H])


class Player(pygame.sprite.Sprite):
    def __init__(self, frames, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = self.start_x = pos_x
        self.pos_y = self.start_y = pos_y
        self.frames = frames
        self.cur_frame = 0
        self.angle = 0
        self.cur_direction = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)

    def start_position(self):
        self.pos_x = self.start_x
        self.pos_y = self.start_y
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)
        self.cur_direction = 0

    def update(self, colorkey=None):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))
        if self.cur_direction == 0:
            self.image = pygame.transform.rotate(self.image, 0)
        if self.cur_direction == 1:
            self.image = pygame.transform.rotate(self.image, 270)
        if self.cur_direction == 2:
            self.image = pygame.transform.rotate(self.image, 180)
        if self.cur_direction == 3:
            self.image = pygame.transform.rotate(self.image, 90)

    def move_up(self):
        self.cur_direction = 0
        count = self.pos_y + 1
        # pygame.mixer.music.set_volume(0.5)
        s.play()
        for i in range(count):
            self.image = pygame.transform.rotate(self.image, 0)
            if self.rect.collidelist(collided_tiles) != -1:
                self.pos_y += 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                self.image = pygame.transform.rotate(self.image, 0)
                break
            if self.pos_y == 0:
                break
            else:
                self.pos_y -= 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = load_image('good_grass.jpg')
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = pygame.transform.scale(
                    uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 0)

    def move_down(self, level_y):
        self.cur_direction = 2
        count = level_y - self.pos_y + 1
        # pygame.mixer.music.set_volume(0.5)
        s.play()
        for i in range(count):
            self.image = pygame.transform.rotate(self.image, 180)
            if self.rect.collidelist(collided_tiles) != -1:
                self.pos_y -= 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                self.image = pygame.transform.rotate(self.image, 180)
                break
            if self.pos_y == level_y:
                break
            else:
                self.pos_y += 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = load_image('good_grass.jpg')
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = pygame.transform.scale(
                    uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 180)

    def move_right(self, level_x):
        self.cur_direction = 1
        count = level_x - self.pos_x + 1
        # pygame.mixer.music.set_volume(0.5)
        s.play()
        for i in range(count):
            if self.rect.collidelist(collided_tiles) != -1:
                self.pos_x -= 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                break
            if self.pos_x == level_x:
                break
            else:
                self.pos_x += 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = load_image('good_grass.jpg')
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = pygame.transform.scale(
                    uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image, (50, 50))

    def move_left(self):
        self.cur_direction = 3
        count = self.pos_x + 1
        # pygame.mixer.music.set_volume(0.5)
        s.play()
        for i in range(count):
            if self.rect.collidelist(collided_tiles) != -1:
                self.pos_x += 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                break
            if self.pos_x == 0:
                break
            else:
                self.pos_x -= 1
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x, tile_height * self.pos_y)
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = load_image('good_grass.jpg')
                uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image = pygame.transform.scale(
                    uncollided_tiles[self.rect.collidelist(uncollided_tiles)].image, (50, 50))


def generate_level(level):
    new_player, x, y = None, None, None
    tp = rd.choice([True, False])
    tp2 = rd.choice([True, False])
    collided = []
    uncollided = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                uncollided.append(Tile('mess', x, y))
            elif level[y][x] == '#':
                collided.append(Tile('box', x, y))
            elif level[y][x] == '*':
                collided.append(Tile('flower', x, y))
            elif level[y][x] == '@':
                uncollided.append(Tile('lawn', x, y))
                px = x
                py = y
    new_player = Player(frames, px, py)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, collided, uncollided


def load_level(filename):
    filename = filename
    house_map = []
    house_width = 5
    house_height = 8
    objects = ['#', '*']

    high_block_position = rd.randint(1, 2)
    for i in range(house_height):
        s = []
        for j in range(house_width):
            s.append('.')
        house_map.append(s)

    low_block_coord = rd.randint(0, house_width - 2)
    high_block_coord = rd.randint(0, house_width - 2)
    stuff_coord1 = rd.randint(0, house_width - 1)
    stuff_coord2 = rd.choice([0, house_width - 1])
    player_coord = rd.randint(0, house_height - 1), rd.randint(0, house_width - 1)
    if high_block_position == 1:
        house_map[0][high_block_coord] = rd.choice(objects)
        house_map[0][high_block_coord + 1] = rd.choice(objects)
        house_map[1][high_block_coord] = rd.choice(objects)
        house_map[1][high_block_coord + 1] = rd.choice(objects)

        house_map[3][stuff_coord1] = rd.choice(objects)
        house_map[2][house_width - stuff_coord1 - 1] = rd.choice(objects)
    if high_block_position == 2:
        house_map[2][high_block_coord] = rd.choice(objects)
        house_map[2][high_block_coord + 1] = rd.choice(objects)
        house_map[3][high_block_coord] = rd.choice(objects)
        house_map[3][high_block_coord + 1] = rd.choice(objects)

        house_map[0][stuff_coord1] = rd.choice(objects)
        house_map[1][house_width - stuff_coord1 - 1] = rd.choice(objects)

    for i in range(1, 4):
        house_map[house_height - i][low_block_coord] = rd.choice(objects)
        house_map[house_height - i][low_block_coord + 1] = rd.choice(objects)

    if house_map[7][stuff_coord2] == '.':
        house_map[7][stuff_coord2] = rd.choice(objects)
    else:
        stuff_coord2 = rd.randint(0, house_width - 1)
        house_map[7][stuff_coord2] = rd.choice(objects)

    if house_map[player_coord[0]][player_coord[1]] == '.':
        house_map[player_coord[0]][player_coord[1]] = '@'
    else:
        player_coord = rd.randint(0, house_height - 1), rd.randint(0, house_width - 1)
        house_map[player_coord[0]][player_coord[1]] = '@'

    with open(filename, 'w') as mapFile:
        for i in range(len(house_map)):
            house_map[i] = ''.join(house_map[i])
            mapFile.write(house_map[i] + '\n')

    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = 5
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player, level_x, level_y, collided_tiles, uncollided_tiles = generate_level(load_level('field.txt'))


def back(uncollided_tiles):
    for i in range(len(uncollided_tiles)):
        uncollided_tiles[i].image = load_image('grass.jpg')
        uncollided_tiles[i].image = pygame.transform.scale(
            uncollided_tiles[i].image, (50, 50))
    return uncollided_tiles


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    rules = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and not flag:
                screen.blit(rules, (0, 0))
                flag = True
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and flag:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


start_screen()
running = True
count_maps = 0
# generate_level(load_level('field.txt'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            if event.key == pygame.K_DOWN:
                player.move_down(level_y)
            if event.key == pygame.K_RIGHT:
                player.move_right(level_x)
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                back(uncollided_tiles)
                player.start_position()
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                count_maps += 1
                player, level_x, level_y, collided_tiles, uncollided_tiles = generate_level(load_level('field.txt'))
            if event.key == pygame.K_SPACE:
                result = Result(count_maps)
                result.display()
    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(40)
    pygame.display.flip()

pygame.quit()
