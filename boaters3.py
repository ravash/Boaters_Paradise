""" boaters.py
    Program Name: Boaters Paradise
    Author : Dylan Scott
    Date Created : July 6th 2012
    Version : 0.3
    
    In this version i've added the Ballon class to the friendly list and an objective for the player to collect. Ive added two island's to the enemy list to increase difficulty. Ive added the Submarine class to be the
    Big slow enemy of the game. Ive changed the way the sprites are written to the background so the islands are on top of everything else.
    """
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Boat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("boat.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndYay = pygame.mixer.Sound("yay.ogg")
            self.sndThunder = pygame.mixer.Sound("thunder.ogg")
            self.sndEngine = pygame.mixer.Sound("Boat-engine.ogg")
            self.sndEngine.play(-1)
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (60, mousey)
                
class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("island.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = -4
    
    def update(self):
        
        self.rect.centerx += self.dx
        if self.rect.left <= 0 :
            self.reset()
            
    def reset(self):
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_height())
        
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("balloon.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = -6
    
    def update(self):
        
        self.rect.centerx += self.dx
        if self.rect.left <= 0 :
            self.reset()
            
    def reset(self):
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_height())
      
class Shark(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shark.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.left <= 0 :
            self.reset()
    
    def reset(self):
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_height())
        self.dx = random.randrange(-8, -4)
        self.dy = random.randrange(-1, 1)
        
class Submarine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sub.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.left <= 0 :
            self.reset()
    
    def reset(self):
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_height())
        self.dx = random.randrange(-5, -4)
        self.dy = 0
    
class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ocean.gif")
        self.rect = self.image.get_rect()
        self.dx = -5
        self.reset()
        
    def update(self):
        self.rect.right += self.dx
        if self.rect.left <= -800:
            self.reset() 
    
    def reset(self):
        self.rect.left = 0

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Spare Engines: %d, score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
    
def game():
    pygame.display.set_caption("Boaters Paradise!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    boat = Boat()
    shark1 = Shark()
    shark2 = Shark()
    shark3 = Shark()
    sub1 = Submarine()
    island1 = Island()
    island2 = Island()
    balloon = Balloon()
    ocean = Ocean()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(ocean, boat, balloon)
    enemySprites = pygame.sprite.Group(island1, island2, shark1, shark2, shark3, sub1)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        
        #check collisions
        
        if boat.rect.colliderect(balloon.rect):
            boat.sndYay.play()
            balloon.reset()
            scoreboard.score += 100

        hitEnemy = pygame.sprite.spritecollide(boat, enemySprites, False)
        if hitEnemy:
            boat.sndThunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
            for theEnemy in hitEnemy:
                theEnemy.reset()
        
        friendSprites.update()
        enemySprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        enemySprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    
    boat.sndEngine.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("Boaters Paradise!")

    boat = Boat()
    ocean = Ocean()
    
    allSprites = pygame.sprite.Group(ocean, boat)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Boating Paradise.     Last score: %d" % score ,
    "Instructions:  You are out on your,",
    "families boat having a nice relaxing,",
    "cruise when your Favourite balloon,",
    "collection gets loose In very,",
    "dangerous waters!It is now your,",    
    " job to navigate these dangerous, ",
    " enemy infested waters to get as ",
    "many balloons back as possible.",
    "Steer with the mouse and",
    "good luck!",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    boat.sndEngine.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
