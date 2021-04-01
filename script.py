import pygame
pygame.init()

# set width and eight of window
sw = 800
sh = 800

# set the variable for the background of the game
bg = pygame.image.load('starsbg.png')
# set window
win = pygame.display.set_mode((sw, sh))
# set title of game
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

# make the paddle class
class Paddle(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color

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
        self.xv = 0
        self.yv = 5

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
    # insert the ball
    ball.draw(win)
    # loop to draw each brick
    for b in bricks:
        b.draw(win)
    pygame.display.update()

# instaniate the paddle into being
player = Paddle(sw/2 - 50, sh - 100, 100, 20, (255, 255, 255))
ball = Ball(sw/2 - 10, sh - 200, 20, 20, (255, 255, 255))
init()
run = True
while run:
    # determine the frames per second at 100
    clock.tick(100)
    # to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()

pygame.quit()