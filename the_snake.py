from random import randrange

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self) -> None:
        """
        Method initializes game object.
        Default attributes: position, body_color.
        """
        self.position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE
        )
        self.body_color = None

    def draw(self) -> None:
        """Method for drawing object. Contains nothing."""
        pass


class Apple(GameObject):
    """Class for apple game object. Inherit from GameObject class."""

    def __init__(self) -> None:
        """
        Method initializes apple game object.
        Position attribute is set randomly.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def draw(self) -> None:
        """Method draws square apple on the screen."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @staticmethod
    def randomize_position() -> tuple:
        """
        Method generates random position on game grid.
        Takes nothing.
        Return the tuple of random integer based on screen width and height
        and grid size.
        """
        random_position = (
            randrange(0, SCREEN_WIDTH - GRID_SIZE + 1, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT - GRID_SIZE + 1, GRID_SIZE)
        )
        return random_position


def handle_keys(game_object) -> None:
    """
    Function tracks keys pressed by user
    and set game object next direction attribute.
    """
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


class Snake(GameObject):
    """
    Class for snake object.
    Inherit from GameObject class.
    """

    def __init__(self) -> None:
        """
        Method initializes snake game object.
        Start move direction - right.
        """
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self) -> None:
        """
        Method set next step direction
        depending on keys pressed by user.
        """
        handle_keys(self)
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position: tuple) -> bool:
        """
        Method moves snake game object.
        Takes apple position.
        Return bool value indicating whether snake ate apple.
        """
        # Calculating new snake position.
        horizon_coord = self.position[0] + GRID_SIZE * self.direction[0]
        vertical_coord = self.position[1] + GRID_SIZE * self.direction[1]
        # Checking if snake new position out the screen.
        # Then snake apear from opposite side of screen.
        if horizon_coord >= SCREEN_WIDTH:
            horizon_coord = 0
        elif horizon_coord < 0:
            horizon_coord = SCREEN_WIDTH
        if vertical_coord >= SCREEN_HEIGHT:
            vertical_coord = 0
        elif vertical_coord < 0:
            vertical_coord = SCREEN_HEIGHT

        self.position = (
            horizon_coord,
            vertical_coord
        )
        self.positions.insert(0, self.position)
        # Checking if snake eat apple.
        if self.position != apple_position:
            self.last = self.positions.pop(-1)
            is_snake_eat_apple = False
        else:
            is_snake_eat_apple = True
            self.length += 1
        # Checking if snake touch itself.
        if (
                self.position in self.positions[1:]
                or self.length == GRID_WIDTH * GRID_HEIGHT
        ):
            self.reset()
        return is_snake_eat_apple

    def get_head_position(self) -> tuple:
        """Method returns snake head position."""
        return self.positions[0]

    def reset(self) -> None:
        """
        Method sets snake game object to its initial state.
        Also deletes snake figure from screen with draw method.
        """
        self.draw(reset=True)
        Snake.__init__(self)

    def draw(self, reset=False) -> None:
        """
        Method draws snake game object.
        If reset is true, snake figure is deleted from screen.
        """
        if reset:
            for position in self.positions:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        else:
            for position in self.positions[:-1]:
                rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            # Drawing snake head
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

            # Delete last snake cell
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """Main process function."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SPEED)
        snake.update_direction()
        is_snake_eat_apple = snake.move(apple.position)
        if is_snake_eat_apple:
            apple.__init__()
            while apple.position in snake.positions:
                # If apple position falls into one of the snake positions
                # then position is selected again.
                apple.position = apple.randomize_position()


if __name__ == '__main__':
    main()
