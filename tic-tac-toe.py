import pygame
import random


# Размеры игрового поля
SCREEN_SIDE = 600

# Цвет фона
BOARD_BACKGROUND_COLOR = (255, 255, 255)

# Количество клеток
COUNT_CELL = 3

# Размер клетки
GRID_SIZE = SCREEN_SIDE // COUNT_CELL

# Цвет объектов
OBJECT_COLOR = (255, 20, 147)

# Цвет линии
LINE_COLOR = (0, 105, 180)

# Толщина линии
LINE_THICKNESS = 5

# Настройка игрового поля
screen = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))

# Заголовок окна игрового поля:
pygame.display.set_caption('Крестики и нолики')

# Логотип в игре

# Создание поверхности для иконки
icon_size = (64, 64)
icon_surface = pygame.Surface(icon_size, pygame.SRCALPHA)

# Рисуем "нолик" на поверхности иконки
circle_position = (32, 32)  # Центр круга
circle_radius = 20  # Радиус круга
pygame.draw.circle(icon_surface, OBJECT_COLOR, 
                   circle_position, circle_radius, 5)  # 5 - ширина контура

# Рисуем "крестик"
cross_size = 15  # Длина сторон крестика
pygame.draw.line(icon_surface, OBJECT_COLOR, 
                 (32 - cross_size, 32 - cross_size), 
                 (32 + cross_size, 32 + cross_size), 5)  # Первая диагональ
pygame.draw.line(icon_surface, OBJECT_COLOR, 
                 (32 - cross_size, 32 + cross_size),
                 (32 + cross_size, 32 - cross_size), 5)  # Вторая диагональ

# Установка иконки окна
pygame.display.set_icon(icon_surface)

# Цвета фигур
COLORS = ((24, 222, 239), (142, 244, 32), (244, 135, 64), (245, 189, 222),)


class Line:
    """Класс линии"""

    def __init__(self):
        self.body_color = LINE_COLOR

    def draw(self):
        """Метод отрисовки"""
        for i in range(GRID_SIZE, SCREEN_SIDE, GRID_SIZE):
            pygame.draw.line(screen,
                             self.body_color,
                             (0, i), (SCREEN_SIDE, i),
                             LINE_THICKNESS
                             )
            pygame.draw.line(screen,
                             self.body_color,
                             (i, 0), (i, SCREEN_SIDE),
                             LINE_THICKNESS
                             )


class GameObject:
    """Базовый класс"""

    def __init__(self):
        self.body_color = random_color()
        self.positions = [
            [0 for _ in range(COUNT_CELL)] for _ in range(COUNT_CELL)
        ]


class Circle(GameObject):
    """Крестик"""

    def draw(self):
        """Метод отрисовки"""
        for y in range(COUNT_CELL):
            for x in range(COUNT_CELL):
                position = self.positions[y][x]
                if position == 1:
                    position_x = x * GRID_SIZE + GRID_SIZE // 2
                    position_y = y * GRID_SIZE + GRID_SIZE // 2
                    position = (position_x, position_y)
                    pygame.draw.circle(screen,
                                       self.body_color, position,
                                       GRID_SIZE // 3, width=LINE_THICKNESS
                                       )


class Cross(GameObject):
    """Крестик"""

    def draw(self):
        """Метод отрисовки"""
        for y in range(COUNT_CELL):
            for x in range(COUNT_CELL):
                position = self.positions[y][x]
                if position == 1:
                    position_x = x * GRID_SIZE + GRID_SIZE // 2
                    position_y = y * GRID_SIZE + GRID_SIZE // 2
                    position_x_start = (position_x - GRID_SIZE // 2) + 10
                    position_y_start = (position_y - GRID_SIZE // 2) + 10
                    position_x_end = (position_x + GRID_SIZE // 2) - 10
                    position_y_end = (position_y + GRID_SIZE // 2) - 10
                    pygame.draw.line(screen,
                                 self.body_color,
                                     (position_x_start, position_y_start),
                                     (position_x_end, position_y_end),
                                     LINE_THICKNESS
                                 )
                    pygame.draw.line(screen,
                                 self.body_color,
                                     (position_x_start, position_y_end),
                                     (position_x_end, position_y_start),
                                     LINE_THICKNESS
                                 )


def change_positions(positions, grid_x, grid_y, another_positions):
    """Функция смены значения в координатах отрисовки"""
    if positions[grid_y][grid_x] == 0:
        positions[grid_y][grid_x] = 1
        another_positions[grid_y][grid_x] = -1


def check_victory(positions):
    """Функция проверки победы"""
    for row in positions:
        if all(cell == 1 for cell in row):
            return True

    for x in range(COUNT_CELL):
        if all(positions[y][x] == 1 for y in range(COUNT_CELL)):
            return True

    if all(positions[i][i] == 1 for i in range(COUNT_CELL)):
        return True

    if all(positions[i][COUNT_CELL - 1 - i] == 1 for i in range(COUNT_CELL)):
        return True

    return False


def check_positions(positions):
    """Функция проверки на пустые клетки"""
    for row in positions:
        if any(cell == 0 for cell in row):
            return False
    return True


def display_winner(winner):
    """Функция для отображения сообщения о победе"""
    font = pygame.font.Font(None, 74)
    text = font.render(f'{winner} победил!', True, (0, 255, 0))
    if not winner:
        text = font.render('Ничья :(', True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_SIDE // 2, SCREEN_SIDE // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(1000)


def random_color():
    """Функция, возвращающая случайный цвет из предопределенного списка"""
    return random.choice(COLORS)


def main():
    """Main"""
    pygame.init()
    lines = Line()
    circle = Circle()
    cross = Cross()
    # Очередь(0 - нолик, 1 - крестик)
    queue = 0
    # Проверка победы
    win = False

    running = True
    while running:

        screen.fill(BOARD_BACKGROUND_COLOR)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Получаем координаты в массиве с отрисовкой
                # при нажатии на клетку
                x, y = event.pos
                grid_x = x // GRID_SIZE
                grid_y = y // GRID_SIZE

                # В массиве объекта меняем значение на отрисовку,
                # а в массиве другого объекта меняем значение,
                # что клетка занята. Затем проверяем победу.
                if queue == 0:
                    change_positions(circle.positions, grid_x, grid_y,
                                     cross.positions)
                    win = check_victory(circle.positions)
                    if win:
                        display_winner("Кружочки")
                    queue = 1
                else:
                    change_positions(cross.positions, grid_x, grid_y,
                                     circle.positions)
                    win = check_victory(cross.positions)
                    if win:
                        display_winner("Крестики")
                    queue = 0
        if win:
            circle = Circle()
            cross = Cross()
        elif check_positions(circle.positions):
            display_winner(win)
            circle = Circle()
            cross = Cross()

        lines.draw()
        circle.draw()
        cross.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
