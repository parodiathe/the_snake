from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POINT = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
GRID_POINT = (GRID_SIZE, GRID_SIZE)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 6

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс объекта игры"""

    def init(self, body_color=None):
        """Инициализация базовых атрибутов"""
        self.position = CENTER_POINT
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        Этот метод должен определять,
        как объект будет отрисовываться на экране..
        """
        pass


class Apple(GameObject):
    """Класс наследник - яблоко"""

    def init(self):
        """Инициализация базовых атрибутов"""
        super().init(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Рандомайзер позиции"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Переопределённый метод для отрисовки"""
        rect = pygame.Rect(self.position, GRID_POINT)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс наследник - змея"""

    positions = []

    def init(self):
        """Инициализация базовых атрибутов"""
        super().init(SNAKE_COLOR)
        self.next_direction = None
        self.last = None
        self.length = 1
        self.reset()
        self.direction = RIGHT

    def draw(self):
        """Переопределённый метод для отрисовки"""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(), GRID_POINT)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, GRID_POINT)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновить направление"""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Передвинуть змейку"""
        head_x, head_y = self.get_head_position()
        x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        if (x, y) in self.positions[2:]:
            self.reset()
        else:
            if self.length == len(self.positions):
                self.last = self.positions.pop()

            self.positions.insert(0, (x, y))

    def get_head_position(self):
        """Получить головную точку"""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку до начальной позиции"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.next_direction = None
        self.last = None
        self.length = 1
        self.positions = [CENTER_POINT]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object):
    """Обработчик кнопок"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
...
