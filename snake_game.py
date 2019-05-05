import pyglet
from random import randrange
from pathlib import Path


TILES_DIRECTORY = Path("snake-tiles")
SIZE_IMG = 64  # the smallest part of game pole is 64 x 64 pixels
WIDTH = SIZE_IMG * 12
HEIGHT = SIZE_IMG * 12


class Game_status:
    def __init__(self, batch):
        self.snake_coordinates = [(32, 32), (96, 32), (160, 32)]
        self.snake_course = (1, 0)
        self.foods = []
        self.foods_coordinates = []
        self.snake_body = []
        self.snake_tiles = {}
        sequence_paths_imgs = TILES_DIRECTORY.glob("*.png")
        for path in sequence_paths_imgs:
            self.snake_tiles[path.stem] = pyglet.image.load(path)


game_window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def create_snake(batch):
    """
    function create GUI of snake body with special pictures
    saved in snake_tiles
    """
    game_status.snake_body.clear()
    for num, coordinates in enumerate(game_status.snake_coordinates):
        x, y = coordinates

        # this part create key for tail
        if num == 0:
            next_x, next_y = game_status.snake_coordinates[num + 1]
            key_1 = "tail"

            if next_x > x:
                if abs(next_x - x) == SIZE_IMG:
                    key_2 = "right"
                else:
                    key_2 = "left"
            elif next_x < x:
                if abs(next_x - x) == SIZE_IMG:
                    key_2 = "left"
                else:
                    key_2 = "right"
            elif next_y > y:
                if abs(next_y - y) == SIZE_IMG:
                    key_2 = "top"
                else:
                    key_2 = "bottom"
            elif next_y < y:
                if abs(next_y - y) == SIZE_IMG:
                    key_2 = "bottom"
                else:
                    key_2 = "top"

        # this part create key for head of snake
        elif num == len(game_status.snake_coordinates) - 1:
            previous_x, previous_y = game_status.snake_coordinates[num - 1]
            key_2 = "tongue"

            if previous_x > x:
                if abs(previous_x - x) == SIZE_IMG:
                    key_1 = "right"
                else:
                    key_1 = "left"
            elif previous_x < x:
                if abs(previous_x - x) == SIZE_IMG:
                    key_1 = "left"
                else:
                    key_1 = "right"
            elif previous_y > y:
                if abs(previous_y - y) == SIZE_IMG:
                    key_1 = "top"
                else:
                    key_1 = "bottom"
            elif previous_y < y:
                if abs(previous_y - y) == SIZE_IMG:
                    key_1 = "bottom"
                else:
                    key_1 = "top"

        # this part create key for rest of body between tail and head
        else:
            next_x, next_y = game_status.snake_coordinates[num + 1]
            previous_x, previous_y = game_status.snake_coordinates[num - 1]

            # this part create key for straight part of snake body (up or down)
            if previous_x == x and next_x == x:
                key_1 = "top"
                key_2 = "bottom"

            # this part create key for straight part ofsnakebody(left or right)
            elif previous_y == y and next_y == y:
                key_1 = "left"
                key_2 = "right"

            # this part create key for corner of snake
            else:
                if previous_y == y and previous_x < x:
                    if abs(previous_x - x) == SIZE_IMG:
                        key_1 = "left"
                    else:
                        key_1 = "right"

                    if next_y > y:
                        if abs(next_y - y) == SIZE_IMG:
                            key_2 = "top"
                        else:
                            key_2 = "bottom"
                    elif next_y < y:
                        if abs(next_y - y) == SIZE_IMG:
                            key_2 = "bottom"
                        else:
                            key_2 = "top"

                elif previous_y == y and previous_x > x:
                    if abs(previous_x - x) == SIZE_IMG:
                        key_1 = "right"
                    else:
                        key_1 = "left"

                    if next_y > y:
                        if abs(next_y - y) == SIZE_IMG:
                            key_2 = "top"
                        else:
                            key_2 = "bottom"
                    elif next_y < y:
                        if abs(next_y - y) == SIZE_IMG:
                            key_2 = "bottom"
                        else:
                            key_2 = "top"
                elif previous_x == x and previous_y < y:
                    if abs(previous_y - y) == SIZE_IMG:
                        key_1 = "bottom"
                    else:
                        key_1 = "top"

                    if next_x > x:
                        if abs(next_x - x) == SIZE_IMG:
                            key_2 = "right"
                        else:
                            key_2 = "left"
                    elif next_x < x:
                        if abs(next_x - x) == SIZE_IMG:
                            key_2 = "left"
                        else:
                            key_2 = "right"

                elif previous_x == x and previous_y > y:
                    if abs(previous_y - y) == SIZE_IMG:
                        key_1 = "top"
                    else:
                        key_1 = "bottom"

                    if next_x > x:
                        if abs(next_x - x) == SIZE_IMG:
                            key_2 = "right"
                        else:
                            key_2 = "left"
                    elif next_x < x:
                        if abs(next_x - x) == SIZE_IMG:
                            key_2 = "left"
                        else:
                            key_2 = "right"

        # there I create the whole key for find the right picture in dict
        st_img = game_status.snake_tiles[key_1 + "-" + key_2]
        # last part create sprite
        game_status.snake_body.append(pyglet.sprite.Sprite(st_img,
                                                           x,
                                                           y,
                                                           batch=batch))


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
            x += -x_course * SIZE_IMG
            y += -y_course * SIZE_IMG
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
    if x - SIZE_IMG // 2 <= 0 and x_course == -1:
        x = WIDTH - SIZE_IMG // 2
    elif x + SIZE_IMG // 2 >= WIDTH and x_course == 1:
        x = SIZE_IMG // 2
    else:
        x += x_course * SIZE_IMG

    if y - SIZE_IMG // 2 <= 0 and y_course == -1:
        y = HEIGHT - SIZE_IMG // 2
    elif y + SIZE_IMG // 2 >= HEIGHT and y_course == 1:
        y = SIZE_IMG // 2
    else:
        y += y_course * SIZE_IMG

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

    create_snake(batch)


def move_snake_onkey(key, modifikator):
    if key == pyglet.window.key.UP:
        game_status.snake_course = (0, 1)
    if key == pyglet.window.key.DOWN:
        game_status.snake_course = (0, -1)
    if key == pyglet.window.key.RIGHT:
        game_status.snake_course = (1, 0)
    if key == pyglet.window.key.LEFT:
        game_status.snake_course = (-1, 0)


# img_snake = pyglet.image.load("green_rectangle.png")
img_food = pyglet.image.load("red_apple.png")
center_image(img_food)
batch = pyglet.graphics.Batch()
game_status = Game_status(batch)
img_snake = game_status.snake_tiles["tail-head"]
center_image(img_snake)

for image in game_status.snake_tiles.values():
    center_image(image)


game_window.push_handlers(
    on_draw=draw_window,
    on_key_press=move_snake_onkey,
)

pyglet.clock.schedule_interval(move_snake_interval, 1/4)

if __name__ == "__main__":
    pyglet.app.run()
