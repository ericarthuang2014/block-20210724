import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_width))
pygame.display.set_caption("Block")

bg_color = (234, 218, 134)
block_red = (242, 85, 92)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Define Var
rows = 6
cols = 6
ball_alive = False
game_over = 0


def show_text(text, font, size, color, x, y):
    font = pygame.font.SysFont(font, size)
    text = font.render(f"{text}", True, color)
    screen.blit(text, (x, y))


class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 40

    def create(self):
        self.blocks = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = self.width * col
                block_y = self.height * row
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                block = [rect, strength]
                block_row.append(block)
            self.blocks.append(block_row)

    def draw(self):
        for block_row in self.blocks:
            for block in block_row:
                if block[1] == 3:
                    block_color = block_blue
                if block[1] == 2:
                    block_color = block_green
                if block[1] == 1:
                    block_color = block_red
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg_color, block[0], 1)


class Paddle:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 20
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - self.height * 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 10
        self.direction = 0

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.direction = 1
            self.rect.x += self.speed * self.direction
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.direction = -1
            self.rect.x += self.speed * self.direction

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 1)


class Ball:
    def __init__(self):
        self.reset()

    def move(self):
        collision_thresh = 6
        wall_destroyed = 1
        for row_count, block_row in enumerate(wall.blocks):
            for block_count, block in enumerate(block_row):
                if self.rect.colliderect(block[0]):
                    if abs(self.rect.top - block[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.bottom - block[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - block[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - block[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    if wall.blocks[row_count][block_count][1] > 1:
                        wall.blocks[row_count][block_count][1] -= 1
                    else:
                        wall.blocks[row_count][block_count][0] = (0, 0, 0, 0)
                if wall.blocks[row_count][block_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                block_count += 1
            row_count += 1
        if wall_destroyed == 1:
            self.game_over = 1

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1
        # Look for Collision with Paddle
        if self.rect.colliderect(paddle):
            if abs(self.rect.bottom - paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.rad, self.rect.y + self.rad), self.rad)
        pygame.draw.circle(screen, bg_color, (self.rect.x + self.rad, self.rect.y + self.rad), self.rad, 1)

    def reset(self):
        self.x = paddle.x + paddle.width // 2 - 10
        self.y = paddle.y - paddle.height
        self.rad = 10
        self.rect = pygame.Rect(self.x, self.y, self.rad * 2, self.rad * 2)
        self.speed_x = 5
        self.speed_y = -5
        self.speed_max = 6
        self.game_over = 0


wall = Wall()
wall.create()
paddle = Paddle()
ball = Ball()


run = True

while run:
    clock.tick(fps)

    screen.fill(bg_color)
    wall.draw()
    paddle.draw()
    ball.draw()

    if ball_alive:
        paddle.move()
        game_over = ball.move()  # ball.move() return value of game_over
        if game_over != 0:
            ball_alive = False
    else:
        if game_over == 1:
            show_text("You Win!", "Bauhaus 93", 88, blue, 120, 300)
        if game_over == 0:
            show_text("Press Space to Start or Esc to Exit", "Bauhaus 93", 36, blue, 40, 300)
        if game_over == -1:
            show_text("You Loss!", "Bauhaus 93", 88, red, 120, 300)
            show_text("Press Space to Restart or Esc to Exit", "Bauhaus 93", 36, blue, 20, 400)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE and ball_alive == False:
                ball_alive = True
                ball.reset()
                wall.create()

    pygame.display.update()

pygame.quit()
