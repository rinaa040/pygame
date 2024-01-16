import pygame
from PIL import Image


all_sprites = pygame.sprite.Group()


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
for frame in split_animated_gif("сut.gif"):
    frames.append(frame)



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, x, y):
        super().__init__(all_sprites)
        self.frames = frames
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(x, y)

    def update(self, colorkey=None):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))

        # print(self.cur_frame)

