import pygame
import sys
import os
import random as rd

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

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


tile_images = {
    'door1': load_image('door1.jpg'),
    'mess': load_image('grass.jpg'),
    'lawn': load_image('good_grass.jpg'),
    'flower': load_image('flower.jpg'),
    'window': load_image('window.png'),
    'box': load_image('grass_box.jpg')
}
player_image = load_image('cut.png')
player_image = pygame.transform.scale(player_image, (50, 50))

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)

    def move(self):
        self.pos_x += 1
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)
        print(tile_width * self.pos_x, tile_height * self.pos_y)
        print(2)



def generate_level(level):
    new_player, x, y = None, None, None
    tp = rd.choice([True, False])
    tp2 = rd.choice([True, False])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('mess', x, y)
            elif level[y][x] == '#':
                Tile('box', x, y)
            elif level[y][x] == '*':
                Tile('flower', x, y)
            elif level[y][x] == '@':
                Tile('lawn', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
    filename = filename
    house_map = []
    house_width = 5
    house_height = 8
    objects = ['#', '*']

    window_position = rd.randint(1, 2)
    for i in range(house_height):
        s = []
        for j in range(house_width):
            s.append('.')
        house_map.append(s)

    door_coord = rd.randint(0, house_width - 2)
    window_coord = rd.randint(0, house_width - 2)
    stuff_coord1 = rd.randint(0, house_width - 1)
    stuff_coord2 = rd.randint(0, house_width - 1)
    player_coord = rd.randint(0, house_height - 1), rd.randint(0, house_width - 1)
    if window_position == 1:
        house_map[0][window_coord] = '#'
        house_map[0][window_coord + 1] = '*'
        house_map[1][window_coord] = '*'
        house_map[1][window_coord + 1] = '#'

        house_map[3][stuff_coord1] = '*'
    if window_position == 2:
        house_map[2][window_coord] = '#'
        house_map[2][window_coord + 1] = '*'
        house_map[3][window_coord] = '*'
        house_map[3][window_coord + 1] = '#'

        house_map[0][stuff_coord1] = '#'

    for i in range(1, 4):
        house_map[house_height - i][door_coord] = '#'
        house_map[house_height - i][door_coord + 1] = '#'

    house_map[7][stuff_coord2] = '#'

    if house_map[player_coord[0]][player_coord[1]] == '.':
        house_map[player_coord[0]][player_coord[1]] = '@'
    else:
        player_coord = rd.randint(0, house_height - 1), rd.randint(0, house_width - 1)
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
    print(list(map(lambda x: x.ljust(max_width, '.'), level_map)))
    print(7)
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player, level_x, level_y = generate_level(load_level('field.txt'))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)




class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


start_screen()
camera = Camera()
running = True
play_mode = False
#generate_level(load_level('field.txt'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.move()
                print(player)

    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick()
    pygame.display.flip()
pygame.quit()
