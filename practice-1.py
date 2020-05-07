import pygame

# tutorial used: https://nerdparadise.com/programming/pygame/part1

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False

is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # changes color of rect if you hit space
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue

        # clears the screen (turns it all black)
        screen.fill((0, 0, 0))

        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        
        # check if direction keys pressed, and move the rectangle accordingly if they are
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3
        
        # draw rectangle
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
        
        # updates game screen
        pygame.display.flip()
        
        # will block execution until 1/60 seconds have passed
        # since the previous time clock.tick was called.
        clock.tick(60)