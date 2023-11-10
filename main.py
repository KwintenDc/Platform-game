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
    def __init__(self, x, y, width, height, color, vel_y, speed, onGround, jumping):
        super().__init__(x, y, width, height, color)
        self.vel_y = vel_y
        self.speed = speed
        self.onGround = onGround
        self.jumping = jumping

class Platform(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Obstacles(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

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

def main():
    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN_COLOR = (35, 170, 200)  # Lightblue

    COLOR_WHITE = (255, 255, 255)  
    COLOR_BLACK = (0, 0, 0)  
    COLOR_GRAY = (128, 128, 128)  
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0) 
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

    PLATFORM_THICKNESS = 40

    GROUND_COLOR = COLOR_GREEN
    GROUND_THICKNESS = 50
    GRAVITY = 0.0008            # Acceleration due to gravity
    JUMP_STRENGTH = -0.5        # Negative because y-axis is flipped

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platform Game")

    # Initialize player position, velocity, and jump state
    player_x, player_y = 400 - PLAYER_WIDTH / 2, SCREEN_HEIGHT - GROUND_THICKNESS - PLAYER_HEIGHT
    player_vel_y = 0
    onGround = False
    jumping = False

    player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, player_vel_y, PLAYER_SPEED, onGround, jumping)

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
        [2000 + 200, SCREEN_HEIGHT - GROUND_THICKNESS, 1950, GROUND_THICKNESS, GROUND_COLOR],
        [4150 + 200, SCREEN_HEIGHT - GROUND_THICKNESS, 1950, GROUND_THICKNESS, GROUND_COLOR],
    ]

    ground_platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in ground_platforms_data]

    #Create obstacles
    obstacles_data = [
        # (x, y, width, height, color)
        # [x , SCREEN_HEIGHT-GROUND_THICKNESS-height, width, height, color]
        [1000, SCREEN_HEIGHT-GROUND_THICKNESS-150, 75, 150, COLOR_GRAY],
        [1250, SCREEN_HEIGHT-GROUND_THICKNESS-150, 75, 150, COLOR_GRAY],
        [1500, SCREEN_HEIGHT-GROUND_THICKNESS-250, 75, 250, COLOR_GRAY],

        [3400, SCREEN_HEIGHT-GROUND_THICKNESS-35, 75, 35, COLOR_DARK_BROWN],
        [3400 + 75, SCREEN_HEIGHT-GROUND_THICKNESS-70, 75, 70, COLOR_DARK_BROWN],
        [3400 + 75 * 2, SCREEN_HEIGHT-GROUND_THICKNESS-105, 75, 105, COLOR_DARK_BROWN],
        [3400 + 75 * 3, SCREEN_HEIGHT-GROUND_THICKNESS-140, 75, 140, COLOR_DARK_BROWN],

        [3850, SCREEN_HEIGHT-GROUND_THICKNESS-140, 75, 140, COLOR_DARK_BROWN],
        [3850 + 75, SCREEN_HEIGHT-GROUND_THICKNESS-105, 75, 105, COLOR_DARK_BROWN],
        [3850 + 75 * 2, SCREEN_HEIGHT-GROUND_THICKNESS-70, 75, 70, COLOR_DARK_BROWN],
        [3850 + 75 * 3, SCREEN_HEIGHT-GROUND_THICKNESS-35, 75, 35, COLOR_DARK_BROWN],
    ]

    obstacles = [Obstacles(x, y, width, height, color) for x, y, width, height, color in obstacles_data]

    font = pygame.font.Font(None, 36) 
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the keys currently pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

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

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if CheckCollisionObstacles(obstacle, player) == "T":
                player.y = obstacle.y - player.height
                player.onGround = True

            elif CheckCollisionObstacles(obstacle, player) == "LW":
                player.x = obstacle.x - player.width 

            elif CheckCollisionObstacles(obstacle, player) == "RW":
                player.x = obstacle.x + obstacle.width        

        # Move player
        if keys[pygame.K_q]:
            if player.x > 0:
                player.x -= PLAYER_SPEED

        # Move objects
        if keys[pygame.K_d]:
                if player.x > SCREEN_WIDTH / 2:
                    for platform in platforms:
                        platform.x -= PLAYER_SPEED
                    for ground in ground_platforms:
                        ground.x -= PLAYER_SPEED
                    for obstacle in obstacles:
                        obstacle.x -= PLAYER_SPEED
                else:
                    player.x += PLAYER_SPEED

        if player.y > (SCREEN_HEIGHT - player.height):
            running = False
            print("You lose!")
            
        # Color the screen blue
        screen.fill(SCREEN_COLOR)

        # Draw the platforms and remove them if they go off screen
        for platform in platforms:
            if platform.x + platform.width < 0:
                platforms.remove(platform)
            else:
                pygame.draw.rect(
                    screen, platform.color, (int(platform.x), int(platform.y), int(platform.width), int(platform.height))
                )

        for ground in ground_platforms:
            if ground.x + ground.width < 0:
                ground_platforms.remove(ground)
            else:
                pygame.draw.rect(
                    screen, ground.color, (int(ground.x), int(ground.y), int(ground.width), int(ground.height))
                )
        
        for obstacle in obstacles:
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)
            else:
                pygame.draw.rect(
                    screen, obstacle.color, (int(obstacle.x), int(obstacle.y), int(obstacle.width), int(obstacle.height))
                )

        # Draw the player
        player.draw(screen)

        # Create a text surface with the player's coordinates
        text = font.render(f"Player: ({int(player.x)}, {int(player.y)})", True, (255, 255, 255))

        # Blit (copy) the text surface onto the game window at the desired position (e.g., top left corner)
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()