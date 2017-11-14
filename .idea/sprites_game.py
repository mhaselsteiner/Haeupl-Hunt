import pygame
import random
import os

WIDTH = 1200
HEIGHT = 724
FPS = 30 #frames per second
#define colors

WHITE =(255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#set up assest
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_dir = os.path.join(game_folder,"sound")


pygame.init()
pygame.mixer.init() # initializes sound
random.seed()
# init osund: sound can be converted from mp4 via command line :avconv -i sound.mp4 -vn -f wav sound.wav

speiben_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'speiben.wav'))
heast_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'heast.wav'))
gscheiderfetzn_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'gscheiderfetzn.wav'))
saperlott_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'saperlott.wav'))
guadertropfen_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'guadertropfen.wav'))

story_intro_en = pygame.mixer.Sound(os.path.join(snd_dir, 'intro_englisch.wav'))
gammelintro_sound_en = pygame.mixer.Sound(os.path.join(snd_dir, 'gammelenglisch.wav'))
story_intro_de = pygame.mixer.Sound(os.path.join(snd_dir, 'intro_deutsch.wav'))
gammelintro_sound_de = pygame.mixer.Sound(os.path.join(snd_dir, 'gammelintro.wav'))


#loasd images
bg=pygame.image.load(os.path.join(img_folder, "rathaus.png"))
#drawing text in screen
font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size, x ,y ):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #True sets anti alias (blurs pixel at the edges of letters -> text looks smoother)
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    speed = 4
    calm_down_time = 0
    sober_up_time = 0
    spritzer_count = 0
    anger = False
    drunk = False
    puking = False
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.michihappy
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 28
        #pygame.draw.circle(self.image,BLUE,self.rect.center , self.radius)
        self.rect.center = (WIDTH -100, HEIGHT -100)
        self.rect.bottom = HEIGHT - 10
        self.y_speed = 0
        self.x_speed = 0
        self.last_update = 0
        self.frame_rate_puke = 300  # speed of animation
        self.current_frame = 1

    def load_images(self):
        self.michihappy = pygame.image.load(os.path.join(img_folder, "michihappy.png")).convert()
        self.michispeibt = []
        for i in range(6):
            filename = 'speiben{}.png'.format(i)
            frame = pygame.image.load(os.path.join(img_folder, filename)).convert()
            self.michispeibt.append(frame)

        self.michiboes = pygame.image.load(os.path.join(img_folder, "michiboes.png")).convert()

    def animate(self):
        if self.puking:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate_puke:
                self.last_update = now
                # pygame.time.wait(300)

                if self.current_frame == len(self.michispeibt):
                    self.image = self.michihappy
                    self.puking = False
                    self.current_frame = 1
                else:
                    self.image = self.michispeibt[self.current_frame]
                    self.current_frame += 1
        elif self.anger:
            self.image = self.michiboes

        else:
            self.image = self.michihappy

        self.image.set_colorkey(WHITE)




    def update(self):
        self.y_speed = 0
        self.x_speed = 0
        self.animate()


        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x_speed = - self.speed
        if keystate[pygame.K_RIGHT]:
            self.x_speed = self.speed
        if keystate[pygame.K_UP]:
            self.y_speed = - self.speed
        if keystate[pygame.K_DOWN]:
            self.y_speed = self.speed
        if pygame.time.get_ticks() > self.sober_up_time:
            self.drunk = False
            self.spritzer_count = 0
            self.speed = 4


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

    def getdrunk(self):
        self.drunk = True
        self.spritzer_count += 1
        self.sober_up_time = 15 * 1e3 + pygame.time.get_ticks()
        if self.spritzer_count == 1:
            self.speed += 1
            guadertropfen_sound.play()

        elif self.spritzer_count == 8:
                self.speed += 1
                gscheiderfetzn_sound.play()
        else:
            self.speed += 1

    def puke(self):
        self.puking = True
        speiben_sound.play()
        self.drunk = False
        pygame.time.delay(2000)
        self.spritzer_count = 0
        if self.speed >= 2:
            self.speed = self.speed - 2
        else:
            self.speed = 0


    def  angry(self):
        self.calm_down_time =  4 * 1e3 + pygame.time.get_ticks()
        self.anger = True
        self.shout = True
        self.image = self.michiboes
        if self.shout:
           # if random.randint(0, 3) == 2:
            heast_sound.play()
            #else:
             #   saperlott_sound.play()

        self.shout = False
        if self.speed >= 2:
            self.speed = self.speed - 2
        else:
            self.speed = 1
        pygame.time.delay(2000)


        #self.rect = self.image.get_rect()



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"gammel2.png" )).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 400)
        self.radius = 160
        #pygame.draw.circle(self.image, BLUE, (400- self.radius, 400- self.radius), self.radius)
        self.y_speed = 2

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 10:
            self.y_speed = - self.y_speed
        if self.rect.top < 20:
            self.y_speed = - self.y_speed

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
        self.radius = self.rect.width / 2
        self.rect.bottom = y + 30
        self.rect.centerx = x + 30
        self.y_speed =  random.randint(-8, 8)
        self.x_speed = 10
    def update(self):
        self.rect.y +=self.y_speed
        self.rect.x += self.x_speed
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()

class Knedl(pygame.sprite.Sprite):
    typ = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.typ = random.randint(1, 4)
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



class Spritzer(pygame.sprite.Sprite):
    typ = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.typ = random.randint(1, 4)
        flasche = "spritzer.png"
        self.image = pygame.image.load(os.path.join(img_folder,flasche )).convert()
        self.image .set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(10,HEIGHT - 20)
        self.rect.centerx = random.randint(10,WIDTH- 20)

    def update(self):
        self.rect.y = self.rect.y
        self.rect.x = self.rect.x
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()



