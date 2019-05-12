import pyglet
from random import randrange, choice
from pathlib import Path


TILES_DIRECTORY = Path("snake-tiles")
SIZE_IMG = 64  # the smallest part of game pole is 64 x 64 pixels
WIDTH = SIZE_IMG * 12
HEIGHT = SIZE_IMG * 12


class Game_status:
    def __init__(self, batch):
        self.lifes = 1
        self.score = 0
        self.speed = 1/4
        self.speed_coeficient = 1/4
        self.snake_coordinates = [(32, 32), (96, 32), (160, 32)]
        self.snake_course = (1, 0)
        self.health_food = []
        self.health_coordinates = []
        self.poison_food = []
        self.poison_coordinates = []
        self.compost = []
        self.compost_coordinates = []
        self.snake_body = []
        self.snake_tiles = {}
        self.label_game_over = None
        self.label_lifes = None
        self.label_score = None
        sequence_paths_imgs = TILES_DIRECTORY.glob("*.png")
        for path in sequence_paths_imgs:
            self.snake_tiles[path.stem] = pyglet.image.load(path)

    def create_snake(self, batch):
        """
        Method create GUI of snake body with special pictures
        saved in snake_tiles
        """
        self.snake_body.clear()
        for num, coordinates in enumerate(self.snake_coordinates):
            x, y = coordinates

            # this part create key for tail
            if num == 0:
                next_x, next_y = self.snake_coordinates[num + 1]
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
            elif num == len(self.snake_coordinates) - 1:
                previous_x, previous_y = self.snake_coordinates[num - 1]
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
                next_x, next_y = self.snake_coordinates[num + 1]
                previous_x, previous_y = self.snake_coordinates[num - 1]

                # this part create key for straight part of
                # snake body (up or down)
                if previous_x == x and next_x == x:
                    key_1 = "top"
                    key_2 = "bottom"

                # this part create key for straight part
                # of snake body(left or right)
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
            st_img = self.snake_tiles[key_1 + "-" + key_2]
            # last part create sprite
            self.snake_body.append(pyglet.sprite.Sprite(st_img,
                                                        x,
                                                        y,
                                                        batch=batch))


game_window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def draw_window():
    """
    Function draws objects on screen.
    Labels and pictures.
    """
    game_window.clear()
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    batch.draw()
    heart.draw()
    if game_status.label_lifes is not None:
        game_status.label_lifes.draw()
    if game_status.label_score is not None:
        game_status.label_score.draw()
    if game_status.label_game_over is not None:
        game_status.label_game_over.draw()


def create_compost(dt, batch):
    """
    Function create picture of compost with random coordinates.
    Finally trigger function delete_compost.
    """
    if not game_status.compost_coordinates:
        x_compost = randrange(32, WIDTH, 64)
        y_compost = randrange(32, HEIGHT, 64)
        while (x_compost, y_compost) in game_status.snake_coordinates\
                or (x_compost, y_compost) in game_status.health_coordinates\
                or (x_compost, y_compost) in game_status.poison_coordinates:
            x_compost = randrange(32, WIDTH, 64)
            y_compost = randrange(32, HEIGHT, 64)

        game_status.compost_coordinates.append((x_compost, y_compost))
        game_status.compost.append(pyglet.sprite.Sprite(img_compost,
                                                        x_compost,
                                                        y_compost,
                                                        batch=batch))

        pyglet.clock.schedule_once(delete_compost, 3)


def create_food(dt, batch):
    """
    Function create health, poison food with random coordinates.
    """
    x_food = randrange(32, WIDTH, 64)
    y_food = randrange(32, HEIGHT, 64)
    while (x_food, y_food) in game_status.snake_coordinates \
            or (x_food, y_food) in game_status.health_coordinates\
            or (x_food, y_food) in game_status.poison_coordinates\
            or (x_food, y_food) in game_status.compost_coordinates:
        x_food = randrange(32, WIDTH, 64)
        y_food = randrange(32, HEIGHT, 64)

    if choice((True, False)):
        game_status.health_coordinates.append((x_food, y_food))
        game_status.health_food.append(pyglet.sprite.Sprite(img_health_food,
                                                            x_food,
                                                            y_food,
                                                            batch=batch))
    else:
        game_status.poison_coordinates.append((x_food, y_food))
        game_status.poison_food.append(pyglet.sprite.Sprite(img_poison_food,
                                                            x_food,
                                                            y_food,
                                                            batch=batch))


