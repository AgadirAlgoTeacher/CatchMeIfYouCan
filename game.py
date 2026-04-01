from pygame import *

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)

window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')

background = transform.scale(image.load('Background.png'), Size)

GuySize  = (100, 80 )
CopSize = (100, 80)
CarSize = (200, 150)

#loading images
Guy = transform.scale(image.load('Guy.png'), GuySize)
Cop = transform.scale( image.load('Cop.png') , CopSize )
car = transform.rotate(transform.scale(image.load('Car.png'), CarSize), 90)


# entities properties
GuyPosx = 10 
GuyPosy = SCREEN_HEIGHT // 2 
GuySpeed = 1

CopPosx = 100
CopPosy = 100
CopSpeed = 0.5

CarPosx = 350
CarPosy = 200
CarSpeed = 2

game = True



while game:
    #detect if game ended
    for e in event.get():
        if e.type == QUIT:
            game = False

    #detect keys
    keys = key.get_pressed()
    if keys[K_LEFT] and GuyPosx > 0:
        GuyPosx -= GuySpeed
    if keys[K_RIGHT] and GuyPosx < SCREEN_WIDTH - GuySize[0]:
        GuyPosx += GuySpeed
    if keys[K_UP] and GuyPosy > 0:
        GuyPosy -= GuySpeed
    if keys[K_DOWN] and GuyPosy < SCREEN_HEIGHT - GuySize[1]:
        GuyPosy += GuySpeed

    #moving the car up and down
    CarPosy += CarSpeed
    if CarPosy <= 0 or CarPosy >= SCREEN_HEIGHT - 10:
        CarSpeed *= -1


    window.blit(background, (0, 0))
    window.blit(Guy, (GuyPosx, GuyPosy))
    window.blit(Cop, (CopPosx, CopPosy))
    window.blit(car, (CarPosx, CarPosy))
    
    display.update()

