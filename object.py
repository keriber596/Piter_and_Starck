from pygame.sprite import Sprite, collide_rect
from pygame.draw import rect
from pygame import Surface
from pygame.image import load
from pygame.transform import scale


SPEED = 20
GRAVITY = 1
JUMP_POWER = 10


class Player(Sprite):
    def __init__(self, x, y, width=50, height=50):
        Sprite.__init__(self)
        #self.image = load('data/паук/стоит/паук_стоит_направо_1.png')
        self.image = Surface((width, height))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yvel = 0
        self.xvel = 0
        self.onGround = False
        self.count = 0
        self.jump = False

    def new_coord(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, left, right, up, platforms):

        # лево право
        if left or right:
            if left:
                self.xvel = -SPEED
            if right:
                self.xvel = SPEED
        else:
            self.xvel = 0

        # прыжок
        if not self.onGround:
            self.yvel += GRAVITY
            if up and self.count < 1 and self.yvel > 0:
                self.count += 1
                self.yvel += -JUMP_POWER*2

        if up and self.onGround:
            self.jump = True
            self.onGround = False
            self.yvel = -JUMP_POWER*2

        self.onGround = False
        print(self.xvel, left, right)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)


    def collide(self, xvel, yvel, platforms):
        for pl in platforms:
            if collide_rect(self, pl):
                if yvel > 0:
                    self.count = 0
                    self.onGround = True
                    self.rect.bottom = pl.rect.top
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                if xvel < 0:
                    self.rect.left = pl.rect.right
                if xvel > 0:
                    self.rect.right = pl.rect.left


class Background(Sprite):
    def __init__(self, x, y, filename):
        Sprite.__init__(self)
        self.image = scale(load(filename), (int(1080//1.52), int(1080//1.52)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, side):
        pass

class Platform(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self)
        self.image = Surface((width, height))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, side):
        pass
