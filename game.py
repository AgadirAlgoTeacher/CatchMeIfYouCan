from pygame import *

init()

SCREEN_WIDTH = display.Info().current_w //1.05
SCREEN_HEIGHT = display.Info().current_h //1.05

Size = (SCREEN_WIDTH, SCREEN_HEIGHT)

window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')

background = transform.scale(image.load('imgs/background.png'), Size)

GuySize  = (SCREEN_WIDTH // 25, SCREEN_HEIGHT // 17)
CopSize = (SCREEN_WIDTH // 20, SCREEN_HEIGHT // 16)
CarSize = (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)
HUDSize = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 10)
#loading images
Guy = transform.scale(image.load('imgs/GuyIdle.png').convert_alpha(), GuySize)
mouse.set_visible(False)
gun = transform.scale(image.load('imgs/gun.png').convert_alpha(), (30, 30))
Cop = transform.scale( image.load('imgs/CopIdle.png').convert_alpha() , CopSize )
car = transform.rotate(transform.scale(image.load('imgs/Car.png').convert_alpha(), CarSize), 90)
HUD = transform.scale(image.load('imgs/HUD.png').convert_alpha(), HUDSize)  

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

angle = 0



while game:
    #detect if game ended
    for e in event.get():
        if e.type == QUIT:
            game = False

    #detect keys
    keys = key.get_pressed()
    if keys[K_LEFT] and GuyPosx > 0:
        GuyPosx -= GuySpeed
        angle = -180
    if keys[K_RIGHT] and GuyPosx < SCREEN_WIDTH - GuySize[0]:
        GuyPosx += GuySpeed
        angle = 0
    if keys[K_UP] and GuyPosy > 0:
        GuyPosy -= GuySpeed
        angle = 90
    if keys[K_DOWN] and GuyPosy < SCREEN_HEIGHT - GuySize[1]:
        GuyPosy += GuySpeed
        angle = -90

        
    if keys[K_LEFT] and keys[K_DOWN]:
        angle = -135
    if keys[K_LEFT] and keys[K_UP]:
        angle = 135
    if keys[K_RIGHT] and keys[K_DOWN]:
        angle = -45
    if keys[K_RIGHT] and keys[K_UP]:
        angle = 45

    #moving the car up and down
    CarPosy += CarSpeed
    if CarPosy <= 0 or CarPosy >= SCREEN_HEIGHT - 10:
        CarSpeed *= -1
    
    # cop follows guy
    if CopPosx < GuyPosx: CopPosx += CopSpeed; cop_angle = 0
    if CopPosx > GuyPosx: CopPosx -= CopSpeed; cop_angle = 180
    if CopPosy < GuyPosy: CopPosy += CopSpeed; cop_angle = -90
    if CopPosy > GuyPosy: CopPosy -= CopSpeed; cop_angle = 90
    # cop angle
    if CopPosx < GuyPosx and CopPosy < GuyPosy: cop_angle = -45
    if CopPosx < GuyPosx and CopPosy > GuyPosy: cop_angle = 45
    if CopPosx > GuyPosx and CopPosy < GuyPosy: cop_angle = -135
    if CopPosx > GuyPosx and CopPosy > GuyPosy: cop_angle = 135

    window.blit(background, (0, 0))
    window.blit(transform.rotate(Guy, angle), (GuyPosx, GuyPosy))
    window.blit(gun, mouse.get_pos())
    window.blit(transform.rotate(Cop, cop_angle), (CopPosx, CopPosy))
    window.blit(car, (CarPosx, CarPosy))
    window.blit(HUD, (0, SCREEN_HEIGHT - HUDSize[1]))
    display.update()

