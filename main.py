import pygame
import os

SCREENWIDTH = 850
SCREENHEIGHT = 480

# initializing pygame
os.environ['SDL_VIDEO_WINDOW_POS'] = str(SCREENWIDTH // 2) + "," + str(SCREENHEIGHT // 2)
pygame.init()

walk_right_pics = [pygame.image.load('./assets/R1.png'), pygame.image.load('./assets/R2.png'),
                   pygame.image.load('./assets/R3.png'), pygame.image.load('./assets/R4.png'),
                   pygame.image.load('./assets/R5.png'), pygame.image.load('./assets/R6.png'),
                   pygame.image.load('./assets/R7.png'), pygame.image.load('./assets/R8.png'),
                   pygame.image.load('./assets/R9.png')]

walk_left_pics = [pygame.image.load('./assets/L1.png'), pygame.image.load('./assets/L2.png'),
                  pygame.image.load('./assets/L3.png'), pygame.image.load('./assets/L4.png'),
                  pygame.image.load('./assets/L5.png'), pygame.image.load('./assets/L6.png'),
                  pygame.image.load('./assets/L7.png'), pygame.image.load('./assets/L8.png'),
                  pygame.image.load('./assets/L9.png')]

standing = pygame.image.load('./assets/standing.png')

bg = pygame.image.load('./assets/bg.jpg')

win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Testing")


class Player:
    def __init__(self, initial_x, initial_y, width, height):
        self.x = initial_x
        self.y = initial_y
        self.width = width
        self.height = height
        self.velocity = 5
        self.left = False
        self.right = False
        self.walk_count = 0
        self.is_jumping = False
        self.jump_count = 10

    def draw(self, win):
        if self.walk_count + 1 > 27:
            self.walk_count = 0
        if self.left:
            win.blit(walk_left_pics[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        elif self.right:
            win.blit(walk_right_pics[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            win.blit(standing, (self.x, self.y))


clock = pygame.time.Clock()

player = Player(50, 400, 64, 64)
run = True


def redraw_game_window():
    win.blit(bg, (0, 0))
    player.draw(win)
    pygame.display.update()


while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x >= player.velocity:
        player.x -= player.velocity
        player.left = True
        player.right = False

    elif keys[pygame.K_RIGHT] and player.x <= SCREENWIDTH - player.width - player.velocity:
        player.x += player.velocity
        player.left = False
        player.right = True

    else:
        player.left = False
        player.right = False
        walk_count = 0

    if not player.is_jumping:
        if keys[pygame.K_SPACE]:
            player.is_jumping = True
            player.left = False
            player.right = False
            walk_count = 0
    else:
        if player.jump_count >= -10:
            player.y -= int((player.jump_count ** 2) * 0.3 * (lambda x: -1 if x < 0 else 1)(player.jump_count))
            player.jump_count -= 1
        else:
            player.is_jumping = False
            player.jump_count = 10

    redraw_game_window()

pygame.quit()
