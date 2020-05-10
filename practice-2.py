import pygame
import os
import math
import random
from pathlib import Path

#   tutorial used: https://nerdparadise.com/programming/pygame/part2

#   FIX UP THE LOGIC!!!
#   First, only calculate everything's position
#   Second, check collisions
#   Lastly, place everything on-screen


_image_library = {}
#   prevents images from being initialized more than once
def get_image(path):
        global _image_library
        path = 'image/' + path
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

#   prevents sounds from being initialized more than once
_sound_library = {}
def play_sound(path):
    global _sound_library
    path = 'sound/' + path
    sound = _sound_library.get(path)
    if sound == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(canonicalized_path)
            _sound_library[path] = sound
    sound.play()

# sets current working directory to where the code is being run from
os.chdir(Path(__file__).resolve().parent)

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Game title (Remember to CHANGE AT SOME POINT)
pygame.display.set_caption('Epic Game')

screenWidth = 768
screenHeight = 432

screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False

musicFile = "sound/night-of-fire.mp3"

pygame.mixer.music.load(musicFile)
pygame.mixer.music.play()

clock = pygame.time.Clock()

class Bullet:
    def __init__(self, x, y, type, angle=0, fromEnemy=False):
        #   type: bullet variant
        #       0 = default
        #   count: how long bullet remains on screen (in frames)
        #   speed: speed of bullet (in pixels [maybe fix at some point])
        #   graphic: image of bullet
        #   soundImpact: sound of bullet when hits target
        #   graphicImpact: graphic that appears when bullet hits target
        #   x: starting point from player (x)
        #   y: starting point from player (y)
        #
        #   --BULLET RELATED INFO IN OTHER CLASSES--
        #   Gun.sound: sound of bullet when fired
        #
        self.type = type
        if self.type == 0:
            self.x = x + 50
            self.y = y + 20
            self.count = 100
            self.speed = 8
            self.graphic = "bullet.png"
            self.sound = "gun-luger.wav"
            self.soundImpact = "bullet-impact-1.wav"
            self.sizeX = 10
            self.sizeY = 10
            self.damage = 50

        elif self.type == 1:
            self.x = x + 50
            self.y = y
            self.count = 30
            self.speed = 5
            self.graphic = "ball.png"
            self.soundImpact = "bullet-impact-1.wav"
            self.sizeX = 50
            self.sizeY = 50
            self.damage = 100
        
        #shotgun
        elif self.type == 2:
            self.x = x + 30
            self.y = y + 20
            self.count = 50
            self.speed = 8
            self.graphic = "bullet.png"
            self.soundImpact = "bullet-impact-1.wav"
            self.sizeX = 10
            self.sizeY = 10
            self.damage = 25

            #values needed for angled bullets
            self.angle = angle
            self.startY = self.y
            self.startX = self.x
            self.progX = 0
            self.progY = 0

        #laser
        elif self.type == 3:
            self.x = x + 50
            self.y = y + 10
            self.count = 25
            self.speed = 0
            self.graphic = "epic-laser.png"
            self.soundImpact = "bullet-impact-1.wav"
            self.sizeX = 300
            self.sizeY = 30
            self.damage = 3

            #values needed for laser bullets
            self.endX = self.x + self.sizeX
            self.endY = self.y + self.sizeY
        else:
            self.x = x + 50
            self.y = y + 25
            self.count = 30
            self.speed = 10
            self.graphic = "bullet.png"
            self.soundImpact = "bullet-impact-1.wav"
            self.sizeX = 10
            self.sizeY = 10
            self.damage = 50

        self.fromEnemy = fromEnemy
        self.hit = False

        if fromEnemy:
            self.speed = -self.speed
            self.x = x
            self.y = y + 20
        
        # center of bullet
        self.centerX = self.x + (self.sizeX/2)
        self.centerY = self.y + (self.sizeX/2)
    
    # bullet travels 1 frame and brings down the bullet's lifespan
    def move(self):
        #for angled shots (angle of 0 = horizontal)
        if self.type == 2:
            self.progX = self.progX + self.speed
            self.progY = ((self.angle * self.progX))
            self.y = self.progY + self.startY

            self.x = self.progX + self.startX
        if self.type == 3:
            self.x = player.x + 50
            self.y = player.y + 10

            self.endX = self.x + self.sizeX
            self.endY = self.y + self.sizeY
        else:
            # moves bullet depending on speed value
            self.x = self.x + self.speed
        # finds bullet's current center values
        self.centerX = self.x + (self.sizeX/2)
        self.centerY = self.y + (self.sizeX/2)

        # checks if bullet is within play area
        if self.centerX > screenWidth or self.centerX < 0:
            if self.type != 3:
                self.count = 0
            else:
                # doesn't allow laser to do damage off-screen
                # but laser stays even if player takes it off screen
                self.endX = screenWidth
                self.count -= 1
        else:
            self.count -= 1

