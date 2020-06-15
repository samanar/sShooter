import os
import pygame

SCREENWIDTH = 750
SCREENHEIGHT = 480

os.environ['SDL_VIDEO_WINDOW_POS'] = str(SCREENWIDTH // 2) + "," + str(SCREENHEIGHT // 2)
bg = pygame.image.load('./assets/bg.jpg')


class Player:
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
        self.is_standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):

        if self.walk_count + 1 > 27:
            self.walk_count = 0

        if not self.is_standing:
            if self.left:
                win.blit(self.walk_left_pics[self.walk_count // 3], (self.x, self.y))

            elif self.right:
                win.blit(self.walk_right_pics[self.walk_count // 3], (self.x, self.y))

            self.walk_count += 1

        else:
            if self.left:
                win.blit(self.walk_left_pics[0], (self.x, self.y))
            else:
                win.blit(self.walk_right_pics[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # NEW
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # To draw the hit box around the player


class Projectile:
    def __init__(self, x, y, facing):
        # facing 1 --> right
        # facing -1 --> left
        self.x = x
        self.y = y
        self.radius = 6
        self.color = (0, 0, 0)
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy:
    walk_right_pics = [pygame.image.load('./assets/R1E.png'), pygame.image.load('./assets/R2E.png'),
                       pygame.image.load('./assets/R3E.png'),
                       pygame.image.load('./assets/R4E.png'), pygame.image.load('./assets/R5E.png'),
                       pygame.image.load('./assets/R6E.png'),
                       pygame.image.load('./assets/R7E.png'), pygame.image.load('./assets/R8E.png'),
                       pygame.image.load('./assets/R9E.png'),
                       pygame.image.load('./assets/R10E.png'), pygame.image.load('./assets/R11E.png')]
    walk_left_pics = [pygame.image.load('./assets/L1E.png'), pygame.image.load('./assets/L2E.png'),
                      pygame.image.load('./assets/L3E.png'),
                      pygame.image.load('./assets/L4E.png'), pygame.image.load('./assets/L5E.png'),
                      pygame.image.load('./assets/L6E.png'),
                      pygame.image.load('./assets/L7E.png'), pygame.image.load('./assets/L8E.png'),
                      pygame.image.load('./assets/L9E.png'),
                      pygame.image.load('./assets/L10E.png'), pygame.image.load('./assets/L11E.png')]

    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.path = [x, end]
        self.walk_count = 0
        self.velocity = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # NEW

    def draw(self, win):
        self.move()
        if self.walk_count + 1 >= 33:
            self.walk_count = 0

        if self.velocity > 0:
            win.blit(self.walk_right_pics[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            win.blit(self.walk_left_pics[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # NEW
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draws the hit box around the enemy

    def __change_direction(self):
        self.velocity *= -1
        self.walk_count = 0

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.__change_direction()
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.__change_direction()

    def hit(self):
        print('hit')


pygame.init()
win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("sShooter")
clock = pygame.time.Clock()

player = Player(50, 400, 64, 64)
enemy = Enemy(0, 405, SCREENWIDTH - 50)
bullets = []
shoot_loop = 0


def redraw_game_window():
    win.blit(bg, (0, 0))
    player.draw(win)
    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


run = True
while run:
    clock.tick(27)

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 5:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                run = False

    for bullet in bullets:

        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and \
                bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and \
                    bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                enemy.hit()
                bullets.pop(bullets.index(bullet))  # removes bullet from bullet list

        if SCREENWIDTH > bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shoot_loop == 0:
        if len(bullets) < 5:
            direction = 1
            if player.left:
                direction = -1
            bullets.append(
                Projectile(round(player.x + player.width // 2), round(player.y + player.height // 2), direction))

            shoot_loop = 1

    if keys[pygame.K_LEFT] and player.x >= player.velocity:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.is_standing = False

    elif keys[pygame.K_RIGHT] and player.x <= SCREENWIDTH - player.width - player.velocity:
        player.x += player.velocity
        player.left = False
        player.right = True
        player.is_standing = False

    else:
        player.is_standing = True
        walk_count = 0

    if not player.is_jumping:
        if keys[pygame.K_UP]:
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
