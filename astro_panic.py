#*******************************************
#
# Programowanie
# Astro panic 
# Roman Furman 
#
#*******************************************
import pygame
from pygame.locals import *
import os.path
import random
import csv
import sys
#-----------------------------------------------------------------------
# Parametry programu
#-----------------------------------------------------------------------

SCREEN_WIDTH = 805
SCREEN_HEIGHT = 604
WHITE_SCREEN_WIDTH = 725.5
WHITE_SCREEN_HEIGHT = 545
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

#------------------
# define colors
#------------------
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKGREY = (93,94,94)

#-----------------------------------------------------------------------
# Funkcje pomocnicze
#-----------------------------------------------------------------------
def loadImage(name, useColorKey=False):
    """The function loads the image from the file and converts its pixels
     on the screen pixel format.
        Arguments:
            name: image
            useColorKey: If it is True, the pixel color (0,0) the image will be treated as transparent
    """
    fullname = os.path.join("File_Astro_panic",name)
    image = pygame.image.load(fullname)
    image = image.convert() 
    if useColorKey is True:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL) 
    return image

def loadSound(name):
    """The function loads sound from the file.
    """
    fullname = os.path.join("File_Astro_panic",name)
    sound = pygame.mixer.Sound(fullname)
    return sound

def draw_text(surface, text, size, x, y, color):
    """Function draw text on a window.
        Arguments:
            surface: screen
            text: text that you want to write
            size: size of the text
            x: width
            y: height
            color: color of the text
    """
    font = pygame.font.Font(pygame.font.match_font('Anti-aliased'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------
#------------------
# Game menu
#------------------
def menu():
    """Funtion create strat menu and quit menu at the end of the game.
    """
    global game

    background = pygame.image.load("File_Astro_panic/start_menu.jpg").convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    if game:
        draw_text(screen, "PRESS [ENTER] TO BEGIN", 35, SCREEN_WIDTH-210, SCREEN_HEIGHT-100, DARKGREY)
    draw_text(screen, "PRESS [ESC] TO QUIT", 35, SCREEN_WIDTH-SCREEN_WIDTH+170, SCREEN_HEIGHT - 100, DARKGREY)
   
    if game:
        draw_text(screen, "Astro panic", 100, SCREEN_WIDTH/2, 90, DARKGREY)
    if not game:
        draw_text(screen, "Game over!", 100, SCREEN_WIDTH/2, 90, DARKGREY)

    with open('high_score.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            number = row[0]

    draw_text(screen, "High score: {0!s}".format(int(number)), 35, SCREEN_WIDTH/2, SCREEN_HEIGHT-180, WHITE)
    if not game:
        draw_text(screen, "Your score: {0!s}".format(score), 30, SCREEN_WIDTH/2, SCREEN_HEIGHT-150, WHITE)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game:
                break
            elif event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            running = False
            pygame.quit() 
            sys.exit()  

#------------------
# Lives Draw
#------------------
def draw_lives(surf, x, y, lives, img):
    """Function draw pictures as lifes in game window.
        Arguments:
            surf: screen
            x: width
            y: height
            lives: how much lives player have
            img: mini image 
    """
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

#-----------------------------------------------------------------------------
# Klasy obiektów
#-----------------------------------------------------------------------------
#------------------
# Class Player
#------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize the Sprite base class
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("player.jpg",True)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2,0.92*SCREEN_HEIGHT) 
        self.x_velocity = 0
        self.y_velocity = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 500:
            self.hidden = False
            self.rect.center = (SCREEN_WIDTH/2, 0.92*SCREEN_HEIGHT)
        self.rect.move_ip((self.x_velocity,self.y_velocity))

        if self.rect.left < (SCREEN_WIDTH-WHITE_SCREEN_WIDTH)/2-5:
            self.rect.left = (SCREEN_WIDTH-WHITE_SCREEN_WIDTH)/2-5
        elif self.rect.right > SCREEN_WIDTH-28:
            self.rect.right = SCREEN_WIDTH-28

    def hide(self):
        # hide the player temporarily 
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200)

#-------------------------
# Class PlayerLaser
#-------------------------
class PlayerLaser(pygame.sprite.Sprite):

    def __init__(self,startpos):
        # Initialize the Sprite base class
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("shot.jpg",True)
        self.rect = self.image.get_rect()
        self.rect.center = startpos

    def update(self):
        if self.rect.bottom <= 60:
            self.kill()
        else:
            self.rect.move_ip((0,-30))

#--------------------
# Class EnemyFighter
#--------------------
class UFO(pygame.sprite.Sprite):
    def __init__(self,img,startx,starty,x,y):
        # Initialize the Sprite base class
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage(img, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.x_velocity = random.randint(x,y)
        self.y_velocity = random.randint(x,y)

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))
        
        if self.rect.left < (SCREEN_WIDTH-WHITE_SCREEN_WIDTH)/2-5 or self.rect.right > SCREEN_WIDTH-28:
            self.x_velocity = -(self.x_velocity)

        if self.rect.top < (SCREEN_HEIGHT-WHITE_SCREEN_HEIGHT)/2-10 or self.rect.bottom > SCREEN_WIDTH-230:
            self.y_velocity = -(self.y_velocity)