class Gun:
    def __init__(self, type):
        #   type = gun type
        #       0 = default
        #       1 = TEST
        #   sound = sound of gun when fired
        #   fireRate = how quickly gun can be fired (by frame/sec)
        #   cooldown = cooldown between shots (set to fireRate whenever gun is shot)
        self.type = type
        if self.type == 0:
            self.bulletType = 0
            self.fireRate = 10
            self.sound = "gun-luger.wav"
        elif self.type == 1:
            self.bulletType = 1
            self.fireRate = 30
            self.sound = "deagle-50.wav"
        elif self.type == 2:
            self.bulletType = 2
            self.fireRate = 20
            self.sound = "gun-luger.wav"
        elif self.type == 3:
            self.bulletType = 3
            self.fireRate = 50
            self.sound = "epic-laser.wav"
        else:
            self.bulletType = 0
            self.fireRate = 10
            

    def canShoot(self):
        if player.mainGunCD == 0:
            return True
        else:
            return False

    def move(self, pressed, playX, playY):
        # player gun cooldown reduced by 1 frame if it can't be fired
        if player.mainGunCD > 0:
            player.mainGunCD -= 1
        
        # gun fired if spacebar is held
        if pressed[pygame.K_SPACE]:
            # checks if gun can be shot
            if self.canShoot():
                player.mainGunCD = self.fireRate
                play_sound(player.mainGun.sound)
                
                if player.mainGun.type == 2:
                    bullets.bullets.append(Bullet(playX, playY, self.bulletType, 0.6))
                    bullets.bullets.append(Bullet(playX, playY, self.bulletType, 0.3))
                    bullets.bullets.append(Bullet(playX, playY, self.bulletType, 0))
                    bullets.bullets.append(Bullet(playX, playY, self.bulletType, -0.3))
                    bullets.bullets.append(Bullet(playX, playY, self.bulletType, -0.6))
                # fires the bullet; adds bullet to bullets on screen
                bullets.bullets.append(Bullet(playX, playY, self.bulletType))
            

# individual enemy data
class Enemy:
    def __init__(self, type, x, y):
        self.type = type
        self.graphic = "ball.png"
        self.width = 50
        self.height = 50
        self.x = x + 600
        self.y = y
        self.explodeType = 0
        self.deathSound = "explode-impact-1.wav"
        self.healthMax = 200

        self.centerX = self.x + (self.width/2)
        self.centerY = self.y + (self.height/2)
        self.endX = self.x + self.width
        self.endY = self.y + self.height

        self.startX = self.x
        self.startY = self.y
        self.isAlive = True
        self.hit = False
        self.health = self.healthMax

        self.cooldown = 50
        self.speed = 4
        self.progress = 0
        self.maxProgress = self.speed * 30

    def move(self):
        self.progress += self.speed
        self.y = self.startY + self.progress

        self.centerX = self.x + (self.width/2)
        self.centerY = self.y + (self.height/2)
        self.endX = self.x + self.width
        self.endY = self.y + self.height

        self.cooldown -= 1
        if self.cooldown == 0:
            bullets.bullets.append(Bullet(self.x, self.y, 2, -.6, True))
            bullets.bullets.append(Bullet(self.x, self.y, 2, -.3, True))
            bullets.bullets.append(Bullet(self.x, self.y, 2, 0, True))
            bullets.bullets.append(Bullet(self.x, self.y, 2, .3, True))
            bullets.bullets.append(Bullet(self.x, self.y, 2, .6, True))
            self.cooldown = 50

        if self.progress >= self.maxProgress or self.progress <= 0:
            self.speed = -self.speed
            

'''
    def move(self):
        self.x += 1
        self.y += 1
'''

'''
    def animate(self):
        self.speedControl += 1
        if self.frameSpeed == self.speedControl:
            self.speedControl = 0
            if self.curFrame + 1 >= len(self.animateX) or self.curFrame >= len(self.animateY):
                self.animateInterval *= -1
            if self.curFrame <= 0:
                self.animateInterval *= -1

            self.x = self.startX + self.animateX[self.curFrame]
            self.y = self.startY + self.animateY[self.curFrame]

            self.centerX = self.x + (self.width/2)
            self.centerY = self.y + (self.height/2)
            self.endX = self.x + self.width
            self.endY = self.y + self.height

            print("X: " + str(self.x))
            print("Y: " + str(self.y))
            print("curFrame: " + str(self.curFrame))

            self.curFrame += self.animateInterval
'''

