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
    def __init__(self, x, y, width, height, sprite_sheet_path, vel_y, speed, onGround, isJumping, MovingDirection):
        self.x, self.y = x, y
        self.vel_y = vel_y
        self.width, self.height = width, height
        self.speed = speed
        self.onGround = onGround
        self.isJumping = isJumping
        self.MovingDirection = MovingDirection
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.previous_direction = "RIGHT"
        self.animationtimer = 0

        self.left_small_walking_frames = []
        self.left_small_standing_frames = []
        self.right_small_walking_frames = []
        self.right_small_standing_frames = []
        self.left_small_jumping_frames = []
        self.right_small_jumping_frames = []

        self.left_small_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(89.5, 0, 15.5, 15.5), (self.width, self.height)))
        self.left_small_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(121, 0, 15.5, 15.5), (self.width, self.height)))
        self.left_small_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(150, 0, 15.5, 15.5), (self.width, self.height)))

        self.left_small_standing_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(181, 0, 15.5, 15.5), (self.width, self.height)))

        self.right_small_standing_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(210, 0, 15.5, 15.5), (self.width, self.height)))

        self.right_small_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(240, 0, 15.5, 15.5), (self.width, self.height)))
        self.right_small_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(270, 0, 15.5, 15.5), (self.width, self.height)))
        self.right_small_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(300, 0, 15.5, 15.5), (self.width, self.height)))

        self.left_small_jumping_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(29, 1, 15.5, 15.5), (self.width, self.height)))

        self.right_small_jumping_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(361, 1, 15.5, 15.5), (self.width, self.height)))

    def draw(self, screen):
        if(self.MovingDirection == "STANDING"):
            if(self.previous_direction == "LEFT"):
                frame = self.left_small_standing_frames[0]
                if(self.isJumping):
                    frame = self.left_small_jumping_frames[0]
            elif(self.previous_direction == "RIGHT"):
                frame = self.right_small_standing_frames[0]
                if(self.isJumping):
                    frame = self.right_small_jumping_frames[0]

        elif(self.MovingDirection == "LEFT"):
            self.previous_direction = "LEFT"
            frame = self.left_small_walking_frames[0]
            if(self.isJumping):
                frame = self.left_small_jumping_frames[0]

        elif(self.MovingDirection == "RIGHT"):
            frame = self.right_small_walking_frames[2]
            self.previous_direction = "RIGHT"
            if(self.isJumping):
                frame = self.right_small_jumping_frames[0]
                
        screen.blit(frame, (self.x, self.y))

class Platform(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Obstacles(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Enemies(GameObject):
    def __init__(self, x, y, width, height, color, speed, walking_left, sprite_sheet_path):
        super().__init__(x, y, width, height, color)
        self.speed = speed
        self.walking_left = walking_left
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.previous_direction = "RIGHT"

        self.left_walking_frames = []
        self.right_walking_frames = []

        self.left_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(149.5, 119, 18, 25), (self.width, self.height)))

        self.right_walking_frames.append(pygame.transform.scale(self.sprite_sheet.subsurface(179, 119, 18, 25), (self.width, self.height)))

    def draw(self, screen):
        if(self.walking_left == True):
            frame = self.left_walking_frames[0]
        elif(self.walking_left == False):
            frame = self.right_walking_frames[0]
        screen.blit(frame, (self.x, self.y))
        

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
PLAYER_WIDTH = 45
PLAYER_SPEED = 0.25
PLAYER_SPRITE_SHEET_PATH = "smb_mario_sheet.png" 

ENEMY_HEIGHT = 45
ENEMY_WIDTH = 30
ENEMY_COLOR = COLOR_RED
ENEMY_SPEED = 0.10 
ENEMIES_SPRITE_SHEET_PATH = "smb_enemies_sheet.png"

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

