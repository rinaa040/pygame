import pygame
from class_board import Board

class Life(Board):
    def render(self, screen):
        screen.fill((0, 0, 0))
        for i in range(self.height):
            for j in range(self.width):
                if not self.board[i][j]:
                    pygame.draw.rect(screen, "white", (j * self.cell_size + self.top,
                                                       i * self.cell_size + self.left,
                                                       self.cell_size,
                                                       self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, "white", (j * self.cell_size + self.top,
                                                       i * self.cell_size + self.left,
                                                       self.cell_size,
                                                       self.cell_size), 1)
                    pygame.draw.rect(screen, "green", (j * self.cell_size + self.top + 1,
                                                       i * self.cell_size + self.left + 1,
                                                       self.cell_size - 2,
                                                       self.cell_size - 2))

    def on_click(self, cell):
        if not play_mode:
            self.board[cell[1]][cell[0]] = not self.board[cell[1]][cell[0]]

    def next_move(self):
        copy_lst = self.board.copy()
        for i in range(1, self.height):
            for j in range(1, self.width):
                x = list(copy_lst[i - 1:i + 2, j - 1:j + 2])
                x = [y for a in x for y in a].count(1) - self.board[i][j]
                if copy_lst[i][j] == 0 and x == 3:
                    self.board[i][j] = 1
                elif copy_lst[i][j] == 1 and x in (2, 3):
                    self.board[i][j] = 1
                else:
                    self.board[i][j] = 0



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((920, 920))
    board = Life(30, 30)
    running = True
    play_mode = False
    fps = 30
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_mode = not play_mode
            if play_mode:
                board.next_move()

        board.render(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()