import pygame
import random
import os

WIDTH = 1200
HEIGHT = 724
FPS = 30  #frames per second

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#set up assest
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_dir = os.path.join(game_folder, "sound")

pygame.init()
pygame.mixer.init()  # initializes sound
random.seed()
# init osund: sound can be converted from mp4 via command line :avconv -i sound.mp4 -vn -f wav sound.wav
german_channel = pygame.mixer.Channel(1)
english_channel = pygame.mixer.Channel(2)

speiben_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'speiben.wav'))
heast_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'heast.wav'))
gscheiderfetzn_sound = pygame.mixer.Sound(
    os.path.join(snd_dir, 'gscheiderfetzn.wav'))
guadertropfen_sound = pygame.mixer.Sound(
    os.path.join(snd_dir, 'guadertropfen.wav'))

story_intro_en = pygame.mixer.Sound(
    os.path.join(snd_dir, 'intro_englisch.wav'))
gammelintro_sound_en = pygame.mixer.Sound(
    os.path.join(snd_dir, 'gammelenglisch.wav'))
story_intro_de = pygame.mixer.Sound(os.path.join(snd_dir, 'intro_deutsch.wav'))
gammelintro_sound_de = pygame.mixer.Sound(
    os.path.join(snd_dir, 'gammelintro.wav'))