#-------------------------------
# Class ScoreBoard
#------------------------------
class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize the Sprite base class
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.text = "Score: %4d" % self.score
        self.font = pygame.font.SysFont(None,40)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()

    def update(self,n):
        self.score += n
        self.text = "Score: %4d" % self.score
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()

#-----------------------------------------------------------------------
# Właściwy program
#-----------------------------------------------------------------------

# PyGame initialization
pygame.init()

# Generate window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Astro Panic")

# Background image
background_image = loadImage("background.jpg")

# Audio file
PlayerShotFX = loadSound("shot.wav")
explodeFX = loadSound("explode.wav")


# Initialize player ship
PlayerSprite = pygame.sprite.RenderClear()       # container for the player's ship
player = Player()                                # create a ship
PlayerSprite.add(player)                         # add him to the group
PlayerLaserSprites = pygame.sprite.RenderClear() # container for lasers

# Mini ship for life board
Player_mini = pygame.transform.scale(player.image, (25,19))
Player_mini.set_colorkey(BLACK)

# Initialize enemy UFOs
UFOSprites = pygame.sprite.RenderClear()
UFOSprites2 = pygame.sprite.RenderClear()
UFOSprites3 = pygame.sprite.RenderClear()
UFOSprites4 = pygame.sprite.RenderClear()
UFOSprites.add(UFO("UFO.jpg",150,300,-3,3))
UFOSprites.add(UFO("UFO.jpg",450,200,-5,5))
UFOSprites.add(UFO("UFO.jpg",650,120,-4,4))

# Initialize hit counter
scoreboardSprite = pygame.sprite.RenderClear()
scoreboardSprite.add(ScoreBoard())
scoreboardSprite.draw(screen)
pygame.display.flip()

clock = pygame.time.Clock()
running = True
game = True
show_menu = True
score = 0
UFO_counter = 0
UFO_counter2 = 0
UFO_counter3 = 0
UFO_counter4 = 0