class Item:
    def __init__(self, x, y, itemType, typeVariant):
        def gunItem():
            self.itemType = 'gun'
            def machineGun():
                self.gunType = 0
                self.graphic = "item-machine-gun.png"
            def shotgun():
                self.gunType = 2
                self.graphic = "item-shotgun.png"
            def laser():
                self.gunType = 3
                self.graphic = "item-laser.png"

            tVariant = {
            0 : machineGun,
            2 : shotgun,
            3 : laser
            }
            tVariant[typeVariant]()
        def upgradeItem():
            print("YEET")

        self.speed = 3

        self.sizeX = 32
        self.sizeY = 32

        self.x = x - self.sizeX/2
        self.y = y - self.sizeY/2

        self.centerX = self.x + (self.sizeX/2)
        self.centerY = self.y + (self.sizeY/2)

        self.pickedUp = False
        self.inBounds = True

        iType = {
            'gun' : gunItem,
            'upg' : upgradeItem
        }
        iType[itemType]()

    def move(self):
        if self.x < 0:
            self.inBounds = False
        else:
            self.x = self.x - self.speed
            self.centerX = self.x + (self.sizeX/2)
            self.centerY = self.y + (self.sizeY/2)


# individual impact data, including impact/explosionn types and animation progress
class Impact:
    # x: enemy's center x
    # y: enemy's center y
    # type: impact type (determines graphics; should depend on enemy type)
    def __init__(self, x, y, type):
        self.type = type
        self.x = x
        self.y = y
        # default type
        if self.type == 0:
            # each file name for impact/explosion graphics are set up the same
            # file name = basename-# + frame# + file_type
            self.graphicBase = "explosion-1-"
            self.graphicEnd = ".png"

            # how many frames are in the animation, as well as the size
            self.frames = 9
            self.sizeX = 64
            self.sizeY = 64
            
            # when enemy dies and explosion displayed, this sound is played
            # !!!FIX THIS, NOT WORKING!!!
            
        # calculates x and y of explosion graphic
        self.x = self.x - (self.sizeX/2)
        self.y = self.y - (self.sizeY/2)

        # starting frame
        self.frameCur = 0

        self.isActive = True

        # graphic's first animation frame name
        self.graphic = self.graphicBase + "0" + self.graphicEnd
    
    # animates the explosion for each frame
    def animateFrame(self):
        if self.frames > self.frameCur:
            self.graphic = self.graphicBase + str(self.frameCur) + self.graphicEnd
            self.frameCur += 1

        # if no more animation frames left, impact is flagged for removal
        else:
            self.isActive = False

# player data
class Player():
    def __init__(self):
        # starting position
        self.x = 200
        self.y = 200
        
        # player's graphic
        self.graphic = "ball.png"

        # gets size of player (X, Y)
        self.size = get_image(self.graphic).get_size()
        self.sizeX = self.size[0]
        self.sizeY = self.size[1]

        # player's default starting gun
        self.mainGun = Gun(0)

        # value for checking if player's gun can be fired
        self.mainGunCD = 0

        self.centerX = self.x + self.sizeX/2
        self.centerY = self.y + self.sizeY/2

        self.endX = self.x + self.sizeX
        self.endY = self.y + self.sizeY
    
    # player movement and action checks for each frame
    def move(self, pressed):
        # player movement
        if pressed[pygame.K_UP]: self.y -= 3
        if pressed[pygame.K_DOWN]: self.y += 3
        if pressed[pygame.K_LEFT]: self.x -= 3
        if pressed[pygame.K_RIGHT]: self.x += 3

        # keeps player contained in the play area
        if self.x < 0:
            self.x = 0
        if self.x > screenWidth - self.sizeX:
            self.x = screenWidth - self.sizeX
        if self.y < 0:
            self.y = 0
        if self.y > screenHeight - self.sizeY:
            self.y = screenHeight - self.sizeY

        self.centerX = self.x + self.sizeX/2
        self.centerY = self.y + self.sizeY/2

        self.endX = self.x + self.sizeX
        self.endY = self.y + self.sizeY

        # main gun actions
        self.mainGun.move(pressed, self.x, self.y)