def eat_food(batch):
    """
    Function describes what happened when snake eats something
    (health, poison food or composter).
    """
    for num, coordinates in enumerate(game_status.health_coordinates):
        if game_status.snake_coordinates[-1] == coordinates:
            x_0, y_0 = game_status.snake_coordinates[0]
            x_1, y_1 = game_status.snake_coordinates[1]
            x_0 += (x_0 - x_1)
            y_0 += (y_0 - y_1)

            game_status.snake_coordinates.insert(0, (x_0, y_0))
            game_status.lifes += 1
            game_status.score += 1
            del game_status.health_coordinates[num]
            del game_status.health_food[num]

    for num, coordinates in enumerate(game_status.poison_coordinates):
        if game_status.snake_coordinates[-1] == coordinates:
            game_status.lifes -= 4
            del game_status.poison_coordinates[num]
            del game_status.poison_food[num]

    if game_status.snake_coordinates[-1] in game_status.compost_coordinates:
        for num in range((len(game_status.poison_food))//3):
            del game_status.poison_coordinates[num]
            del game_status.poison_food[num]

        game_status.speed_coeficient *= 4/5
        game_status.speed = game_status.speed_coeficient
        print(game_status.speed)
        game_status.compost_coordinates.clear()
        game_status.compost.clear()
        pyglet.clock.schedule_once(create_compost, 50, batch)


def delete_compost(dt):
    """
    Function delete pciture of composter after 3 seconds.
    Time for deleting is defined in create_compost function.
    """
    if game_status.compost_coordinates and game_status.compost:
        game_status.compost_coordinates.clear()
        game_status.compost.clear()
        pyglet.clock.schedule_once(create_compost, 50, batch)


def move_snake():
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
        game_status.label_game_over = pyglet.text.Label(
                                                "GAME OVER: Snake crashed!",
                                                font_name='Times New Roman',
                                                font_size=24,
                                                color=((255, 255, 255, 255)),
                                                x=game_window.width//2,
                                                y=game_window.height//2,
                                                anchor_x='center',
                                                anchor_y='center',
                                                )

        pyglet.clock.unschedule(move_interval)
        pyglet.clock.unschedule(create_food)
        pyglet.clock.unschedule(create_compost)
    # if your lifes are < than 1 game over
    elif game_status.lifes < 1:
        game_status.label_game_over = pyglet.text.Label(
                                                "GAME OVER: No lifes !",
                                                font_name='Times New Roman',
                                                font_size=24,
                                                color=((255, 255, 255, 255)),
                                                x=game_window.width//2,
                                                y=game_window.height//2,
                                                anchor_x='center',
                                                anchor_y='center',
                                                )

        pyglet.clock.unschedule(move_interval)
        pyglet.clock.unschedule(create_food)
        pyglet.clock.unschedule(create_compost)

    # otherwise game continue normally
    else:
        game_status.snake_coordinates.append((x, y))
        del game_status.snake_coordinates[0]
        eat_food(batch)
        game_status.create_snake(batch)
        for i, sprite in enumerate(game_status.snake_body):
            sprite.x, sprite.y = game_status.snake_coordinates[i]

    # Label for health
    game_status.label_lifes = pyglet.text.Label("x " + str(game_status.lifes),
                                                font_name='Times New Roman',
                                                font_size=18,
                                                color=((255, 255, 255, 255)),
                                                x=50,
                                                y=game_window.height - 16,
                                                anchor_x='center',
                                                anchor_y='center',
                                                )

    # Label for score
    game_status.label_score = pyglet.text.Label(
                                            "SCORE: " + str(game_status.score),
                                            font_name='Times New Roman',
                                            font_size=18,
                                            color=((255, 255, 255, 255)),
                                            x=game_window.width - 70,
                                            y=game_window.height - 16,
                                            anchor_x='center',
                                            anchor_y='center',
                                                )


def move_interval(dt):
    """
    This function change speed of frequency of game = speed of snake.
    """
    game_status.speed -= dt
    if game_status.speed < 0:
        game_status.speed = game_status.speed_coeficient
        move_snake()


def move_snake_onkey(key, modifikator):
    """
    control snake with keyboard arrows
    """
    if key == pyglet.window.key.UP:
        game_status.snake_course = (0, 1)
    if key == pyglet.window.key.DOWN:
        game_status.snake_course = (0, -1)
    if key == pyglet.window.key.RIGHT:
        game_status.snake_course = (1, 0)
    if key == pyglet.window.key.LEFT:
        game_status.snake_course = (-1, 0)


img_health_food = pyglet.image.load("red_apple.png")
center_image(img_health_food)
img_poison_food = pyglet.image.load("poison_apple.png")
center_image(img_poison_food)
img_life = pyglet.image.load("life.png")
center_image(img_life)
img_compost = pyglet.image.load("compost.png")
center_image(img_compost)
batch = pyglet.graphics.Batch()
heart = pyglet.sprite.Sprite(img_life, 15, HEIGHT - 15)
game_status = Game_status(batch)


for image in game_status.snake_tiles.values():
    center_image(image)

create_food(0, batch)

game_window.push_handlers(
    on_draw=draw_window,
    on_key_press=move_snake_onkey,
)

pyglet.clock.schedule_interval(move_interval, 1/30)
pyglet.clock.schedule_interval(create_food, 4, batch)
pyglet.clock.schedule_once(create_compost, 50, batch)


if __name__ == "__main__":
    pyglet.app.run()
