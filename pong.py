"""
In the Pong game, two players control two paddles. Left player control left paddle by pressing 'q' to move the paddle up
and pressing 'a' to move the paddle down. Right player use 'p' and 'l' to move right paddle up and down. When the
ball hit the boundary or the paddle's facing center side, the ball will reflect. If left boundary is hit by the ball,
right player will add one point, vice versa. When one player have more than 10 points, the game will stop but the
window won't close. The window will close only when the user hit close bottom.
"""

import pygame


def main():
    pygame.init()  # Initialize all pygame modules.
    pygame.display.set_mode((500, 400))  # Create a pygame display window.
    pygame.display.set_caption('Mini-project 2 - Pong')  # Set the title of the display window.
    w_surface = pygame.display.get_surface()  # Get the display surface.
    game = Game(w_surface)  # Create a game object.
    game.play()  # Start the main game loop.
    pygame.quit()  # Quit pygame and clean up the window.


class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a game.

        self.surface = surface
        self.bg_color, self.fg_color = pygame.Color('black'), pygame.Color('white')  # Two colors used in the program.

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked, self.continue_game = False, True

        self.l_score, self.r_score = 0, 0  # Score recorders.

        self.left_velocity, self.right_velocity = 0, 0  # Paddles' original velocity.

        self.left_y, self.right_y = 150, 150  # Paddles' top side coordinate.

        self.left_x, self.right_x = 100, 390  # Paddles' left side coordinate.

        self.ball = Ball(self.fg_color, 5, [250, 200], [6, 2], self.surface)
        self.left_paddle = Paddle(self.fg_color, self.left_x, self.left_y, self.left_velocity, self.surface)
        self.right_paddle = Paddle(self.fg_color, self.right_x, self.right_y, self.right_velocity, self.surface)

    def play(self):
        # Play the game until the player presses the close box.

        while not self.close_clicked:  # Until player clicks close box.
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # Run at most with FPS Frames.

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.

        # Identify user keyboard input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.KEYDOWN:
                self.key_down(event)
            elif event.type == pygame.KEYUP:
                self.key_up(event)

        # Create new Paddle objects to override the previous Paddle objects.
        self.left_paddle = Paddle(self.fg_color, self.left_x, self.left_y, self.left_velocity, self.surface)
        self.right_paddle = Paddle(self.fg_color, self.right_x, self.right_y, self.right_velocity, self.surface)

    def key_down(self, event):
        # Check the specific situation when user press down a key.

        # Change left paddle velocity.
        if event.key == pygame.K_q:
            self.left_velocity = -10
        elif event.key == pygame.K_a:
            self.left_velocity = 10

        # Change right paddle velocity.
        if event.key == pygame.K_p:
            self.right_velocity = -10
        elif event.key == pygame.K_l:
            self.right_velocity = 10

    def key_up(self, event):
        # Check the specific situation when user release a key.

        # Reset the paddle's velocity to zero when user release related keys.
        if event.key == pygame.K_q or event.key == pygame.K_a:
            self.left_velocity = 0
        elif event.key == pygame.K_p or event.key == pygame.K_l:
            self.right_velocity = 0

    def draw(self):
        # Draw all game objects.

        self.surface.fill(self.bg_color)  # Clear the display surface.
        self.ball.draw()
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.left_score()
        self.right_score()
        pygame.display.update()  # Make the updated surface appear on the display.

    def update(self):
        # Update the game objects for the next frame.

        self.left_y = self.left_paddle.move()
        self.right_y = self.right_paddle.move()

        # Update the score based on the ball's movement.
        player = self.ball.move(self.left_paddle, self.right_paddle)
        if player == 'left':
            self.l_score += 1
        elif player == 'right':
            self.r_score += 1

    def decide_continue(self):
        # Check and remember if the game should continue.

        if self.l_score > 10 or self.r_score > 10:
            self.continue_game = False

    def left_score(self):
        # Show left score at the top left corner of the surface

        font = pygame.font.SysFont('Times New Roman', 50)
        text_box = font.render(str(self.r_score), True, pygame.Color('white'), None)
        location = (0, 0)
        self.surface.blit(text_box, location)

    def right_score(self):
        # Show right score at the top right corner of the surface.

        font = pygame.font.SysFont('Times New Roman', 50)
        text_box = font.render(str(self.l_score), True, pygame.Color('white'), None)
        text_rect = text_box.get_rect()
        text_rect.right = self.surface.get_width()
        location = text_rect
        self.surface.blit(text_box, location)


class Ball:
    # An object in this class represents a ball that moves.

    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        # initialize a Dot.

        self.color = ball_color
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface

    def move(self, left_paddle, right_paddle):
        # Change the location of the ball by adding the corresponding speed values to the x and y coordinate of its
        # center.

        # Check x then y.
        size = self.surface.get_size()
        for i in range(0, 2):
            self.center[i] += self.velocity[i]

            # To see if the ball collide with the boundary.
            if self.center[i] <= self.radius or self.center[i] + self.radius >= size[i]:
                self.velocity[i] = -self.velocity[i]

                # To see if the ball collide left or right boundary.
                if i == 0:
                    return 'left' if self.velocity[0] > 0 else 'right'  # The velocity has already been reversed

            # To see if the ball collide with left paddle from right side.
            elif left_paddle.get_center().collidepoint(self.center) and self.velocity[0] < 0:
                self.velocity[0] = -self.velocity[0]

            # To see if the ball collide with the right paddle from left side.
            elif right_paddle.get_center().collidepoint(self.center) and self.velocity[0] > 0:
                self.velocity[0] = -self.velocity[0]

    def draw(self):
        # Draw the ball on surface.

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)


class Paddle:
    # An object in this class represents a Paddle that moves.

    def __init__(self, paddle_color, x, y, paddle_velocity, surface):
        # Initialize a paddle.

        self.color = paddle_color
        self.x = x
        self.y = y
        self.velocity = paddle_velocity
        self.surface = surface

    def move(self):
        # Change the y coordinate of the paddle.

        # Make sure the paddle don't move across the boundary.
        if self.get_center().top + self.velocity < 0 or self.get_center().bottom + self.velocity > 400:
            self.velocity = 0

        self.y += self.velocity
        return self.y

    def draw(self):
        # Draw the paddle on the surface.

        pygame.draw.rect(self.surface, self.color, pygame.Rect(self.x, self.y, 10, 100))

    def get_center(self):
        # Get the Rect of the paddle.

        return pygame.Rect(self.x, self.y, 10, 100)


main()
