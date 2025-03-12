import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BALL_RADIUS = 15
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 10
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BALL_SPEED = 3
ANGLE = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Catcher Game")
font = pygame.font.Font(None, 36)

game_over = False
score = 0

class Platform:
    def __init__(self, x, y, angle, direction, index):
        self.x = x
        self.y = y
        self.angle = angle
        self.direction = direction
        self.index = index
        self.length = PLATFORM_WIDTH

    def draw(self):
        rad = math.radians(self.angle)
        if self.direction == 'left':
            x2, y2 = self.x + self.length * math.cos(rad), self.y + self.length * math.sin(rad)
        else:
            x2, y2 = self.x - self.length * math.cos(rad), self.y + self.length * math.sin(rad)
        pygame.draw.line(screen, ORANGE, (self.x, self.y), (x2, y2), PLATFORM_HEIGHT)

class Ball:
    def __init__(self, platform):
        rad = math.radians(platform.angle)
        self.x = platform.x
        self.speed_x = BALL_SPEED * math.cos(rad) if platform.direction == 'left' else -BALL_SPEED * math.cos(rad)
        self.y = platform.y
        self.speed_y = BALL_SPEED * math.sin(rad)
        self.falling = True
        self.platform = platform

    def update(self):
        if self.falling:
            self.x += self.speed_x
            self.y += self.speed_y

            rad = math.radians(self.platform.angle)
            end_x = self.platform.x + (self.platform.length if self.platform.direction == 'left' else -self.platform.length) * math.cos(rad)
            end_y = self.platform.y + self.platform.length * math.sin(rad)

            if (self.platform.direction == 'left' and self.x > end_x) or (self.platform.direction == 'right' and self.x < end_x):
                global game_over
                game_over = True
                return False
        return True

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BALL_RADIUS)

class Button:
    def __init__(self, x, y, index):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.index = index

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)
        text = font.render(str(self.index + 1), True, WHITE)
        screen.blit(text, (self.rect.x + 25, self.rect.y + 10))

platforms = [
    Platform(0, 150, ANGLE, 'left', 0),
    Platform(0, 300, ANGLE, 'left', 1),
    Platform(WIDTH, 150, ANGLE, 'right', 2),
    Platform(WIDTH, 300, ANGLE, 'right', 3)
]

buttons = [
    Button(50, 500, 0),
    Button(200, 500, 1),
    Button(550, 500, 2),
    Button(700, 500, 3)
]

balls = []
running = True
clock = pygame.time.Clock()
time_to_next_ball = random.randint(60, 180)

while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for platform in platforms:
        platform.draw()

    for button in buttons:
        button.draw()

    if not game_over:
        time_to_next_ball -= 1
        if time_to_next_ball <= 0:
            balls.append(Ball(random.choice(platforms)))
            time_to_next_ball = random.randint(60, 180)

        new_balls = []
        for ball in balls:
            if ball.update():
                new_balls.append(ball)
            else:
                score += 1
            ball.draw()
        balls = new_balls

        keys = pygame.key.get_pressed()
        for button in buttons:
            if keys[pygame.K_1 + button.index]:
                new_balls = [ball for ball in new_balls if ball.platform.index != button.index]
                if len(new_balls) < len(balls):
                    score += 1
                balls = new_balls
                break

    else:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        score_text = font.render(f"Score:{score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 30))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        game_over = False
        balls.clear()
        time_to_next_ball = random.randint(60, 180)
        score = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()