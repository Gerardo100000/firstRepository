import pygame

class Game:
    def __init__(self):
        self.states = ("paused", "playing")
        self.state = 0
        self.score_1 = 0
        self.score_2 = 0
        self.winner = None
        
    def getScore(self):
        return str(self.score_1) + " : " + str(self.score_2)
        
    def win(self, player):
        self.winner = player
        if player == 1:
            self.score_1 += 1
        else:
            self.score_2 += 1
    
    def nextState(self):
        self.state = (self.state + 1) % len(self.states)
        
        if self.getState() == "playing":
            self.winner = None
        
    def getState(self):
        return self.states[self.state]

class Ball:
    def __init__(self, x=0, y=0, size=10):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.xdir = 1
        self.ydir = 1
        self.size = size
        self.rally = 0
        self.state = [x, y, self.dx, self.dy, self.xdir, self.ydir, size, self.rally]
        
    def reset(self):
        self.x = self.state[0]
        self.y = self.state[1]
        self.dx = self.state[2]
        self.dy = self.state[3]
        self.xdir = self.state[4]
        self.ydir = self.state[5]
        self.size = self.state[6]
        self.rally = self.state[7]
        
    def getY(self):
        return self.y
    
    def getYDir(self):
        return self.ydir
        
    def recieved(self):
        self.rally = self.rally + 1
        
    def getRally(self):
        return self.rally
        
    def flipYDir(self):
        self.ydir = -1 * self.ydir
        
    def setDir(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir
        
    def hitBox(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
            
    def setSpeed(self, dx, dy):
        self.dx = dx
        self.dy = dy
        
    def move(self, dt):
        self.x = self.x - self.dx * dt if self.xdir < 0 else self.x + self.dx * dt
        self.y = self.y - self.dy * dt if self.ydir < 0 else self.y + self.dy * dt
        
    def setPos(self, x=None, y=None):
        self.x = x if x else self.x
        self.y = y if y else self.y
    
    def render(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
class Paddle:
    def __init__(self, x=0, y=0, width=10, height=100, x_clamp=(0,1), y_clamp=(0,1)):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height
        self.y_clamp = y_clamp
        self.x_clamp = x_clamp
        self.key = None
        
    def hitBox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def setKey(self, key):
        self.key = key
        
    def checkKey(self, key):
        return key == self.key
        
    def getPos(self):
        return (self.x, self.y)
    
    def setSpeed(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    def move(self, dt):
        self.x = max(self.x_clamp[0], min(self.x_clamp[1] - self.width, self.x + self.dx * dt))
        self.y = max(self.y_clamp[0], min(self.y_clamp[1] - self.height, self.y + self.dy * dt))
        
    def setPos(self, x, y):
        self.x = x
        self.y = y

    def decel(self):
        print("E")

    def render(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)