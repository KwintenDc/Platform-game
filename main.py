import pygame
from pygame.locals import *
import sys

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Player(GameObject):
    def __init__(self, x, y, width, height, color, vel_y, speed, onGround, isJumping, isMoving):
        super().__init__(x, y, width, height, color)
        self.vel_y = vel_y
        self.speed = speed
        self.onGround = onGround
        self.isJumping = isJumping
        self.isMoving = isMoving

class Platform(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Obstacles(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Enemies(GameObject):
    def __init__(self, x, y, width, height, color, speed, walking_left):
        super().__init__(x, y, width, height, color)
        self.speed = speed
        self.walking_left = walking_left

# Define game states
START_SCREEN = 0
PLAYING = 1

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_COLOR = (66, 135, 245)  # Lightblue

COLOR_WHITE = (255, 255, 255)  
COLOR_BLACK = (0, 0, 0)  
COLOR_GRAY = (128, 128, 128)  
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (34, 139, 34) 
COLOR_BLUE = (0, 0, 255)  
COLOR_YELLOW = (255, 255, 0) 
COLOR_MAGENTA = (255, 0, 255) 
COLOR_CYAN = (0, 255, 255)
COLOR_BROWN = (231, 90, 16)
COLOR_DARK_BROWN = (69, 17, 0)

PLAYER_HEIGHT = 65
PLAYER_WIDTH = PLAYER_HEIGHT / 2
PLAYER_COLOR = COLOR_BLUE
PLAYER_SPEED = 0.25

ENEMY_HEIGHT = 30
ENEMY_WIDTH = 30
ENEMY_COLOR = COLOR_RED
ENEMY_SPEED = 0.10 

PLATFORM_THICKNESS = 40

GROUND_COLOR = COLOR_GREEN
GROUND_THICKNESS = 50
GRAVITY = 0.0008            # Acceleration due to gravity
JUMP_STRENGTH = -0.5        # Negative because y-axis is flipped
              
def CheckCollisionPlatforms(platform, player): 
    if player.x < platform.x + platform.width and player.x > platform.x - player.width:
        if player.y + player.height > platform.y and player.y + player.height < platform.y + 1:
            return True
    return False

def CheckCollisionObstacles(obstacle, player):
    if player.x + player.width > obstacle.x and player.x < obstacle.x + obstacle.width:
        if player.y + player.height > obstacle.y and player.y + player.height < obstacle.y + 1:
            return "T"
    if player.x + player.width < obstacle.x + obstacle.width/2 and player.x + player.width > obstacle.x: 
        if player.y + player.height > obstacle.y and player.y < obstacle.y + obstacle.height:
            return "LW"
    if player.x > obstacle.x + obstacle.width/2 and player.x < obstacle.x + obstacle.width:
        if player.y + player.height > obstacle.y and player.y < obstacle.y + obstacle.height:
            return "RW"
    return False

def MoveEnemy(enemies, player):
    if player.isMoving is True:
        for enemy in enemies:
            if enemy.walking_left is True:
                enemy.x -= (player.speed + enemy.speed)
            elif enemy.walking_left is False:
                enemy.x += (enemy.speed - player.speed)
    else: 
        for enemy in enemies:
            if enemy.walking_left is True:
                enemy.x -= (enemy.speed)
            elif enemy.walking_left is False:
                enemy.x += (enemy.speed) 

# Temporary lose condition
def CheckLoseCondition(lose):
    if lose:
        return True
    return False

def draw_start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    screen.fill(SCREEN_COLOR)  # Light Blue

    # Draw some hills in the background
    pygame.draw.circle(screen, COLOR_GREEN, (150, 500), 100)
    pygame.draw.circle(screen, COLOR_GREEN, (300, 500), 80)
    pygame.draw.circle(screen, COLOR_GREEN, (450, 500), 120)

    # Draw the ground
    pygame.draw.rect(screen, (139, 69, 19), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

    # Draw a simple Mario Bros-style logo
    font = pygame.font.Font(None, 72)
    text = font.render("Platform game", True, (255, 255, 255))

    # Calculate the width of the text surface
    text_width = text.get_width()

    # Center the text on the x-axis
    text_x = SCREEN_WIDTH // 2 - text_width // 2
    text_y = SCREEN_HEIGHT // 4

    screen.blit(text, (text_x, text_y))

    # Draw a prompt to press any key
    font = pygame.font.Font(None, 36)
    text = font.render("Press Enter to start", True, (255, 255, 255))
    # Calculate the width of the text surface
    text_width = text.get_width()

    # Center the text on the x-axis
    text_x = SCREEN_WIDTH // 2 - text_width // 2
    text_y = SCREEN_HEIGHT // 2

    screen.blit(text, (text_x, text_y))

def reset_game():
    # Initialize player position, velocity, and jump state
    player_x, player_y = 400 - PLAYER_WIDTH / 2, SCREEN_HEIGHT - GROUND_THICKNESS - PLAYER_HEIGHT
    player_vel_y = 0
    onGround = False
    isJumping = False
    isMoving = False

    player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, player_vel_y, PLAYER_SPEED, onGround, isJumping, isMoving)

    # Create platforms
    platforms_data = [
        # (x, y, width, height, color)
        [450, 400, 200, PLATFORM_THICKNESS, COLOR_BROWN],
        [2500, 400, 200, PLATFORM_THICKNESS, COLOR_BROWN],
        [2800, 300, 200, PLATFORM_THICKNESS, COLOR_BROWN],
    ]

    platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in platforms_data]

    ground_platforms_data = [
        # (x, y, width, height, color)
        [0, SCREEN_HEIGHT - GROUND_THICKNESS, 2000, GROUND_THICKNESS, GROUND_COLOR],
        [2000 + 200, SCREEN_HEIGHT - GROUND_THICKNESS, 2200, GROUND_THICKNESS, GROUND_COLOR],
        [4400 + 200, SCREEN_HEIGHT - GROUND_THICKNESS, 2000, GROUND_THICKNESS, GROUND_COLOR],
    ]

    ground_platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in ground_platforms_data]

    #Create obstacles
    obstacles_data = [
        # (x, y, width, height, color)
        # [x , SCREEN_HEIGHT-GROUND_THICKNESS-height, width, height, color]
        [1000, SCREEN_HEIGHT-GROUND_THICKNESS-150, 75, 150, COLOR_GRAY],
        [1500, SCREEN_HEIGHT-GROUND_THICKNESS-150, 75, 150, COLOR_GRAY],
        [1750, SCREEN_HEIGHT-GROUND_THICKNESS-250, 75, 250, COLOR_GRAY],

        [3650, SCREEN_HEIGHT-GROUND_THICKNESS-35, 75, 35, COLOR_DARK_BROWN],
        [3650 + 75, SCREEN_HEIGHT-GROUND_THICKNESS-70, 75, 70, COLOR_DARK_BROWN],
        [3650 + 75 * 2, SCREEN_HEIGHT-GROUND_THICKNESS-105, 75, 105, COLOR_DARK_BROWN],
        [3650 + 75 * 3, SCREEN_HEIGHT-GROUND_THICKNESS-140, 75, 140, COLOR_DARK_BROWN],

        [4100, SCREEN_HEIGHT-GROUND_THICKNESS-140, 75, 140, COLOR_DARK_BROWN],
        [4100 + 75, SCREEN_HEIGHT-GROUND_THICKNESS-105, 75, 105, COLOR_DARK_BROWN],
        [4100 + 75 * 2, SCREEN_HEIGHT-GROUND_THICKNESS-70, 75, 70, COLOR_DARK_BROWN],
        [4100 + 75 * 3, SCREEN_HEIGHT-GROUND_THICKNESS-35, 75, 35, COLOR_DARK_BROWN],
    ]

    obstacles = [Obstacles(x, y, width, height, color) for x, y, width, height, color in obstacles_data]

    enemies_data = [
        [1500 - ENEMY_WIDTH, SCREEN_HEIGHT-GROUND_THICKNESS - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_COLOR, ENEMY_SPEED, True]
    ] 

    enemies = [Enemies(x, y, width, height, color, speed, walking_left) for x, y, width, height, color, speed, walking_left in enemies_data]

    lose = False

    return player, enemies, platforms, ground_platforms, obstacles, lose
