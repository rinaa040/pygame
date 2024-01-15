import pygame
from PIL import Image

all_sprites = pygame.sprite.Group()


def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode)
        ret.append(pygame_image)
    return ret


frames = []
for frame in split_animated_gif("сut.gif"):
    frames.append(frame)

print(frames)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, x, y):
        super().__init__(all_sprites)
        self.frames = frames
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        print(self.cur_frame)



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    running = True
    dragon = AnimatedSprite(frames, 50, 50)
    fps = 5
    clock = pygame.time.Clock()

    while running:
        dragon = AnimatedSprite(frames, 50, 50)
        dragon.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
