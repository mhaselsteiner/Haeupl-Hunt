import pygame
import random
import os

WIDTH = 480
HEIGHT = 480
FPS = 10 #frames per second
#define colors

WHITE =(255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#set up assest
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

pygame.init()
pygame.mixer.init() # initializes sound

#drawing text in screen
font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size, x ,y ):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #True sets anti alias (blurs pixel at the edges of letters -> text looks smoother)
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"Hauplheld.png" )).convert()
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(GREEN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH -100, HEIGHT -100)
        self.rect.bottom = HEIGHT - 10
        self.y_speed = 0
        self.x_speed = 0

    def update(self):
        self.y_speed = 0
        self.x_speed = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x_speed = -5
        if keystate[pygame.K_RIGHT]:
            self.x_speed = 5
        if keystate[pygame.K_UP]:
            self.y_speed = -5
        if keystate[pygame.K_DOWN]:
            self.y_speed = 5


        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top >= HEIGHT - 80:
            self.rect.top = HEIGHT - 80
        if self.rect.bottom <= 0 + 80:
            self.rect.bottom = 0 + 80



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"gammel.png" )).convert()
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(GREEN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -1
        if self.rect.top < 200:
            self.y_speed = 1

        if self.rect.left > WIDTH:
            self.rect.right = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        grammel = "grammel" + str(random.randint(1,6)) + ".png"
        self.image = pygame.image.load(os.path.join(img_folder,grammel )).convert()
        self.image .set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = -2
    def update(self):
        self.rect.y +=self.y_speed
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()

class Knedl(pygame.sprite.Sprite):
    typ = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.typ = random.randint(1, 6)
        knedl = "knedl" + str(self.typ) + ".png"
        self.image = pygame.image.load(os.path.join(img_folder,knedl )).convert()
        self.image .set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(10,HEIGHT - 20)
        self.rect.centerx = random.randint(10,WIDTH- 20)
        #self.y_speed = random.randint(-6,6)
        #self.x_speed = random.randint(-6,6)
    def update(self):
        self.rect.y = self.rect.y
        self.rect.x =   self.rect.x
        #self.rect.y += self.y_speed
        #self.rect.x += self.x_speed
        #self.y_speed = random.randint(-6, 6)
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Haeupl Hunt")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group( )
knedln = pygame.sprite.Group( )
gammelgrammel = Enemy()
player = Player()
all_sprites.add(gammelgrammel, player)
enemies.add(gammelgrammel)
knedl = Knedl()
knedln.add(knedl)
all_sprites.add(knedl)
#Game loop
running = True
score = 0
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    knedl = Knedl()
    knedln.add(knedl)
    all_sprites.add(knedl)
	#process input
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running =  False
        elif (random.randint(0,600) / 5) >0:
            gammelgrammel.shoot()
	#update
    all_sprites.update()
    knedln.update()
    #check to see if enemy got player
    hits = pygame.sprite.spritecollide(player,enemies,False) #bool sets if sprite should be deleted
    if hits:
        running = False
    # check to see if grammel player
    hits = pygame.sprite.spritecollide(player, bullets, False)  # bool sets if sprite should be deleted
    if hits:
        running = False
    #check to see if we collected some tokens (ate knoedl)
    hits = pygame.sprite.spritecollide(player, knedln, True)  # bool sets if sprite should be deleted
    if hits:
        for that_knedl in knedln:
            score += that_knedl.typ


    hits = pygame.sprite.spritecollide(gammelgrammel, knedln, True)  # bool sets if sp



	#draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen,str(score), 18, WIDTH / 2, 10)

    #after drwing flip display
    pygame.display.flip() # shows new screen graphics

pygame.quit()