def main():
    
    # Initialize Pygame
    pygame.init()

    # Set the initial game state
    game_state = START_SCREEN

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platform Game")

    # Initialize player position, velocity, and jump state
    player_x, player_y = 400 - PLAYER_WIDTH / 2, SCREEN_HEIGHT - GROUND_THICKNESS - PLAYER_HEIGHT
    player_vel_y = 0
    onGround = False
    isJumping = False
    isMoving = False

    player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, player_vel_y, PLAYER_SPEED, onGround, isJumping, isMoving)

    # Initialize enenmy states
    walking_left = True

    # Create platforms
    platforms_data = [
        # (x, y, width, height, color)
        [450, 400, 200, PLATFORM_THICKNESS, COLOR_BROWN],
        [2500, 400, 200, PLATFORM_THICKNESS, COLOR_BROWN],
        [2800, 300, 200, PLATFORM_THICKNESS, COLOR_BROWN],
    ]

    platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in platforms_data]

    ground_platforms_data = [
        # (x, y, width, height, color)
        [0, SCREEN_HEIGHT - GROUND_THICKNESS, 2000, GROUND_THICKNESS, GROUND_COLOR],
        [2000 + 200, SCREEN_HEIGHT - GROUND_THICKNESS, 2200, GROUND_THICKNESS, GROUND_COLOR],
        [4400 + 200, SCREEN_HEIGHT - GROUND_THICKNESS, 2000, GROUND_THICKNESS, GROUND_COLOR],
    ]

    ground_platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in ground_platforms_data]

    #Create obstacles
    obstacles_data = [
        # (x, y, width, height, color)
        # [x , SCREEN_HEIGHT-GROUND_THICKNESS-height, width, height, color]
        [1000, SCREEN_HEIGHT-GROUND_THICKNESS-150, 75, 150, COLOR_GRAY],
        [1500, SCREEN_HEIGHT-GROUND_THICKNESS-150, 75, 150, COLOR_GRAY],
        [1750, SCREEN_HEIGHT-GROUND_THICKNESS-250, 75, 250, COLOR_GRAY],

        [3650, SCREEN_HEIGHT-GROUND_THICKNESS-35, 75, 35, COLOR_DARK_BROWN],
        [3650 + 75, SCREEN_HEIGHT-GROUND_THICKNESS-70, 75, 70, COLOR_DARK_BROWN],
        [3650 + 75 * 2, SCREEN_HEIGHT-GROUND_THICKNESS-105, 75, 105, COLOR_DARK_BROWN],
        [3650 + 75 * 3, SCREEN_HEIGHT-GROUND_THICKNESS-140, 75, 140, COLOR_DARK_BROWN],

        [4100, SCREEN_HEIGHT-GROUND_THICKNESS-140, 75, 140, COLOR_DARK_BROWN],
        [4100 + 75, SCREEN_HEIGHT-GROUND_THICKNESS-105, 75, 105, COLOR_DARK_BROWN],
        [4100 + 75 * 2, SCREEN_HEIGHT-GROUND_THICKNESS-70, 75, 70, COLOR_DARK_BROWN],
        [4100 + 75 * 3, SCREEN_HEIGHT-GROUND_THICKNESS-35, 75, 35, COLOR_DARK_BROWN],
    ]

    obstacles = [Obstacles(x, y, width, height, color) for x, y, width, height, color in obstacles_data]

    enemies_data = [
        [1500 - ENEMY_WIDTH, SCREEN_HEIGHT-GROUND_THICKNESS - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_COLOR, ENEMY_SPEED, True]
    ] 

    enemies = [Enemies(x, y, width, height, color, speed, walking_left) for x, y, width, height, color, speed, walking_left in enemies_data]

    font = pygame.font.Font(None, 36) 
    # Game loop
    running = True
    lose = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get the keys currently pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

        if game_state == START_SCREEN:
            # Display the starting screen and wait for a key press to start the game
            draw_start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            pygame.display.update()

            if keys[pygame.K_KP_ENTER]:
                game_state = PLAYING  # Transition to the playing state

        # Game logic
        elif game_state == PLAYING:
            if CheckLoseCondition(lose):
                game_state = START_SCREEN
                player, enemies, platforms, ground_platforms, obstacles, lose = reset_game()
            # Handle jumping
            if keys[pygame.K_SPACE] and player.onGround:
                player.jumping = True
                player.vel_y = JUMP_STRENGTH

            if not player.onGround:
                player.vel_y += GRAVITY

            if player.onGround:
                player.jumping = False

            player.y += player.vel_y 

            player.onGround = False

            # Check for collisions on platforms
            for platform in platforms:
                if not keys[pygame.K_s]:
                    if CheckCollisionPlatforms(platform, player):
                        player.y = platform.y - player.height
                        player.onGround = True

            # Check for collisions on ground
            for ground in ground_platforms:
                if CheckCollisionPlatforms(ground, player):
                        player.y = ground.y - player.height
                        player.onGround = True

            # Check for collisions with obstacles and check collisions for enemies with obstacles
            for obstacle in obstacles:
                if CheckCollisionObstacles(obstacle, player) == "T":
                    player.y = obstacle.y - player.height
                    player.onGround = True

                elif CheckCollisionObstacles(obstacle, player) == "LW":
                    player.x = obstacle.x - player.width 

                elif CheckCollisionObstacles(obstacle, player) == "RW":
                    player.x = obstacle.x + obstacle.width   

                
                for enemy in enemies:
                    if CheckCollisionObstacles(obstacle, enemy) == "RW":
                        enemy.walking_left = False
                        enemy.x = obstacle.x + obstacle.width
                    if CheckCollisionObstacles(obstacle, enemy) == "LW":
                        enemy.walking_left = True
                        enemy.x = obstacle.x - enemy.width     

            # Check for collisions with enemies
            for enemy in enemies:
                if CheckCollisionObstacles(enemy, player) in ["T", "LW", "RW"]:
                    lose = True


            # Move player
            if keys[pygame.K_q]:
                if player.x > 0:
                    player.x -= PLAYER_SPEED

            # Move objects
            if keys[pygame.K_d]:
                if player.x > SCREEN_WIDTH / 2:
                    player.isMoving = True
                    for platform in platforms:
                        platform.x -= PLAYER_SPEED
                    for ground in ground_platforms:
                        ground.x -= PLAYER_SPEED
                    for obstacle in obstacles:
                        obstacle.x -= PLAYER_SPEED
                    MoveEnemy(enemies, player)
                else:
                    player.isMoving = False
                    player.x += PLAYER_SPEED
                    MoveEnemy(enemies, player)
            else:
                player.isMoving = False
                MoveEnemy(enemies, player)
                        
            if player.y > (SCREEN_HEIGHT - player.height * 1.5):
                lose = True
                
            # Color the screen blue
            screen.fill(SCREEN_COLOR)

            # Draw the platforms and remove them if they go off screen (plus a buffer so that enemies don't disappear too early)
            for platform in platforms:
                if platform.x + platform.width < -300:
                    platforms.remove(platform)
                else:
                    platform.draw(screen)

            for ground in ground_platforms:
                if ground.x + ground.width < -300:
                    ground_platforms.remove(ground)
                else:
                    ground.draw(screen)
            
            for obstacle in obstacles:
                if obstacle.x + obstacle.width < -300:
                    obstacles.remove(obstacle)
                else:
                    obstacle.draw(screen)
            
            for enemy in enemies:
                if enemy.x + enemy.width < -300:
                    enemies.remove(enemy)
                else:
                    enemy.draw(screen)

            # Draw the player
            player.draw(screen)

            pygame.display.update()
                
    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()