def show_game_over_screen():
    draw_text(screen, "OIS AUS! OIS OASCH!!",40, WIDTH/2, HEIGHT/2)
    draw_text(screen,"Waunst no amoi spuen wuest, druck a Tastn", 20, WIDTH / 2, HEIGHT / 1.5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False



def show_start_screen(language):
    draw_text(screen, "Willkommen in Wien!", 40, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "To switch to english please press 'E'", 20, WIDTH / 2, HEIGHT / 1.5)
    pygame.display.flip()
    waiting = True
    now=pygame.time.get_ticks()
#    chan1 = pygame.mixer.Channel()
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.key.get_pressed()[pygame.K_s]:
                pygame.mixer.stop()
                waiting = False
#            if event.type == endint:
 #               waiting == False

            if event.type == pygame.key.get_pressed()[pygame.K_e]:
                language = "en"
                if not pygame.mixer.get_busy():
                    #chan1= \
                    story_intro_en.play()
                   # endint = chan1.get_endevent()
            if pygame.time.get_ticks() > now + 100:
                waiting = False

            else:
                if not pygame.mixer.get_busy():
                    #chan1 = \
                    story_intro_de.play()
                    #endint = chan1.get_endevent()




                #if pygame.time.get_ticks() > now + 21000:






screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Haeupl Hunt")
clock = pygame.time.Clock()




all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group( )
knedln = pygame.sprite.Group()
wein = pygame.sprite.Group()
gammelgrammel = Enemy()
player = Player()
all_sprites.add(gammelgrammel, player)
enemies.add(gammelgrammel)
knedl = Knedl()
knedln.add(knedl)
all_sprites.add(knedl)


maxwidthbar=100
speibzahl=12.
game_over = False
running = True
score = 0
intro = False
language = "de"
hitsbuffer =  []
#Game loop


while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    if intro :
        show_start_screen(language)
        pygame.mixer.stop()
        if language == "de":
            gammelintro_sound_de.play()
        elif language=="en":
            gammelintro_sound_en.play()
        pygame.time.wait(6000)
    intro = False


	#process input
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running =  False


    if (random.randint(0,600) % 17) == 0:
        gammelgrammel.shoot()
    elif((random.randint(0, 600) / 11) == 0):
        spritzer = Spritzer()
        wein.add(spritzer)
        all_sprites.add(spritzer)
    if (random.randint(0, 600) / 2) == 0:
        knedl = Knedl()
        knedln.add(knedl)
        all_sprites.add(knedl)
        screen.blit(bg, (0, 0))

    #update
    all_sprites.update()
    knedln.update()

    #check to see if enemy got player
    hits = pygame.sprite.spritecollide(player,enemies,False, pygame.sprite.collide_circle) #bool sets if sprite should be deleted
    if hits:
        #running = False
        game_over  = True
    # check to see if grammel hit player
    hits = pygame.sprite.spritecollide(gammelgrammel,knedln,True, pygame.sprite.collide_circle) #bool sets if sprite should be deleted
    hits = pygame.sprite.spritecollide(gammelgrammel,wein,True, pygame.sprite.collide_circle) #bool sets if sprite should be deleted


    hits = pygame.sprite.spritecollide(player, bullets, False, pygame.sprite.collide_circle)
    if hits:
        if not hitsbuffer:
            player.angry()

    if (pygame.time.get_ticks() >= player.calm_down_time) & (player.anger):  # has he clamed down?
        player.anger = False

    hitsbuffer = pygame.sprite.spritecollide(player, bullets, False, pygame.sprite.collide_circle)

        #running = False
    #check to see if we collected some tokens (ate knoedl)
    hits = pygame.sprite.spritecollide(player, knedln, True)  # bool sets if sprite should be deleted
    if hits:
        for that_knedl in hits:
            score += that_knedl.typ
    #hits = pygame.sprite.spritecollide(gammelgrammel, knedln, True)  # bool sets if sp



            # check to see if we collected some tokens (drank spritzer)
    hits = pygame.sprite.spritecollide(player, wein, True)  # bool sets if sprite should be deleted
    if hits:
        player.getdrunk()
        if player.spritzer_count == speibzahl:
            player.puke()
            player.speed = 4
            score = score - 20 # knedl speiben
            #speiben = Speiben(player.rect.center)
            #all_sprites.add(speiben)

	#draw
    #screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, 'Knedl Score: ' + str(score), 18, WIDTH / 2 - 20, 10)
    draw_text(screen, 'Spritzer: ' + str(player.spritzer_count), 18, WIDTH / 2 + 90, 10)
    progress = float(player.spritzer_count) /speibzahl
    pygame.draw.rect(screen, GREEN, pygame.Rect(WIDTH / 2 + 135, 18, maxwidthbar * progress,10))
    pygame.draw.rect(screen,BLACK, pygame.Rect(WIDTH / 2 + 135, 18, maxwidthbar, 10), 1)
    #after drwing flip display
    pygame.display.flip() # shows new screen graphics

    if game_over:
        show_game_over_screen()
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        knedln = pygame.sprite.Group()
        wein = pygame.sprite.Group()
        gammelgrammel = Enemy()
        player = Player()
        all_sprites.add(gammelgrammel, player)
        enemies.add(gammelgrammel)
        knedl = Knedl()
        knedln.add(knedl)
        all_sprites.add(knedl)
        running = True
        score = 0
        intro = False
        hitsbuffer = []
        game_over = False

