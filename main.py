import kivy

kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty,
                             ObjectProperty, BooleanProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class PongPaddle(Widget):
    score = NumericProperty(0)
    can_bounce = BooleanProperty(True)

    def bounce_ball(self, ball):
        if self.collide_widget(ball) and self.can_bounce:
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            self.can_bounce = False
        elif not self.collide_widget(ball) and not self.can_bounce:
            self.can_bounce = True

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        if self.ball:
            self.ball.center = self.center
            self.ball.velocity = vel

    def update(self, dt):
        if self.ball and self.player1 and self.player2:
            self.ball.move()
            self.player1.bounce_ball(self.ball)
            self.player2.bounce_ball(self.ball)

            if (self.ball.y < self.y) or (self.ball.top > self.top):
                self.ball.velocity_y *= -1

            if self.ball.x < self.x:
                self.player2.score += 1
                self.serve_ball(vel=(4, 0))
            if self.ball.right > self.width:
                self.player1.score += 1
                self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3 and self.player1:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3 and self.player2:
            self.player2.center_y = touch.y

class MenuScreen(Screen):
    def start_game(self):
        self.manager.current = 'game'

class GameScreen(Screen):
    def on_enter(self):
        pong_game = self.ids.pong_game
        if pong_game:
            pong_game.serve_ball()
            Clock.schedule_interval(pong_game.update, 1.0 / 60.0)

    def on_leave(self):
        Clock.unschedule(self.ids.pong_game.update)

class PongApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    PongApp().run()