class Graphics():
    def __init__(self):
        self.blah = 0
        self.bgGraphic = "background-test.png"
        self.bgW, self.bgH = get_image(self.bgGraphic).get_size()
        self.bg_rect = get_image(self.bgGraphic).get_rect()

        self.bgX = 0
        self.bgY = 0

    def blit(self):
        # looping background
        for num in range(2):
            self.bgX -= .5
            if self.bgX <= -self.bgW:
                self.bgX = 0
            screen.blit(get_image(self.bgGraphic), (self.bgX, self.bgY))
            screen.blit(get_image(self.bgGraphic), (self.bgX + self.bgW, self.bgY))

        screen.blit(get_image(player.graphic), (player.x, player.y))

        num = 0
        while num in range (len(enemies.enemies)):
            screen.blit(get_image(enemies.enemies[num].graphic), (enemies.enemies[num].x, enemies.enemies[num].y))
            num += 1

        for b in bullets.bullets:
            screen.blit(get_image(b.graphic), (b.x, b.y))

        for i in impacts.impacts:
            screen.blit(get_image(i.graphic), (i.x, i.y))

        for i in items:
            screen.blit(get_image(i.graphic), (i.x, i.y))

        for b in bars.bars:
            pygame.draw.rect(screen, (0, 0, 0), (b[3] - 1, b[4] - 1, b[8] + 2, b[6] + 2), 0)
            pygame.draw.rect(screen, (255, 255, 255), (b[3] - 1, b[4] - 1, b[8] + 2, b[6] + 2), 1)
            pygame.draw.rect(screen, (b[0], b[1], b[2]), (b[3], b[4], b[5], b[6]), b[7])

# stores all bullet data, checked each frame
class Bullets():
    def __init__(self):
        self.bullets = []

    def move(self):
        num = 0
        # cycles through each bullet
        while num in range(len(self.bullets)):
            # if bullet's screen time has ended, it isn't displayed and is removed from the data
            if self.bullets[num].count == 0:
                del self.bullets[num]
                num -= 1
            # bullet movements are calculated
            else:
                self.bullets[num].move()
            num += 1

# stores all enemy data including each frame's movements for putting on screen
class Enemies():
    def __init__(self):
        self.enemies = []

    def move(self):
        if self.enemies:
            num = 0

            while num in range(len(self.enemies)):
                # performs enemy movements
                self.enemies[num].move()
                num += 1

# stores impact data to put on screen,checked each frame
class Impacts():
    def __init__(self):
        self.impacts = []

    def move(self):
        num = 0

        # animates each explosion/impact each frame
        while num in range(len(self.impacts)):
            self.impacts[num].animateFrame()
            # if no more frames to animate, explosion is over and it is erased
            if self.impacts[num].isActive == False:
                del self.impacts[num]
                num -= 1
            num += 1

# bullets/enemy collision checker; checks for every frame
class collisionChecker():

    def check(self):
        checkResult = []
        # checks each bullet for any possible collisions
        for bullet in bullets.bullets:
            # cycles through all enemies for each bullet
            if bullet.type == 3:
                for enemy in enemies.enemies:
                    if enemy.isAlive:
                        if bullet.x < enemy.centerX:
                            if bullet.endX > enemy.centerX:
                                if bullet.y < enemy.centerY:
                                    if bullet.endY > enemy.centerY:
                                        enemy.health -= bullet.damage
                                        if enemy.health <= 0:
                                            enemy.isAlive = False
                                            impacts.impacts.append(Impact(enemy.centerX, enemy.centerY, 0))
            else:
                for enemy in enemies.enemies:
                    # ensures one collision per bullet and that it only collides with enemies still alive
                    if not bullet.hit and enemy.isAlive and not bullet.fromEnemy:
                        # checks if bullet is within enemy's X values
                        if bullet.centerX > enemy.startX:
                            if bullet.centerX < enemy.endX:
                                # checks if bullet is within enemy's Y values
                                if bullet.centerY > enemy.startY:
                                    if bullet.centerY < enemy.endY:
                                        # bullet made contact with enemy!
                                        bullet.hit = True
                                        # bullet deals damage based on damage value
                                        enemy.health -= bullet.damage
                                        # if health 0, enemy marked as dead and explosion occurs
                                        if enemy.health <= 0:
                                            enemy.isAlive = False
                                            impacts.impacts.append(Impact(enemy.centerX, enemy.centerY, 0))
                    elif not bullet.hit and bullet.fromEnemy:
                        if bullet.centerX > player.x:
                            if bullet.centerX < player.x + player.sizeX:
                                if bullet.centerY > player.y:
                                    if bullet.centerY < player.y + player.sizeY:
                                        bullet.hit = True
                                        impacts.impacts.append(Impact(player.x + player.sizeX/2, player.y + player.sizeY/2, 0))

                              

        num = 0
        while num < len(bullets.bullets):
            if bullets.bullets[num].hit == True:
                play_sound(bullets.bullets[num].soundImpact)
                del bullets.bullets[num]
                num -= 1
            num += 1
        
        num = 0
        while num < len(enemies.enemies):
            if enemies.enemies[num].isAlive == False:
                play_sound(enemies.enemies[num].deathSound)
                checkResult.append({
                    'type' : 'death',
                    'centerX' : enemy.centerX,
                    'centerY' : enemy.centerY
                })
                del enemies.enemies[num]
                num -= 1
            num += 1

        return checkResult

    def itemCheck(self, items):
        try:
            for i in items:
                if i.centerX < player.endX:
                    if i.centerX > player.x:
                        if i.centerY > player.y:
                            if i.centerY < player.endY:
                                if i.itemType == 'gun':
                                    player.mainGun = Gun(i.gunType)
                                i.pickedUp = True

            # gets rid of items that have been picked up or have gotten out of bounds
            i = 0
            while i in range(len(items)):
                if not items[i].inBounds or items[i].pickedUp:
                    del items[i]
                    i -= 1
                i += 1
                    
                                
        except Exception as e:
            print(e)
        return items

