import pyglet


SIZE_POLE = 64  # the smallest part of game pole is 64 x 64 pixels
WIDTH = SIZE_POLE * 12
HEIGHT = SIZE_POLE * 12


class Game_status:
    def __init__(self):
        self.snake_coordinates = [(0, 0), (64, 0), (128, 0)]
        self.snake_course = set()


game_window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


def draw_window():
    game_window.clear()
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    batch.draw()


def move_snake_interval(dt):

    x, y = game_status.snake_coordinates[-1]
    if (1, 0) in game_status.snake_course:
        x += dt * SIZE_POLE
        game_status.snake_coordinates.append((x, y))
    del game_status.snake_coordinates[0]

    for i, part in enumerate(snake_body):
        part.x, part.y = game_status.snake_coordinates[i]

    print(snake_body)

    # for position, part in enumerate(snake_body):
    #     if (1, 0) in game_status.snake_course:
    #         part.x += dt * SIZE_POLE
    #         game_status.snake_coordinates.append((part.x, 0))
    #     elif (-1, 0) in game_status.snake_course:
    #         part.x += -abs(dt * SIZE_POLE)
    #         game_status.snake_coordinates.append((part.x, 0))
    #     elif (0, 1) in game_status.snake_course:
    #         part.y += dt * SIZE_POLE
    #         game_status.snake_coordinates.append((0, part.y))
    #     elif (0, -1) in game_status.snake_course:
    #         part.y += -abs(dt * SIZE_POLE)
    #         game_status.snake_coordinates.append((0, part.y))
    #     del game_status.snake_coordinates[0]
    #     print(game_status.snake_coordinates)


def move_snake_onkey(key, modifikator):
    if key == pyglet.window.key.UP:
        game_status.snake_course.clear()
        game_status.snake_course.add((0, 1))
    if key == pyglet.window.key.DOWN:
        game_status.snake_course.clear()
        game_status.snake_course.add((0, -1))
    if key == pyglet.window.key.RIGHT:
        game_status.snake_course.clear()
        game_status.snake_course.add((1, 0))
    if key == pyglet.window.key.LEFT:
        game_status.snake_course.clear()
        game_status.snake_course.add((-1, 0))


img_snake = pyglet.image.load("green_rectangle.png")
game_status = Game_status()
batch = pyglet.graphics.Batch()

game_status.snake_course.add((1, 0))

snake_body = []

# for x, y in game_status.snake_coordinates:
for x, y in game_status.snake_coordinates:
    snake_body.append(pyglet.sprite.Sprite(img_snake, x, y, batch=batch))

game_window.push_handlers(
    on_draw=draw_window,
    on_key_press=move_snake_onkey,
)

pyglet.clock.schedule_interval(move_snake_interval, 1/10)

if __name__ == "__main__":
    pyglet.app.run()
