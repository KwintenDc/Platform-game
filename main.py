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

class Pipes(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

def CheckCollisionPlatforms(platform, player):
    if player.x < platform.x + platform.width and player.x > platform.x - player.width:
        if player.y + player.height > platform.y and player.y + player.height < platform.y + 1:
            return True
    return False

def CheckCollisionPipes(pipe, player):
    if player.x + player.width > pipe.x and player.x < pipe.x + pipe.width:
        if player.y + player.height > pipe.y and player.y + player.height < pipe.y + 1:
            return "T"
    if player.x + player.width < pipe.x + pipe.width/2 and player.x + player.width > pipe.x: 
        if player.y + player.height > pipe.y and player.y < pipe.y + pipe.height:
            return "LW"
    if player.x > pipe.x + pipe.width/2 and player.x < pipe.x + pipe.width:
        if player.y + player.height > pipe.y and player.y < pipe.y + pipe.height:
            return "RW"
    return False

def main():
    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN_COLOR = (35, 170, 200)  # Lightblue

    COLOR_WHITE = (255, 255, 255)  # White
    COLOR_BLACK = (0, 0, 0)  # Black
    COLOR_GRAY = (128, 128, 128)  # Gray
    COLOR_RED = (255, 0, 0)  # Red
    COLOR_GREEN = (0, 255, 0)  # Green
    COLOR_BLUE = (0, 0, 255)  # Blue
    COLOR_YELLOW = (255, 255, 0)  # Yellow
    COLOR_MAGENTA = (255, 0, 255)  # Magenta
    COLOR_CYAN = (0, 255, 255)  # Cyan
    COLOR_BROWN = (231, 90, 16)

    PLAYER_HEIGHT = 50
    PLAYER_WIDTH = PLAYER_HEIGHT / 2
    PLAYER_COLOR = COLOR_BLUE
    PLAYER_SPEED = 0.25

    PLATFORM_THICKNESS = 40
    PLATFORM_SPEED = 0.05

    GROUND_COLOR = COLOR_GREEN
    GROUND_THICKNESS = 50
    GRAVITY = 0.0008  
    JUMP_STRENGTH = -0.5  

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platform Test")

    # Initialize player position, velocity, and jump state
    player_x, player_y = 400 - PLAYER_WIDTH / 2, SCREEN_HEIGHT - GROUND_THICKNESS - PLAYER_HEIGHT
    player_vel_y = 0
    onGround = False
    jumping = False

    player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, player_vel_y, PLAYER_SPEED, onGround, jumping)

    # Create platforms
    platforms_data = [
        # (x, y, width, height, color, speed)
        [100.0, 400.0, 200.0, PLATFORM_THICKNESS, COLOR_BROWN],
        [400.0, 300.0, 200.0, PLATFORM_THICKNESS, COLOR_BROWN],
        [200.0, 200.0, 200.0, PLATFORM_THICKNESS, COLOR_BROWN],
        [500.0, 100.0, 200.0, PLATFORM_THICKNESS, COLOR_BROWN],
    ]

    platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in platforms_data]

    ground_platforms_data = [
        [0, SCREEN_HEIGHT - GROUND_THICKNESS, SCREEN_WIDTH, GROUND_THICKNESS, GROUND_COLOR],
        [SCREEN_WIDTH + 100, SCREEN_HEIGHT - GROUND_THICKNESS, SCREEN_WIDTH, GROUND_THICKNESS, GROUND_COLOR],
        [(SCREEN_WIDTH + 100) *2, SCREEN_HEIGHT - GROUND_THICKNESS, SCREEN_WIDTH, GROUND_THICKNESS, GROUND_COLOR],
        [(SCREEN_WIDTH + 100) *3, SCREEN_HEIGHT - GROUND_THICKNESS, SCREEN_WIDTH, GROUND_THICKNESS, GROUND_COLOR],
    ]

    ground_platforms = [Platform(x, y, width, height, color) for x, y, width, height, color in ground_platforms_data]

    #Create pipes
    pipes_data = [
        [1000, SCREEN_HEIGHT-GROUND_THICKNESS-100, 50, 100, COLOR_GRAY],
        [1250, SCREEN_HEIGHT-GROUND_THICKNESS-200, 50, 200, COLOR_GRAY],
        [1500, SCREEN_HEIGHT-GROUND_THICKNESS-300, 50, 300, COLOR_GRAY],
    ]

    pipes = [Pipes(x, y, width, height, color) for x, y, width, height, color in pipes_data]


    font = pygame.font.Font(None, 36)  # You can choose the font and size you prefer
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
        for platform in platforms:
            if not keys[pygame.K_s]:
                if CheckCollisionPlatforms(platform, player):
                    player.y = platform.y - player.height
                    player.onGround = True
                    if player.jumping:
                        player.vel_y = 0

        for ground in ground_platforms:
            if CheckCollisionPlatforms(ground, player):
                    player.y = ground.y - player.height
                    player.onGround = True
                    if player.jumping:
                        player.vel_y = 0
        for pipe in pipes:
            if CheckCollisionPipes(pipe, player) == "T":
                player.y = pipe.y - player.height
                player.onGround = True
                if player.jumping:
                    player.vel_y = 0
            elif CheckCollisionPipes(pipe, player) == "LW":
                player.x = pipe.x - player.width
                player.onGround = True
                if player.jumping:
                    player.vel_y = 0
            elif CheckCollisionPipes(pipe, player) == "RW":
                player.x = pipe.x + pipe.width
                player.onGround = True
                if player.jumping:
                    player.vel_y = 0

        # Move player
        if(keys[pygame.K_q]):
            if(player.x > 0):
                player.x -= PLAYER_SPEED

        # Move objects
        if keys[pygame.K_d]:
            if(player.x > SCREEN_WIDTH / 2):
                for platform in platforms:
                    platform.x -= PLAYER_SPEED
                for ground in ground_platforms:
                    ground.x -= PLAYER_SPEED
                for pipe in pipes:
                    pipe.x -= PLAYER_SPEED
            else:
                player.x += PLAYER_SPEED

        if player.y > (SCREEN_HEIGHT - player.height):
            running = False
            print("You lose!")
            
        # Color the screen blue
        screen.fill(SCREEN_COLOR)

        # Draw the platforms
        for platform in platforms:
            if(platform.x + platform.width < 0):
                platforms.remove(platform)
            else:
                pygame.draw.rect(
                    screen, platform.color, (int(platform.x), int(platform.y), int(platform.width), int(platform.height))
                )

        for ground in ground_platforms:
            if(ground.x + ground.width < 0):
                ground_platforms.remove(ground)
            else:
                pygame.draw.rect(
                    screen, ground.color, (int(ground.x), int(ground.y), int(ground.width), int(ground.height))
                )
        
        for pipe in pipes:
            if(pipe.x + pipe.width < 0):
                pipes.remove(pipe)
            else:
                pygame.draw.rect(
                    screen, pipe.color, (int(pipe.x), int(pipe.y), int(pipe.width), int(pipe.height))
                )

        # Draw the player
        player.draw(screen)

        # Create a text surface with the player's coordinates
        text = font.render(f"Player: ({int(player.x)}, {int(player.y)})", True, (255, 255, 255))

        # Blit (copy) the text surface onto the game window at the desired position (e.g., top left corner)
        screen.blit(text, (10, 10))

        # Update the display
        # pygame.display.flip()
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()