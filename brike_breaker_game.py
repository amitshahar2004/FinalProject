import tkinter as tk

BRIKE_BREAKER_BALL_SPEAD      = 10
BRIKE_BREAKER_BALL_SIZE       = 10
BRIKE_BREAKER_X_DIRECTION     = 0
BRIKE_BREAKER_Y_DIRECTION     = 1
BRIKE_BREAKER_PLAYER_WIDTH    = 40
BRIKE_BREAKER_PLAYER_HIGH     = 5
BRIKE_BREAKER_NUM_OF_ATTEMPTS = 3

#Brick Breaker game
#המשתמש צריך לשבור את הלבנים תוך זריקת הכדור אלייהם
#
class BrickBreakerClass(object):
    def __init__(self, canvas, param):
        self.param  = param
        self.canvas = canvas

    def get_place(self):
        return self.canvas.coords(self.param)

    def move(self, x, y):
        self.canvas.move(self.param, x, y)

    def delete(self):
        self.canvas.delete(self.param)


class BallClass(BrickBreakerClass):
    def __init__(self, canvas, x, y):
        self.direction = [1, -1]

        self.ball_speed = BRIKE_BREAKER_BALL_SPEAD
        param = canvas.create_oval(x-BRIKE_BREAKER_BALL_SIZE, y-BRIKE_BREAKER_BALL_SIZE,
                                  x+BRIKE_BREAKER_BALL_SIZE, y+BRIKE_BREAKER_BALL_SIZE,
                                  fill='white')
        super(BallClass, self).__init__(canvas, param)

    def update_direction(self):
        coordinates = self.get_place()
        width = self.canvas.winfo_width()
        if coordinates[0] <= 0 or coordinates[2] >= width:
            self.direction[BRIKE_BREAKER_X_DIRECTION] *= -1
        if coordinates[1] <= 0:
            self.direction[BRIKE_BREAKER_Y_DIRECTION] *= -1
        x = self.direction[BRIKE_BREAKER_X_DIRECTION] * self.ball_speed
        y = self.direction[BRIKE_BREAKER_Y_DIRECTION] * self.ball_speed
        self.move(x, y)

    def crash(self, game_objects):
        coordinates = self.get_place()
        x = (coordinates[0] + coordinates[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[BRIKE_BREAKER_Y_DIRECTION] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coordinates = game_object.get_place()
            if x > coordinates[2]:
                self.direction[BRIKE_BREAKER_X_DIRECTION] = 1
            elif x < coordinates[0]:
                self.direction[BRIKE_BREAKER_X_DIRECTION] = -1
            else:
                self.direction[BRIKE_BREAKER_Y_DIRECTION] *= -1

        for game_object in game_objects:
            if isinstance(game_object, BrickClass):
                game_object.hit()


class PlayerClass(BrickBreakerClass):
    def __init__(self, canvas, x, y):
        self.ball = None
        param = canvas.create_rectangle(x - BRIKE_BREAKER_PLAYER_WIDTH,
                                       y - BRIKE_BREAKER_PLAYER_HIGH,
                                       x + BRIKE_BREAKER_PLAYER_WIDTH,
                                       y + BRIKE_BREAKER_PLAYER_HIGH,
                                       fill='#FF4040')
        super(PlayerClass, self).__init__(canvas, param)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coordinates = self.get_place()
        width = self.canvas.winfo_width()
        if coordinates[0] + offset >= 0 and coordinates[2] + offset <= width:
            super(PlayerClass, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)


class BrickClass(BrickBreakerClass):
    COLORS = {1: '#4535AA', 2: '#ED639E', 3: '#8FE1A2'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = BrickClass.COLORS[hits]
        param = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(BrickClass, self).__init__(canvas, param)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.param,
                                   fill=BrickClass.COLORS[self.hits])


class GameClass(tk.Frame):
    def __init__(self, master):
        super(GameClass, self).__init__(master)
        self.attempts = BRIKE_BREAKER_NUM_OF_ATTEMPTS
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()
        self.pack()

        self.params = {}
        self.ball = None
        self.paddle = PlayerClass(self.canvas, self.width/2, 326)
        self.params[self.paddle.param] = self.paddle
        # adding brick with different hit capacities - 3,2 and 1
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 3)
            self.add_brick(x + 37.5, 70, 2)
            self.add_brick(x + 37.5, 90, 1)

        self.hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                         lambda _: self.paddle.move(10))

    def setup_game(self):
           self.add_ball()
           self.update_attempts_text()
           self.text = self.draw_text(300, 200,
                                      'To Start - Press Space')
           self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_place()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = BallClass(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        brick = BrickClass(self.canvas, x, y, hits)
        self.params[brick.param] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_attempts_text(self):
        text = 'attempts: %s' % self.attempts
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def check_hit(self):
        ball_coords = self.ball.get_place()
        params = self.canvas.find_overlapping(*ball_coords)
        objects = [self.params[x] for x in params if x in self.params]
        self.ball.crash(objects)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        self.check_hit()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.ball_speed = None
            self.draw_text(300, 200, 'you are the winner!')
            print("you are the winner!")
        elif self.ball.get_place()[3] >= self.height:
            self.ball.ball_speed = None
            self.attempts -= 1
            if self.attempts < 0:
                self.draw_text(300, 200, 'Sorry Game Over Try Again!')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update_direction()
            self.after(50, self.game_loop)




if __name__ == '__main__':
    root = tk.Tk()
    root.title('Break those Bricks!')
    game = GameClass(root)
    game.mainloop()