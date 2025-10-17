import pygame
import numpy as np


# Клеточный автомат - Игра "Жизнь"
class GameLife:

    def __init__(self, width=700, height=700, cell_size=14, fps=15,
                 default_color=(255, 255, 255),
                 alive_color=(0, 0, 0),
                 grid_color=(200, 200, 200)):

        # Инициализация
        pygame.init()

        # Длина и ширина поля
        self.width = width
        self.height = height

        # Размеры границ и клеток
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size

        # Основные цвета
        self.default_color = default_color
        self.grid_color = grid_color
        self.alive_color = alive_color

        # Отрисовка и название
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

        # Матрица состояний клеток (0 — мёртвая, 1 — живая)
        self.cells = np.zeros((self.rows, self.cols), dtype=np.uint8)

        # Состояния игры
        self.flag_running = False
        self.flag_starting = False
        self.flag_drawing = False

    def draw_field(self):
        """
        Отрисовка поля
        """

        # Отрисовка мертвых клеток
        self.screen.fill(self.default_color)

        # Отрисовка живых клеток
        alive = np.argwhere(self.cells == 1)
        for r, c in alive:
            pygame.draw.rect(self.screen,
                             self.alive_color,
                             (c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))

        # Линии сетки
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

    def toggle_cell(self, pos, value=None):
        """
        Изменение состояния клетки
        """

        # Положение клетки
        x, y = pos
        c = x // self.cell_size
        r = y // self.cell_size

        # Изменение значения клетки
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if value is None:
                self.cells[r, c] = 1 - self.cells[r, c] # инверсия
            else:
                self.cells[r, c] = value # явное значение

    def clear_cells(self):
        """
        Обнуление поля
        """
        self.cells.fill(0)

    def create_next_generation(self):
        """
        Вычисление следующего поколения
        """
        cls = self.cells

        # Подсчёт соседей
        neighbors = sum(np.roll(np.roll(cls, i, axis=0), j, axis=1)
                        for i in range(-1, 2)
                        for j in range(-1, 2)
                        if not (i == 0 and j == 0))

        # Правила жизни
        birth = (neighbors == 3) & (cls == 0) # условие для рождения
        survive = ((neighbors == 2) | (neighbors == 3)) & (cls == 1) # условие для выживания
        self.clear_cells() # обнуление
        self.cells[birth | survive] = 1 # логическая маска

    def start_game(self):
        """
        Запуск и перезапуск игры
        """

        if not self.flag_starting:
            self.flag_running = True
            self.flag_starting = True
        else:
            self.clear_cells()
            self.flag_running = False
            self.flag_starting = False

    def run(self):
        """
        Ход игры
        """
        clock = pygame.time.Clock()

        # Основной процесс игры
        while True:
            for event in pygame.event.get():

                # Выход
                if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    pygame.quit()
                    return

                # Пауза или продолжить
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.flag_running = not self.flag_running

                # Запуск или перезапуск
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.start_game()

                # Закрашивание клеток
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.flag_drawing = True
                    self.toggle_cell(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.flag_drawing = False

                elif event.type == pygame.MOUSEMOTION and self.flag_drawing:
                    self.toggle_cell(event.pos, 1)

            # Следующее поколение
            if self.flag_running:
                self.create_next_generation()

            # Отрисовка поля
            self.draw_field()
            pygame.display.flip()
            clock.tick(self.fps)
