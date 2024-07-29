import pygame
import math
import random
import GameState
#hello
pygame.init()
pygame.font.init()

# CONSTANTS
SCREEN_LENGTH = 1200
SCREEN_HEIGHT = 700
PADDLE_SPEED_Y = 1
BALL_LEVEL = 1
BALL_SPEED = 1
ORI_BALL_SPEED = BALL_SPEED
TEXT_FONT_42 = pygame.font.Font("./AmericanCaptain-MdEY.otf", 42)

# FLAGS
run = True

# TIMERS
clock = pygame.time.Clock()

# OBJECTS
# Game Management Object (GameState.Game)
game = GameState.Game()

# Ball Object (GameState.Ball)
ball_size = 10
ball = GameState.Ball(x=SCREEN_LENGTH // 2 - ball_size // 2, y=SCREEN_HEIGHT // 2 - ball_size // 2, size=ball_size)

# Paddle Objects (GameState.Paddle)
paddle_width = 10
paddle_height = 100
paddle_1 = GameState.Paddle(x=50, y=0, width=paddle_width, height=paddle_height, x_clamp=(0, SCREEN_LENGTH // 2), y_clamp=(0, SCREEN_HEIGHT))
paddle_2 = GameState.Paddle(x=SCREEN_LENGTH - paddle_width - 50, y=0, width=paddle_width, height=paddle_height, x_clamp=(SCREEN_LENGTH // 2, SCREEN_LENGTH), y_clamp=(0, SCREEN_HEIGHT))

# Screen Object (Surface)
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Start Game
while run:
    # Get time (sec) since last frame update
    dt = clock.tick()
    
    # GAME LOOP: Handle Inputs
    for event in pygame.event.get():
        # CHECK - Close button was pressed
        if event.type == pygame.QUIT:
            # FLAG - run lowered
            run = False
        # CHECK - Key was pressed
        elif event.type == pygame.KEYDOWN:
            # CHECK - Key was Spacebar and GAMESTATE is PAUSED
            if event.key == pygame.K_SPACE and game.getState() == "paused":
                # Randomize the ball VECTOR and GAMESTATE set to PLAYING
                dy = random.random() * (BALL_SPEED * 0.3)
                dx = math.sqrt(pow(BALL_SPEED, 2) - pow(dy, 2))
                ball.setSpeed(dx, dy)
                ball.setDir(-1 if random.random() < 0.5 else 1, -1 if random.random() < 0.5 else 1)
                game.nextState()
            
            # CHECK - Key was UP
            if event.key == pygame.K_UP:
                # Set paddle_2 VECTOR to negative PADDLE_SPEED_Y
                paddle_2.setKey(pygame.K_UP)
                paddle_2.setSpeed(0, -PADDLE_SPEED_Y)
            # CHECK - Key was DOWN
            if event.key == pygame.K_UP:
                # Set paddle_2 VECTOR to negative PADDLE_SPEED_Y
                paddle_2.setKey(pygame.K_UP)
                paddle_2.setSpeed(0, -PADDLE_SPEED_Y)

            if event.key == pygame.K_LEFT:
                # Set paddle_2 VECTOR to negative PADDLE_SPEED_Y
                paddle_2.setKey(pygame.K_LEFT)
                paddle_2.setSpeed(0, -PADDLE_SPEED_Y)
            if event.key == pygame.K_RIGHT:
                # Set paddle_2 VECTOR to negative PADDLE_SPEED_Y
                paddle_2.setKey(pygame.K_RIGHT)
                paddle_2.setSpeed(0, PADDLE_SPEED_Y)

            elif event.key == pygame.K_DOWN:
                # Set paddle_2 VECTOR to positive PADDLE_SPEED_Y
                paddle_2.setKey(pygame.K_DOWN)
                paddle_2.setSpeed(0, PADDLE_SPEED_Y)
                
            # CHECK - Key was W
            if event.key == pygame.K_w:
                # Set paddle_1 VECTOR to negative PADDLE_SPEED_Y
                paddle_1.setKey(pygame.K_w)
                paddle_1.setSpeed(0, -PADDLE_SPEED_Y)

            if event.key == pygame.K_a:
                # Set paddle_1 VECTOR to negative PADDLE_SPEED_Y
                paddle_1.setKey(pygame.K_a)
                paddle_1.setSpeed(0, -PADDLE_SPEED_Y)
            # CHECK - Key was S
            if event.key == pygame.K_d:
                # Set paddle_1 VECTOR to positive PADDLE_SPEED_Y
                paddle_1.setKey(pygame.K_d)
                paddle_1.setSpeed(0, PADDLE_SPEED_Y)
            elif event.key == pygame.K_s:
                # Set paddle_1 VECTOR to positive PADDLE_SPEED_Y
                paddle_1.setKey(pygame.K_s)
                paddle_1.setSpeed(0, PADDLE_SPEED_Y)
                
        # CHECK - Key was released
        elif event.type == pygame.KEYUP:
            # CHECK - Key was UP and paddle_2 was moving UP
            if event.key == pygame.K_UP and paddle_2.checkKey(pygame.K_UP):
                # Set paddle_2 VECTOR to 0
                paddle_2.setSpeed(0, 0)
            # CHECK - Key was DOWN and paddle_2 was moving DOWN
            if event.key == pygame.K_DOWN and paddle_2.checkKey(pygame.K_DOWN):
                # Set paddle_2 VECTOR to 0
                paddle_2.setSpeed(0, 0)
            if event.key == pygame.K_LEFT:
                paddle_2.setSpeed(0, 0)
            if event.key == pygame.K_RIGHT:
                paddle_2.setSpeed(0, 0)
                
            # CHECK - Key was UP and paddle_2 was moving UP
            if event.key == pygame.K_w and paddle_1.checkKey(pygame.K_w):
                # Set paddle_1 VECTOR to 0
                paddle_1.setSpeed(0, 0)

            if event.key == pygame.K_a and paddle_1.checkKey(pygame.K_a):
                # Set paddle_1 VECTOR to 0
                paddle_1.setSpeed(0, 0)
            # CHECK - Key was DOWN and paddle_2 was moving DOWN
            if event.key == pygame.K_s and paddle_1.checkKey(pygame.K_s):
                # Set paddle_1 VECTOR to 0
                paddle_1.setSpeed(0, 0)

            if event.key == pygame.K_d and paddle_1.checkKey(pygame.K_d):
                # Set paddle_1 VECTOR to 0
                paddle_1.setSpeed(0, 0)

    # Update Game Objects
    paddle_1.move(dt)       # move paddle_1 based on dt and VECTOR
    paddle_2.move(dt)       # move paddle_2 based on dt and VECTOR
    ball.move(dt)           # move ball based on dt and VECTOR
    
    # Game Logic
    # CHECK - GAMESTATE is PLAYING
    if game.getState() == "playing":
        # CHECK - ball x coordinate is less than 0
        if ball.hitBox()[0] < 0:
            # Set GAMESTATE to PAUSED, Player 1 wins, reset game
            game.nextState()
            game.win(1)
            ball.reset()
        # CHECK - ball x coordinate is more than SCREEN_LENGTH
        elif ball.hitBox()[0] + ball_size > SCREEN_LENGTH:
            # Set GAMESTATE to PAUSED, Player 2 wins, reset game
            game.nextState()
            game.win(2)
            ball.reset()
        # CHECK - ball COLLIDES with paddle_1
        elif ball.hitBox().colliderect(paddle_1.hitBox()):
            # Randomize the ball VECTOR towards the positive x direction
            dy = random.random() * (BALL_SPEED * 0.5)
            dx = math.sqrt(pow(BALL_SPEED, 2) - pow(dy, 2))
            ball.setSpeed(dx, dy)
            ball.setDir(1, -1 if random.random() < 0.5 else 1)
            ball.recieved()
            ball.setPos(paddle_1.getPos()[0] + paddle_width)
            
            # CHECK - Rally is a new interval of 10
            if ball.getRally() / 10 == BALL_LEVEL * 1.0:
                # Increase ball speed
                BALL_SPEED = round(BALL_SPEED + 0.2, 1)
                BALL_LEVEL = BALL_LEVEL + 1
        # CHECK - ball COLLIDES with paddle_2
        elif ball.hitBox().colliderect(paddle_2.hitBox()):
            # Randomize the ball VECTOR towards the negative x direction
            dy = random.random() * (BALL_SPEED * 0.5)
            dx = math.sqrt(pow(BALL_SPEED, 2) - pow(dy, 2))
            ball.setSpeed(dx, dy)
            ball.setDir(-1, -1 if random.random() < 0.5 else 1)
            ball.recieved()
            ball.setPos(paddle_2.getPos()[0] - paddle_width)
            
            # CHECK - Rally is a new interval of 10
            if ball.getRally() / 10 == BALL_LEVEL * 1.0:
                # Increase ball speed
                BALL_SPEED = round(BALL_SPEED + 0.2, 1)
                BALL_LEVEL = BALL_LEVEL + 1
        # CHECK - ball y coordinate is less than 0 or more than SCREEN_HEIGHT
        elif ball.hitBox()[1] < 0 or ball.hitBox()[1] + ball_size > SCREEN_HEIGHT:
            # Make ball VECTOR flip y directions
            ball.flipYDir()
            ball.setPos(None, ball.getY() + ball_size * ball.getYDir())

    # TESTING
    # paddle_1.setPos(paddle_1.x, ball.y)
    # paddle_2.setPos(paddle_2.x, ball.y)

    # Rendering
    display_rally = TEXT_FONT_42.render(str(ball.getRally()), True, (255, 255, 255))        # Rally Tracker
    display_speed = TEXT_FONT_42.render(str(BALL_SPEED) + "x",True, (255, 255, 255))        # Speed Tracker
    display_score = TEXT_FONT_42.render(str(game.getScore()), True, (255, 255, 255))        # Score Tracker
    
    screen.fill((0, 0, 0))                                                                  # Background
    screen.blit(display_rally, ((SCREEN_LENGTH - display_rally.get_width()) // 2, 300))     # Rally Tracker
    screen.blit(display_speed, ((SCREEN_LENGTH - display_speed.get_width()) // 2, 400))     # Rally Tracker
    
    # CHECK - GAMESTATE is PAUSED
    if game.getState() == "paused":
        BALL_SPEED = ORI_BALL_SPEED                                                         # Reset ball speed
        screen.blit(display_score, ((SCREEN_LENGTH - display_score.get_width()) // 2, 500)) # Score Tracker
    pygame.draw.rect(screen, (255, 255, 255), ball.render())                                # Ball
    pygame.draw.rect(screen, (255, 255, 255), paddle_1.render())                            # Paddle 1
    pygame.draw.rect(screen, (255, 255, 255), paddle_2.render())                            # Paddle 2
    pygame.display.update()                                                                 # Update Renders
    
pygame.quit()
