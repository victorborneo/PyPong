import random
import pygame

pygame.init()

screenx, screeny = 1000, 800 
window = pygame.display.set_mode((screenx, screeny))
font = pygame.font.SysFont('Arial', 30)
pygame.display.set_caption("Pong")

# RGB
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

class Player:
    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        self.points = points
        self.rect = pygame.Rect(self.x, self.y, 25, 100)

    def move(self, direction, speed):
        self.y += direction * speed

        if self.y <= 0:
            self.y = 0
        elif self.y + 100 >= screeny:
            self.y = screeny - 100

        self.rect = pygame.Rect(self.x, self.y, 25, 100)

class Ball:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.reflect_count = 0
        self.x_direction = random.choice((-1, 1))
        self.y_direction = random.choice((-1, 1))
        self.rect = pygame.Rect(self.x, self.y, 25, 25)

    def move(self):
        self.x += self.x_direction * self.speed
        self.y += self.y_direction * self.speed
        self.rect = pygame.Rect(self.x, self.y, 25, 25)

    def reflect(self, p1, bot):
        if 0 >= self.y or self.y + 25 >= screeny:
            self.y_direction *= -1

        if self.rect.colliderect(p1.rect) or self.rect.colliderect(bot.rect):
            self.x_direction *= -1
            self.reflect_count += 1

        if self.reflect_count >= 10 and self.speed < 10:
            self.reflect_count = 0
            self.speed += 1

    def check_win(self, p1, bot):
        reset = False

        if self.x + 25 <= 0:
            bot.points += 1
            reset = True
        elif self.x >= screenx:
            p1.points += 1
            reset = True

        return reset

def redraw_game_window():
    window.fill(black)
    p_points = font.render(str(p1.points), True, red)
    b_points = font.render(str(bot.points), True, red)
    speed = font.render(f"Speed: {ball.speed}", True, red)

    window.blit(p_points, (10, 10))
    window.blit(b_points, (990 - len(str(bot.points)) * 15, 10))
    window.blit(speed, (10, screeny - 35))

    pygame.draw.rect(window, white, (ball.x, ball.y, 25, 25))
    pygame.draw.rect(window, white, (p1.x, p1.y, 25, 100))
    pygame.draw.rect(window, white, (bot.x, bot.y, 25, 100))

    pygame.display.update()


run = True
ball = Ball(screenx // 2, screeny // 2 + 25, 5)
p1 = Player(50, screeny // 2, 0)
bot = Player(screenx - 75, screeny // 2, 0)
while run:
    pygame.time.Clock().tick(60)
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_UP]:
        p1.move(-1, 8)
    elif keys[pygame.K_DOWN]:
        p1.move(1, 8)

    if ball.speed <= 8:
        bot_speed = ball.speed
    else:
        bot_speed = 8

    bot.move(ball.y_direction, bot_speed)

    if ball.check_win(p1, bot):
        ball = Ball(screenx // 2, screeny // 2 + 25, 5)
        p1 = Player(50, screeny // 2, p1.points)
        bot = Player(screenx - 75, screeny // 2, bot.points)

    ball.move()
    ball.reflect(p1, bot)
    redraw_game_window()
    
pygame.quit()
