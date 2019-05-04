import pyglet
from random import randrange
from pathlib import Path


TILES_DIRECTORY = Path("snake-tiles")
SIZE_POLE = 64  # the smallest part of game pole is 64 x 64 pixels
WIDTH = SIZE_POLE * 12
HEIGHT = SIZE_POLE * 12


class Game_status:
    def __init__(self, batch):
        self.snake_coordinates = [(32, 32), (96, 32), (160, 32)]
        self.snake_course = (1, 0)
        self.foods = []
        self.foods_coordinates = []
        self.snake_body = []
        for x, y in self.snake_coordinates:
            self.snake_body.append(pyglet.sprite.Sprite(img_snake,
                                                        x,
                                                        y,
                                                        batch=batch))


game_window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def draw_window():
    game_window.clear()
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    batch.draw()


def create_food(batch):
    x_food = randrange(32, WIDTH, 64)
    y_food = randrange(32, HEIGHT, 64)
    while (x_food, y_food) in game_status.snake_coordinates:
        x_food = randrange(32, WIDTH, 64)
        y_food = randrange(32, HEIGHT, 64)

    game_status.foods_coordinates.append((x_food, y_food))
    game_status.foods.append(pyglet.sprite.Sprite(img_food,
                                                  x_food,
                                                  y_food,
                                                  batch=batch))


def eat_food(batch):
    for coordinates in game_status.foods_coordinates:
        if game_status.snake_coordinates[-1] == coordinates:
            x, y = game_status.snake_coordinates[0]
            x_course, y_course = game_status.snake_course
            x += -x_course * SIZE_POLE
            y += -y_course * SIZE_POLE
            game_status.snake_coordinates.insert(0, (x, y))
            game_status.snake_body.insert(0,
                                          pyglet.sprite.Sprite(img_snake,
                                                               x,
                                                               y,
                                                               batch=batch))
            game_status.foods_coordinates.clear()
            game_status.foods.clear()


def move_snake_interval(dt):
    """
    Function which set coordinates of snake.
    Also check position of snake and whenever snake is
    out of game window than return snake back to the game
    window.
    At the end of function is loop enumerate for
    move snake with new coordinates.
    """

    x, y = game_status.snake_coordinates[-1]
    x_course, y_course = game_status.snake_course

    # Conditions which ensured that snake will not go out of window
    if x - SIZE_POLE // 2 <= 0 and x_course == -1:
        x = WIDTH - SIZE_POLE // 2
    elif x + SIZE_POLE // 2 >= WIDTH and x_course == 1:
        x = SIZE_POLE // 2
    else:
        x += x_course * SIZE_POLE

    if y - SIZE_POLE // 2 <= 0 and y_course == -1:
        y = HEIGHT - SIZE_POLE // 2
    elif y + SIZE_POLE // 2 >= HEIGHT and y_course == 1:
        y = SIZE_POLE // 2
    else:
        y += y_course * SIZE_POLE

    # if snake hit itself function will stop
    if (x, y) in game_status.snake_coordinates:
        pyglet.clock.unschedule(move_snake_interval)
        print("narazil jsi do hada")
    else:
        game_status.snake_coordinates.append((x, y))
        del game_status.snake_coordinates[0]
        print(game_status.snake_coordinates)
        eat_food(batch)

        for i, sprite in enumerate(game_status.snake_body):
            sprite.x, sprite.y = game_status.snake_coordinates[i]

    if not game_status.foods_coordinates:
        create_food(batch)


def move_snake_onkey(key, modifikator):
    if key == pyglet.window.key.UP:
        game_status.snake_course = (0, 1)
    if key == pyglet.window.key.DOWN:
        game_status.snake_course = (0, -1)
    if key == pyglet.window.key.RIGHT:
        game_status.snake_course = (1, 0)
    if key == pyglet.window.key.LEFT:
        game_status.snake_course = (-1, 0)


snake_tiles = {}
sequence_paths_imgs = TILES_DIRECTORY.glob("*.png")
for path in sequence_paths_imgs:
    snake_tiles[path.stem] = pyglet.image.load(path)
print(snake_tiles)

# img_snake = pyglet.image.load("green_rectangle.png")
img_snake = snake_tiles["tail-head"]
img_food = pyglet.image.load("red_apple.png")
center_image(img_snake)
center_image(img_food)
batch = pyglet.graphics.Batch()
game_status = Game_status(batch)


game_window.push_handlers(
    on_draw=draw_window,
    on_key_press=move_snake_onkey,
)

pyglet.clock.schedule_interval(move_snake_interval, 1/4)

if __name__ == "__main__":
    pyglet.app.run()
