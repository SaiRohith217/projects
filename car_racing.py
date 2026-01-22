import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
ROAD_LEFT = 50
ROAD_RIGHT = WIDTH - 50
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANES = 3
LANE_WIDTH = ROAD_WIDTH // LANES
player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy.png")
road_img = pygame.image.load("assets/road.png")
player_img = pygame.transform.scale(player_img, (40, 70))
enemy_img = pygame.transform.scale(enemy_img, (40, 70))
road_img = pygame.transform.scale(road_img, (ROAD_WIDTH, HEIGHT))
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 6
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed
    def draw(self):
        screen.blit(self.image, self.rect)
class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        lane = random.randint(0, LANES - 1)
        self.rect.x = ROAD_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - self.rect.width) // 2
        self.rect.y = random.randint(-600, -100)
        self.speed = random.randint(2, 4)
    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.reset()
    def draw(self):
        screen.blit(self.image, self.rect)
road_y1 = 0
road_y2 = -HEIGHT
def draw_road(speed):
    global road_y1, road_y2
    road_y1 += speed
    road_y2 += speed
    if road_y1 >= HEIGHT:
        road_y1 = -HEIGHT
    if road_y2 >= HEIGHT:
        road_y2 = -HEIGHT
    screen.blit(road_img, (ROAD_LEFT, road_y1))
    screen.blit(road_img, (ROAD_LEFT, road_y2))
def draw_speed_meter(speed):
    MAX_SPEED = 15
    speed = min(speed, MAX_SPEED)
    meter_x = WIDTH - 18     
    meter_y = 160
    meter_width = 10
    meter_height = 260
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (meter_x, meter_y, meter_width, meter_height),
        2
    )    
    fill_height = int((speed / MAX_SPEED) * meter_height)
    fill_y = meter_y + meter_height - fill_height
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (meter_x + 2, fill_y, meter_width - 4, fill_height)
    )
    text = font.render("SPD", True, (255, 255, 255))
    screen.blit(text, (meter_x - 15, meter_y - 22))
player = Player()
enemies = [Enemy() for _ in range(3)]
score = 0
game_over = False
running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player = Player()
                enemies = [Enemy() for _ in range(3)]
                score = 0
                game_over = False
    if not game_over:
        base_speed = 5
        speed = base_speed + min(10, score // 600)
        draw_road(speed)
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw()
        for enemy in enemies:
            enemy.move(speed)
            enemy.draw()
            if player.rect.inflate(-10, -10).colliderect(
                enemy.rect.inflate(-10, -10)
            ):
                game_over = True
        score += 1
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        draw_speed_meter(speed)
        if score % 800 == 0:
            enemies.append(Enemy())
    else:
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (140, 260))
        screen.blit(font.render("Press R to Restart", True, (255, 255, 255)), (110, 300))
    pygame.display.update()
pygame.quit()
sys.exit()
