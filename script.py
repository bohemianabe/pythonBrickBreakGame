import pygame
import random
pygame.init()

# set width and eight of window
sw = 800
sh = 800

# initiate sounds
brickHitSound = pygame.mixer.Sound('bullet.wav')
bounceSound = pygame.mixer.Sound("hitGameSound.wav")
# hitsound too loud lower to 20%
bounceSound.set_volume(.2)

# set the variable for the background of the game
bg = pygame.image.load('starsbg.png')
# set window
win = pygame.display.set_mode((sw, sh))
# set title of game
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()
gameover = False

# make the paddle class
class Paddle(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color
        self.xx = self.x + self.w
        self.xy = self.y + self.h

    # function to draw the paddle on the screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

# make the ball class
class Ball(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        # for the ball i'll need to mess with it's velocity
        self.xv = random.choice([2, 3, -2, -3, -4])
        self.yv = random.randint(3, 4)
        self.xx = self.x + self.w
        self.xy = self.y + self.h


    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])
 
    # function to calculate movement
    def move(self):
        self.x += self.xv
        self.y += self.yv

# make the brick class
class Brick(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.xx = self.x + self.w
        self.xy = self.y + self.h
        # to set up the bricks with extra balls randomly
        self.ranNum = random.randint(0, 10)
        if self.ranNum < 3:
            self.pregnant = True
        else:
            self.pregnant = False 
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

bricks = []
# a function to generate a list of the bricks since there's so many of them
def init():
    # cool way to tell function to edit the global variable, so i can call it later
    global bricks
    bricks = []
    for i in range(6):
        for j in range(10):
            # function to code all the bricks
            bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (120, 205, 250)))


def redrawGameWindow():
    # insert the background
    win.blit(bg, (0, 0))
    # insert the paddle
    player.draw(win)
    # call the new balls
    for ball in balls:
        ball.draw(win)
    # insert the ball
    ball.draw(win)
    # loop to draw each brick
    for b in bricks:
        b.draw(win)
    
    # create font
    font = pygame.font.SysFont('comicsans', 50)
    # what to say if all the bricks are at zero or else
    if gameover:
        if len(bricks) == 0:
            resText = font.render("Congrats!", 1, (255, 255, 255))
        else:
            resText = font.render("That's rough!", 1, (255, 255, 255))
            # sizing the text in porportion to the window
        win.blit(resText, ((sw // 2 - resText.get_width() // 2), sh//2 - resText.get_height()//2))
        # prompt to play again
        playAgainText = font.render("Press Space To Play Again.", 1 , (255, 255, 255))
        win.blit(playAgainText, ((sw//2 - playAgainText.get_width()//2), sh//2 + 30))
    pygame.display.update()

# instaniate the paddle into being
player = Paddle(sw/2 - 50, sh - 100, 140, 20, (0, 255, 155))
ball = Ball(sw/2 - 10, sh - 400, 20, 20, (255, 255, 255))
balls = [ball]
init()
run = True
while run:
    # determine the frames per second at 100
    clock.tick(100)

    # check to see to play game
    if not gameover:
        for ball in balls:
            ball.move()
        # conditional statement to handle where the paddle is on the condition of the mouse's location
        if pygame.mouse.get_pos()[0] - player.w // 2 < 0:
            player.x = 0
        elif pygame.mouse.get_pos()[0] + player.w // 2 > sw:
            player.x = sw - player.w 
        else: 
            player.x = pygame.mouse.get_pos()[0] - player.w // 2

        for ball in balls:
            # conditional statement for the ball movement. check if the ball is between the beginning or end of the paddle. second if checks if the ball.y and paddle.y are colliding
            if (ball.x >= player.x and ball.x <= player.x + player.w) or (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
                if ball.y + ball.h >= player.y and ball.y + ball.h <= player.y + player.h:
                    ball.yv *= -1
                    ball.y = player.y - ball.h - 1
                    bounceSound.play()

            # to keep the ball from exiting the screen
            if ball.x + ball.w >= sw:
                bounceSound.play()
                ball.xv *= -1
            if ball.x < 0:
                bounceSound.play()
                ball.xv *= -1
            if ball.y <= 0:
                bounceSound.play()
                ball.yv *= -1
                

        # for loop to check if their is break contact
        for brick in bricks:
            for ball in balls:
                if (ball.x >= brick.x and ball.x <= brick.x + brick.y) or (ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w):
                    if (ball.y >= brick.y and ball.y < brick.y + brick.h) or (ball.y + ball.h >= brick.y and ball.y + ball.h <= brick.y + brick.h):
                        brick.visible = False
                        if brick.pregnant:
                            balls.append(Ball(brick.x, brick.y, 20, 20, (255, 255, 255)))
                        # bricks.pop(bricks.index(brick))
                        ball.yv *= -1
                        brickHitSound.play()
                        break

        for brick in bricks:
            if brick.visible == False:
                bricks.pop(bricks.index(brick))

        if len(balls) == 0:
            gameover = True 
    

    # get input from key pressed to play game again
    keys = pygame.key.get_pressed()
    if len(bricks) == 0:
        won = True
        gameover = True
    if gameover:
        if keys[pygame.K_SPACE]:
            gameover = False
            won = False
            ball = Ball(sw/2 - 10, sh - 400, 20, 20, (255, 255, 255))
            if len(balls) == 0:
                balls.append(ball)
            # if len(balls) == 0:
            #     balls.append(ball)

            bricks.clear()
            init()
            # for i in range(6):
            #     for j in range(10):
            #         bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (120, 205, 250)))

    # to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()

pygame.quit()