# stores data for health bar graphics for each enemy
class Bars():
    def __init__(self):
        # default health bar values
        self.bars = []
        # width of inside bar
        self.barMaxWidth = 30
        # height of inside bar
        self.barHeight = 5
        # px above enemy
        self.pxAboveEnemy = 10
    
    # gets data for each enemy's health bar each frame
    def get(self):
        # resets the health bars as they can move around or change value every frame
        # (there might be a better way of doing this efficiently)
        self.bars = []

        for e in enemies.enemies:
            # checks if health is not full (don't want health bars drawn if health full)
            if not e.healthMax == e.health:
                # X value for bar
                self.barX = math.floor(e.centerX - self.barMaxWidth/2)
                # Y value for bar
                self.barY = e.y - self.pxAboveEnemy

                # calculates width of inside bar by % of health left (results in px)
                self.barWidth = math.floor(self.barMaxWidth * (e.health / e.healthMax))

                # inside bar color (green)
                self.barColor = [124, 252, 0]

                # adds bar data for each bar that should be displayed on screen to use with pygame.rect
                # [r, g, b, x, y, width, height, border/thickness, max-width]
                # (can probably be done nicer with tuples? probably don't even need?)
                self.bars.append([self.barColor[0], self.barColor[1], self.barColor[2], self.barX, self.barY, self.barWidth, self.barHeight, 0, self.barMaxWidth])


def moveEnemies(enemies):
    if len(enemies) > 0:
        num = 0

        while num in range(len(enemies)):
            # performs enemy movements
            enemies[num].move()
            num += 1

player = Player()
graphics = Graphics()
bullets = Bullets()
enemies = Enemies()
impacts = Impacts()
bars = Bars()

items = []

collisionChecker = collisionChecker()


while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # switch guns with Z
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if player.mainGun.type < 3:
                    player.mainGun = Gun(player.mainGun.type + 1)
                else:
                    player.mainGun = Gun(0)

            # spawns item drops with Q
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                items.append(Item(player.x + 600, player.y, 'gun', 2))

            # spawns enemy with C
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    enemies.enemies.append(Enemy(0, player.x, player.y))
                

        # clears the screen (turns it all WHITE)
        screen.fill((160, 160, 160))

        pressed = pygame.key.get_pressed()

        player.move(pressed)
        enemies.move()
        bullets.move()
        try:
            for i in items:
                i.move()
            items = collisionChecker.itemCheck(items)
        except Exception as e:
            print(e)

        # checks for bullets that have collided with enemies or the player and distributes damage caused
        # result contains info used for item drop calculations
        result = collisionChecker.check()

        try:
            for r in result:
                # if enemy died, possibility of item drop
                if r['type'] == 'death':
                    dropDeterminer = random.randint(0, 50)
                    if dropDeterminer < 5:
                        gunType = random.choice([0, 2, 3])
                        items.append(Item(r['centerX'], r['centerY'], 'gun', gunType))

            result = []

        except Exception as e:
            print(e)

        impacts.move()

        # calculates health bar information for all enemies that are alive
        bars.get()

        #creates all the graphics
        graphics.blit()

        # updates game screen
        pygame.display.flip()
        
        # will block execution until 1/60 seconds have passed
        # since the previous time clock.tick was called.
        clock.tick(60)