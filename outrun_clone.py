import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
ROAD_WIDTH = 400
LANE_WIDTH = ROAD_WIDTH // 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Load Assets
def load_image(name, scale=None):
    img = pygame.image.load(os.path.join(os.getcwd(), name))
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

car_img = load_image("car.png", (50, 90))
traffic_car_img = load_image("traffic_car.png", (50, 90))
bg_img = load_image("background.png", (WIDTH, HEIGHT))
road_img = load_image("road.png", (ROAD_WIDTH, HEIGHT))
tree_img = load_image("side_trees.png", (80, 80))
boost_img = load_image("speed_boost.png", (40, 40))

# Game Variables
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120
speed = 5
max_speed = 12
acceleration = 0.2
friction = 0.1
turn_speed = 7
score = 0
traffic = []
trees = []
boosts = []

# Setup Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OutRun Clone")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_background():
    """ Draws the background and road """
    screen.blit(bg_img, (0, 0))
    screen.blit(road_img, (WIDTH//2 - ROAD_WIDTH//2, 0))

def draw_trees():
    """ Draws moving trees on the sides """
    for tree in trees:
        screen.blit(tree_img, (tree["x"], tree["y"]))

def draw_boosts():
    """ Draws speed boost power-ups """
    for boost in boosts:
        screen.blit(boost_img, (boost["x"], boost["y"]))

def draw_traffic():
    """ Draws traffic cars """
    for car in traffic:
        screen.blit(traffic_car_img, (car["x"], car["y"]))

def draw_player():
    """ Draws the player's car """
    screen.blit(car_img, (player_x, player_y))

def draw_score():
    """ Displays score on the screen """
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def spawn_traffic():
    """ Spawns traffic cars randomly """
    if random.randint(1, 100) > 97:
        lane = random.randint(0, 2)
        x = WIDTH // 2 - ROAD_WIDTH // 2 + lane * LANE_WIDTH + 10
        traffic.append({"x": x, "y": -100, "speed": random.randint(4, 8)})

def spawn_trees():
    """ Spawns trees on the side of the road """
    if random.randint(1, 10) > 8:
        x_pos = random.choice([WIDTH//2 - ROAD_WIDTH//2 - 80, WIDTH//2 + ROAD_WIDTH//2])
        trees.append({"x": x_pos, "y": -100})

def spawn_boost():
    """ Spawns speed boost power-ups """
    if random.randint(1, 300) > 298:
        lane = random.randint(0, 2)
        x = WIDTH // 2 - ROAD_WIDTH // 2 + lane * LANE_WIDTH + 20
        boosts.append({"x": x, "y": -100})

def move_traffic():
    """ Moves traffic cars down the road """
    for car in traffic:
        car["y"] += car["speed"]
    traffic[:] = [car for car in traffic if car["y"] < HEIGHT]

def move_trees():
    """ Moves trees down the screen """
    for tree in trees:
        tree["y"] += speed
    trees[:] = [tree for tree in trees if tree["y"] < HEIGHT]

def move_boosts():
    """ Moves speed boost power-ups """
    for boost in boosts:
        boost["y"] += speed
    boosts[:] = [boost for boost in boosts if boost["y"] < HEIGHT]

def check_collision():
    """ Checks if player collides with traffic cars """
    for car in traffic:
        if abs(player_x - car["x"]) < 40 and abs(player_y - car["y"]) < 80:
            return True
    return False

def check_boost():
    """ Checks if player collects a speed boost """
    global speed
    for boost in boosts:
        if abs(player_x - boost["x"]) < 30 and abs(player_y - boost["y"]) < 50:
            boosts.remove(boost)
            speed = min(speed + 3, max_speed + 5)

def restart_game():
    """ Restarts the game after a crash """
    global player_x, speed, score, traffic, boosts, trees
    pygame.time.delay(1000)  # Pause before restart
    player_x = WIDTH // 2 - 25
    speed = 5
    score = 0
    traffic.clear()
    boosts.clear()
    trees.clear()

# Main Game Loop
running = True
while running:
    screen.fill(GREEN)  # Background color

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Player Input (Fixed for Smooth Control)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speed = min(speed + acceleration, max_speed)
    else:
        speed = max(speed - friction, 5)

    if keys[pygame.K_LEFT] and player_x > WIDTH//2 - ROAD_WIDTH//2:
        player_x -= turn_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH//2 + ROAD_WIDTH//2 - 50:
        player_x += turn_speed

    # Spawn & Move Objects
    spawn_traffic()
    spawn_trees()
    spawn_boost()
    move_traffic()
    move_trees()
    move_boosts()

    # Check Collisions
    if check_collision():
        restart_game()  # Restart game on crash
    check_boost()

    # Update Score
    score += 1

    # Draw Everything
    draw_background()
    draw_trees()
    draw_boosts()
    draw_traffic()
    draw_player()
    draw_score()

    # Update Display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