#loasd images
bg = pygame.image.load(os.path.join(img_folder, "rathaus.png"))
michi = pygame.image.load(os.path.join(img_folder, "michistart.png"))
#drawing text in screen
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y, color=BLACK):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(
        text, True, color
    )  #True sets anti alias (blurs pixel at the edges of letters -> text looks smoother)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    speed = FPS / 7.5
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
        self.rect.center = (WIDTH - 100, HEIGHT - 100)
        self.rect.bottom = HEIGHT - 10
        self.y_speed = 0
        self.x_speed = 0
        self.last_update = 0
        self.frame_rate_puke = FPS / 0.1  # speed of animation
        self.current_frame = 1

    def load_images(self):
        self.michihappy = pygame.image.load(
            os.path.join(img_folder, "michihappy.png")).convert()
        self.michispeibt = []
        for i in range(6):
            filename = 'speiben{}.png'.format(i)
            frame = pygame.image.load(
                os.path.join(img_folder, filename)).convert()
            self.michispeibt.append(frame)

        self.michiboes = pygame.image.load(
            os.path.join(img_folder, "michiboes.png")).convert()

    def animate(self):
        if self.puking:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate_puke:
                self.last_update = now

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
            self.x_speed = -self.speed
        if keystate[pygame.K_RIGHT]:
            self.x_speed = self.speed
        if keystate[pygame.K_UP]:
            self.y_speed = -self.speed
        if keystate[pygame.K_DOWN]:
            self.y_speed = self.speed
        if pygame.time.get_ticks() > self.sober_up_time:
            self.drunk = False
            self.spritzer_count = 0
            self.speed = FPS / 7.5

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
            self.speed += FPS / 30.
            guadertropfen_sound.play()

        elif self.spritzer_count == 8:
            self.speed += FPS / 30.
            gscheiderfetzn_sound.play()
        else:
            self.speed += FPS / 30.

    def puke(self):
        self.puking = True
        speiben_sound.play()
        self.drunk = False
        pygame.time.delay(2000)
        self.spritzer_count = 0
        if self.speed >= FPS / 15.:
            self.speed = self.speed - FPS / 15.
        else:
            self.speed = 0

    def angry(self):
        self.calm_down_time = 4 * 1e3 + pygame.time.get_ticks()
        self.anger = True
        self.shout = True
        self.image = self.michiboes
        if self.shout:
            heast_sound.play()

        self.shout = False
        if self.speed >= FPS / 15.:
            self.speed = self.speed - FPS / 15.
        else:
            self.speed = FPS / 30.
        pygame.time.delay(2000)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_folder, "gammel2.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 400)
        self.radius = 160
        self.y_speed = FPS / 15.
        self.x_speed = FPS / 15.

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 10:
            self.y_speed = -self.y_speed
        if self.rect.top < 20:
            self.y_speed = -self.y_speed

        if self.rect.left > WIDTH:
            self.rect.right = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        grammel = "grammel" + str(random.randint(1, 6)) + ".png"
        self.image = pygame.image.load(
            os.path.join(img_folder, grammel)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width / 2
        self.rect.bottom = y + 30
        self.rect.centerx = x + 30
        self.y_speed = random.randint(-FPS / 3.75, FPS / 3.75)
        self.x_speed = FPS / 3.

    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT
                or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()


class Knedl(pygame.sprite.Sprite):
    typ = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.typ = random.randint(1, 4)
        knedl = "knedl" + str(self.typ) + ".png"
        self.image = pygame.image.load(
            os.path.join(img_folder, knedl)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(10, HEIGHT - 20)
        self.rect.centerx = random.randint(10, WIDTH - 20)

    def update(self):
        self.rect.y = self.rect.y
        self.rect.x = self.rect.x
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT
                or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()


class Spritzer(pygame.sprite.Sprite):
    typ = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.typ = random.randint(1, 4)
        flasche = "spritzer.png"
        self.image = pygame.image.load(
            os.path.join(img_folder, flasche)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(10, HEIGHT - 20)
        self.rect.centerx = random.randint(10, WIDTH - 20)

    def update(self):
        self.rect.y = self.rect.y
        self.rect.x = self.rect.x
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT
                or self.rect.left < 0 or self.rect.right > WIDTH):
            self.kill()


def show_game_over_screen(language='de'):
    pygame.mixer.stop()
    if language == 'de':
        draw_text(
            screen, "OIS AUS! OIS OASCH!!", 80, WIDTH / 2, HEIGHT / 2, color=WHITE)
        draw_text(
            screen,
            "Waunst no amoi spuen wuest, druck a Tastn",
            40,
            WIDTH / 2,
            HEIGHT / 1.5,
            color=WHITE)
    else:
        draw_text(
            screen, "GAME OVER, OIDE!!", 80, WIDTH / 2, HEIGHT / 2, color=WHITE)
        draw_text(
            screen,
            "Press key to play again",
            40,
            WIDTH / 2,
            HEIGHT / 1.5,
            color=WHITE)

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
    draw_text(screen, " For English Intro Press 'e', to skip 's' ", 20,
              WIDTH / 2, 50)
    draw_text(screen, "Willkommen in Wien!", 40, WIDTH / 2, 100)
    draw_text(
        screen,
        "Iss so viele Knedl wie du kannst, und lass dich nicht vom zornigen vergammelten",
        30, WIDTH / 2, 200)
    draw_text(screen,
              " Grammelknedl oder seiner grammeligen Munition erwischen!", 30,
              WIDTH / 2, 250)

    screen.blit(michi, (200, 1000))
    pygame.display.flip()
    waiting = True
    now = pygame.time.get_ticks()
    if language == 'de':
        german_channel.play(story_intro_de)
    else:
        english_channel.play(story_intro_en)
    while pygame.mixer.get_busy():
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pygame.mixer.stop()
                if event.key == pygame.K_e:
                    language = "en"
                    german_channel.stop()
                    english_channel.play(story_intro_en)
    return language


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Haeupl Hunt")
clock = pygame.time.Clock()

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

maxwidthbar = 100
speibzahl = 12.
game_over = False
running = True
score = 0
intro = True
language = "de"
hitsbuffer = []

while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    screen.blit(bg, (0, 0))  #showbg image and place in center

    while intro:
        screen.blit(michi, (WIDTH / 2, HEIGHT - 250))
        language = show_start_screen(language)
        pygame.mixer.stop()
        if language == "de":
            english_channel.play(gammelintro_sound_de)
        elif language == "en":
            german_channel.play(gammelintro_sound_en)
        intro = False

#process input
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running = False

#defines the appearence rates of spritzer, knedl, grammeln

    if (random.randint(0, 600) % 37) == 0:
        gammelgrammel.shoot()
    if ((random.randint(0, 600) % 67) == 0):
        spritzer = Spritzer()
        wein.add(spritzer)
        all_sprites.add(spritzer)
    if (random.randint(0, 600) % 17) == 0:
        knedl = Knedl()
        knedln.add(knedl)
        all_sprites.add(knedl)
    if (pygame.time.get_ticks() % 100 == 0):
        gammelgrammel.y_speed = gammelgrammel.y_speed + random.randint(-2, 2)
    if (pygame.time.get_ticks() % 3823 == 0):
        gammelgrammel.y_speed = gammelgrammel.x_speed + 1

    #update
    all_sprites.update()
    knedln.update()

    #check to see if enemy got player
    hits = pygame.sprite.spritecollide(
        player, enemies, False,
        pygame.sprite.collide_circle)  #bool sets if sprite should be deleted
    if hits:
        game_over = True
    # check to see if grammel hit player
    hits = pygame.sprite.spritecollide(
        gammelgrammel, knedln, True,
        pygame.sprite.collide_circle)  #bool sets if sprite should be deleted
    hits = pygame.sprite.spritecollide(
        gammelgrammel, wein, True,
        pygame.sprite.collide_circle)  #bool sets if sprite should be deleted
    hits = pygame.sprite.spritecollide(player, bullets, False,
                                       pygame.sprite.collide_circle)
    if hits:
        if not hitsbuffer:
            player.angry()
    if (pygame.time.get_ticks() >=
            player.calm_down_time) & (player.anger):  # has he clamed down?
        player.anger = False
    hitsbuffer = pygame.sprite.spritecollide(player, bullets, False,
                                             pygame.sprite.collide_circle)

    #running = False
    #check to see if we collected some tokens (ate knoedl)
    hits = pygame.sprite.spritecollide(
        player, knedln, True)  # bool sets if sprite should be deleted
    if hits:
        for that_knedl in hits:
            score += that_knedl.typ
    #hits = pygame.sprite.spritecollide(gammelgrammel, knedln, True)  # bool sets if sp

    # check to see if we collected some tokens (drank spritzer)
    hits = pygame.sprite.spritecollide(
        player, wein, True)  # bool sets if sprite should be deleted
    if hits:
        player.getdrunk()
        if player.spritzer_count == speibzahl:
            player.puke()
            player.speed = FPS / 7.5
            score = score - 20  # knedl speiben

    all_sprites.draw(screen)
    draw_text(screen, 'Knedl Score: ' + str(score), 18, WIDTH / 2 - 20, 10)
    draw_text(screen, 'Spritzer: ' + str(player.spritzer_count), 18,
              WIDTH / 2 + 90, 10)
    draw_text(screen, 'Speed: ' + str(player.speed), 18, WIDTH / 2 + 400, 10)
    progress = float(player.spritzer_count) / speibzahl
    pygame.draw.rect(screen, GREEN,
                     pygame.Rect(WIDTH / 2 + 135, 18, maxwidthbar * progress,
                                 10))
    pygame.draw.rect(screen, BLACK,
                     pygame.Rect(WIDTH / 2 + 135, 18, maxwidthbar, 10), 1)
    #after drawing flip display
    pygame.display.flip()  # shows new screen graphics

    if game_over:
        show_game_over_screen(language)
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