def MoveEnemy(enemies, player, objectsMoving):
    for enemy in enemies:
        if player.MovingDirection == "RIGHT":
            if enemy.walking_left == True:
                if player.x < SCREEN_WIDTH / 2:
                    enemy.x -= enemy.speed
                else: 
                    if objectsMoving:
                        enemy.x -= (enemy.speed + player.speed)
                    else:
                        enemy.x -= enemy.speed
            elif enemy.walking_left == False:
                if player.x < SCREEN_WIDTH / 2:
                    enemy.x += enemy.speed
                else:
                    if objectsMoving:
                        enemy.x += enemy.speed - player.speed
                    else:
                        enemy.x += enemy.speed
        else: 
            if enemy.walking_left == True:
                enemy.x -= enemy.speed
            elif enemy.walking_left == False:
                enemy.x += enemy.speed

# TODO : Add more to lose condition
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
    movingDirection = "STANDING"
    objectsMoving = False

    player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPRITE_SHEET_PATH, player_vel_y, PLAYER_SPEED, onGround, isJumping, movingDirection)

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
        [1500 - ENEMY_WIDTH, SCREEN_HEIGHT-GROUND_THICKNESS - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_COLOR, ENEMY_SPEED, True, ENEMIES_SPRITE_SHEET_PATH]
    ] 

    enemies = [Enemies(x, y, width, height, color, speed, walking_left, ENEMIES_SPRITE_SHEET_PATH) for x, y, width, height, color, speed, walking_left, ENEMIES_SPRITE_SHEET_PATH in enemies_data]

    lose = False

    return player, enemies, platforms, ground_platforms, obstacles, lose, objectsMoving
def main():
    
    # Initialize Pygame
    pygame.init()

    # Initialize the clock 
    clock = pygame.time.Clock()

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
    movingDirection = "STANDING"
    objectsMoving = False

    player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPRITE_SHEET_PATH, player_vel_y, PLAYER_SPEED, onGround, isJumping, movingDirection)

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
        [1500 - ENEMY_WIDTH, SCREEN_HEIGHT-GROUND_THICKNESS - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_COLOR, ENEMY_SPEED, True, ENEMIES_SPRITE_SHEET_PATH]
    ] 

    enemies = [Enemies(x, y, width, height, color, speed, walking_left, ENEMIES_SPRITE_SHEET_PATH) for x, y, width, height, color, speed, walking_left, ENEMIES_SPRITE_SHEET_PATH in enemies_data]

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
                player, enemies, platforms, ground_platforms, obstacles, lose, objectsMoving = reset_game()
            # Handle jumping
            if keys[pygame.K_SPACE] and player.onGround:
                player.isJumping = True
                player.vel_y = JUMP_STRENGTH
                player.onGround = False

            if not player.onGround:
                player.vel_y += GRAVITY

            if player.onGround:
                player.isJumping = False

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
                player.MovingDirection = "LEFT"
                if player.x > 0:
                    player.x -= PLAYER_SPEED
                    MoveEnemy(enemies, player, objectsMoving)

            # Move objects
            if keys[pygame.K_d]:
                player.MovingDirection = "RIGHT"
                if player.x > SCREEN_WIDTH / 2:
                    objectsMoving = True
                    for platform in platforms:
                        platform.x -= PLAYER_SPEED
                    for ground in ground_platforms:
                        ground.x -= PLAYER_SPEED
                    for obstacle in obstacles:
                        obstacle.x -= PLAYER_SPEED
                    MoveEnemy(enemies, player, objectsMoving)
                else:
                    player.x += PLAYER_SPEED
                    objectsMoving = False
                    MoveEnemy(enemies, player, objectsMoving)
            
            if not keys[pygame.K_d] and not keys[pygame.K_q]:
                player.MovingDirection = "STANDING"
                MoveEnemy(enemies, player, objectsMoving)
                        
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
            
            # # Put the coordinates of the player on the screen
            # font = pygame.font.Font(None, 36) 
            # text = font.render("x: " + str(player.x) + " y: " + str(player.y), True, (255, 255, 255))
            # screen.blit(text, (0, 0))

            # Tick the clock and update the display (standard 2000)
            clock.tick(4000) 
            pygame.display.update()
                
    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()