while running:
    if show_menu:
        menu()
        pygame.time.delay(1500)
        show_menu = False
        screen.blit(background_image,(0,0))
    if game:
        screen.blit(background_image,(0,0))
        clock.tick(50) #not more than 50 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_LEFT:
                    player.x_velocity = -10
                elif event.key == K_RIGHT:
                    player.x_velocity = 10
                elif event.key == K_SPACE:
                    PlayerLaserSprites.add(PlayerLaser(player.rect.midtop))
                    PlayerShotFX.play()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    player.x_velocity = 0 
                elif event.key == K_RIGHT:
                    player.x_velocity = 0

        # Dodaj statek wroga
        UFO_counter += 1
        if 100 <= UFO_counter:
            UFOSprites.add(UFO("UFO.jpg",200,200,-8,8))
            UFOSprites.add(UFO("UFO.jpg",400,300,-7,7))
            UFOSprites.add(UFO("UFO.jpg",700,220,-6,6))
            UFO_counter = 0

        UFO_counter2 += 1
        if 200 <= UFO_counter2:
            UFOSprites2.add(UFO("UFO.jpg",270,350,-10,10))
            UFOSprites2.add(UFO("UFO.jpg",500,400,-6,6))
            UFO_counter2 = 180

        UFO_counter3 +=1
        if 800 <= UFO_counter3:
            UFOSprites3.add(UFO("UFO.jpg",600,360,-8,8))
            UFO_counter3 = 790

        UFO_counter4 +=1
        if 2000 <= UFO_counter4:
            UFOSprites4.add(UFO("UFO.jpg",300,150,-10,10))
            UFOSprites4.add(UFO("UFO.jpg",450,150,-10,10))
            UFOSprites4.add(UFO("UFO.jpg",500,150,-10,10))
            UFO_counter4 = 1995

        
        # Update all sprites
        PlayerSprite.update()
        PlayerLaserSprites.update()
        UFOSprites.update()
        UFOSprites2.update()
        UFOSprites3.update()
        UFOSprites4.update()

        # Check if enemy UFOSs have been hit
        for hit in pygame.sprite.groupcollide(UFOSprites, PlayerLaserSprites,1,1):
            explodeFX.play()
            score += 1
            scoreboardSprite.update(1)
            pygame.display.flip()

        for hit in pygame.sprite.groupcollide(UFOSprites2, PlayerLaserSprites,1,1):
            explodeFX.play()
            score += 2
            scoreboardSprite.update(2)
            pygame.display.flip()
        
        for hit in pygame.sprite.groupcollide(UFOSprites3, PlayerLaserSprites,1,1):
            explodeFX.play()
            score += 5
            scoreboardSprite.update(5)
            pygame.display.flip()
        
        for hit in pygame.sprite.groupcollide(UFOSprites4, PlayerLaserSprites,1,1):
            explodeFX.play()
            score += 10
            scoreboardSprite.update(10)
            pygame.display.flip()

        # Check if player's ship has been hit
        for hit in pygame.sprite.groupcollide(PlayerSprite, UFOSprites,0,1):
            player.hide()
            player.lives -= 1
            explodeFX.play() 
        
        for hit in pygame.sprite.groupcollide(PlayerSprite, UFOSprites2,0,1):
            player.hide()
            player.lives -= 1
            explodeFX.play() 
        
        for hit in pygame.sprite.groupcollide(PlayerSprite, UFOSprites3,0,1):
            player.hide()
            player.lives -= 1
            explodeFX.play() 

        for hit in pygame.sprite.groupcollide(PlayerSprite, UFOSprites4,0,1):
            player.hide()
            player.lives -= 1
            explodeFX.play() 

        # If player's ship is destroyed
        if player.lives == 0:
            with open('high_score.csv', newline='') as inputfile:
                for row in csv.reader(inputfile):
                    high_score = int(row[0])
            if score > int(high_score):
                with open("high_score.csv", "w", newline='') as f:
                    thewriter = csv.writer(f)
                    thewriter.writerow(['{0!s}'.format(score)])
            print("Koniec gry")
            game = False
            show_menu = True

        # Clear the screen
        PlayerLaserSprites.clear(screen, background_image)
        PlayerSprite.clear(screen, background_image)
        UFOSprites.clear(screen, background_image)
        UFOSprites2.clear(screen, background_image)
        UFOSprites3.clear(screen, background_image)
        UFOSprites4.clear(screen, background_image)
        scoreboardSprite.clear(screen, background_image)
        

        # Draw sprites on the screen
        scoreboardSprite.draw(screen)
        PlayerLaserSprites.draw(screen)
        PlayerSprite.draw(screen)
        UFOSprites.draw(screen)
        UFOSprites2.draw(screen)
        UFOSprites3.draw(screen)
        UFOSprites4.draw(screen)
        draw_lives(screen, SCREEN_WIDTH-100, 5, player.lives, Player_mini)

        # *after* drawing everything, flip the display
        pygame.display.flip()
