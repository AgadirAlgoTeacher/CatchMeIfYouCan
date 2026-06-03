from pygame import *
from random import randint
from math import cos, sin, radians
import json, sys, os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable))

init()

SCREEN_WIDTH  = int(display.Info().current_w // 1.05)
SCREEN_HEIGHT = int(display.Info().current_h // 1.05)
ScreenSize    = (SCREEN_WIDTH, SCREEN_HEIGHT)

window = display.set_mode(ScreenSize)
display.set_caption('Catch Me If You Can')

background = transform.scale(image.load('imgs/background.png'), ScreenSize)

GuySize       = (SCREEN_WIDTH // 25, SCREEN_HEIGHT // 17)
CopSize       = (SCREEN_WIDTH // 20, SCREEN_HEIGHT // 16)
CarSize       = (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)
IconSize      = (SCREEN_WIDTH // 13, SCREEN_HEIGHT // 10)
CashSize      = (SCREEN_WIDTH // 35, SCREEN_HEIGHT // 25)
LightningSize = (SCREEN_WIDTH // 5,  SCREEN_HEIGHT // 15)

#loading images
GuyRunningFrames = [
    transform.scale(image.load('imgs/Guy1.png').convert_alpha(), GuySize),
    transform.scale(image.load('imgs/Guy2.png').convert_alpha(), GuySize),
    transform.scale(image.load('imgs/Guy3.png').convert_alpha(), GuySize)
]
Guy         = transform.scale(image.load('imgs/GuyIdle.png').convert_alpha(), GuySize)
Cop         = transform.scale(image.load('imgs/CopIdle.png').convert_alpha(), CopSize)
Car         = transform.rotate(transform.scale(image.load('imgs/Car.png').convert_alpha(), CarSize), 90)
Car2        = transform.flip(Car, False, True)
Car3        = transform.rotate(Car, -90)
Cash        = transform.scale(image.load('imgs/Cash.png').convert_alpha(), CashSize)
Lightning   = transform.scale(image.load('imgs/Lightning.png').convert_alpha(), LightningSize)
HealthImg   = transform.scale(image.load('imgs/Health.png').convert_alpha(), IconSize)
TazerImg    = transform.scale(image.load('imgs/Tazer.png').convert_alpha(), IconSize)
MoneyImg    = transform.scale(image.load('imgs/Money.png').convert_alpha(), IconSize)
TopScoreImg = transform.scale(image.load('imgs/TopScore.png').convert_alpha(), IconSize)
LevelsImg   = image.load('imgs/Levels.png').convert_alpha()
LevelsRowH  = LevelsImg.get_height() // 6
LevelsRowW  = LevelsImg.get_width()
WantedW     = SCREEN_WIDTH // 6
WantedH     = int(WantedW * LevelsRowH / LevelsRowW)

TopScore   = json.load(open('data.json'))['Top Score']
WantedFont = font.SysFont('impact', 48)
TitleFont  = font.SysFont('impact', 80)
BtnFont    = font.SysFont('impact', 42)
font       = font.SysFont(None, 40)

# level durations (ms) and thresholds
LEVEL_DURATIONS  = [10000, 25000, 30000, 30000, 30000, 30000]
LEVEL_THRESHOLDS = [sum(LEVEL_DURATIONS[:i]) for i in range(6)]
ANIM_SPEED       = 120
GuySpeed         = 1
CopSpeed         = 0.5


def reset_game():
    global tazer, Health, Money, SpawnedCash, cash_for_recharge
    global GuyPosx, GuyPosy, angle, anim_frame, anim_timer
    global CopPosx, CopPosy, Cop_angle, Cop2Posx, Cop2Posy, Cop2_angle
    global Cop3Posx, Cop3Posy, Cop3_angle, Cop4Posx, Cop4Posy, Cop4_angle
    global CarPosx, CarPosy, CarSpeed, Car2Posx, Car2Posy, Car2Speed
    global Car3Posx, Car3Posy, Car3Speed
    global lightning_active, lightning_timer, lightning_hit
    global cop_stunned, cop_stun_end_time, wanted_level, start_time

    tazer             = 5
    Health            = 100
    Money             = 0
    cash_for_recharge = 0
    GuyPosx           = 10
    GuyPosy           = SCREEN_HEIGHT // 2
    angle             = 0
    anim_frame        = 0
    anim_timer        = 0
    CopPosx,  CopPosy,  Cop_angle  = 100,                100,                0
    Cop2Posx, Cop2Posy, Cop2_angle = SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200, 0
    Cop3Posx, Cop3Posy, Cop3_angle = 100,                SCREEN_HEIGHT - 200, 0
    Cop4Posx, Cop4Posy, Cop4_angle = SCREEN_WIDTH - 200, 100,                 0
    CarPosx,  CarPosy,  CarSpeed   = 350,              200,               2
    Car2Posx, Car2Posy, Car2Speed  = SCREEN_WIDTH-350, SCREEN_HEIGHT-200, -2
    Car3Posx, Car3Posy, Car3Speed  = 0,                SCREEN_HEIGHT//2,  2
    lightning_active               = False
    lightning_timer                = 0
    lightning_hit                  = False
    cop_stunned                    = False
    cop_stun_end_time              = 0
    wanted_level                   = 0
    start_time                     = time.get_ticks()
    SpawnedCash = [(randint(0, SCREEN_WIDTH-50), randint(0, SCREEN_HEIGHT-50)) for _ in range(5)]


reset_game()
game_state = 'start'
mouse.set_visible(True)
game = True


while game:
    mx, my = mouse.get_pos()

    for e in event.get():
        if e.type == QUIT:
            game = False
        if game_state == 'playing':
            if e.type == KEYDOWN and e.key == K_SPACE and tazer > 0:
                tazer -= 1
                lightning_active = True
                lightning_timer  = time.get_ticks()
                lightning_hit    = False
        if game_state in ('start', 'gameover'):
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                btn_w, btn_h = 240, 65
                btn_x = SCREEN_WIDTH  // 2 - btn_w // 2
                btn_y = SCREEN_HEIGHT // 2 + 60
                if Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mx, my):
                    reset_game()
                    game_state = 'playing'
                    mouse.set_visible(False)

    # ── START SCREEN ──────────────────────────────────────────────
    if game_state == 'start':
        window.blit(background, (0, 0))
        overlay = Surface(ScreenSize, SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        window.blit(overlay, (0, 0))

        title     = TitleFont.render('Catch Me If You Can', True, (255, 220, 0))
        t_outline = TitleFont.render('Catch Me If You Can', True, (0, 0, 0))
        tx = SCREEN_WIDTH  // 2 - title.get_width()  // 2
        ty = SCREEN_HEIGHT // 2 - 130
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            window.blit(t_outline, (tx + dx, ty + dy))
        window.blit(title, (tx, ty))

        sub = WantedFont.render('Collect cash. Dodge cops. Survive.', True, (200, 200, 200))
        window.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, ty + title.get_height() + 10))

        btn_w, btn_h = 240, 65
        btn_x = SCREEN_WIDTH  // 2 - btn_w // 2
        btn_y = SCREEN_HEIGHT // 2 + 60
        hovering  = Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mx, my)
        btn_color = (255, 210, 0) if hovering else (200, 150, 0)
        draw.rect(window, btn_color, (btn_x, btn_y, btn_w, btn_h), border_radius=14)
        draw.rect(window, (255, 255, 255), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=14)
        btn_text = BtnFont.render('PLAY', True, (0, 0, 0))
        window.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width()  // 2,
                               btn_y + btn_h // 2 - btn_text.get_height() // 2))

        display.update()
        continue

    # ── GAME OVER SCREEN ──────────────────────────────────────────
    if game_state == 'gameover':
        window.blit(background, (0, 0))
        overlay = Surface(ScreenSize, SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        window.blit(overlay, (0, 0))

        go_surf = TitleFont.render('GAME OVER', True, (220, 30, 30))
        go_out  = TitleFont.render('GAME OVER', True, (0, 0, 0))
        gx = SCREEN_WIDTH  // 2 - go_surf.get_width()  // 2
        gy = SCREEN_HEIGHT // 2 - 150
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            window.blit(go_out, (gx + dx, gy + dy))
        window.blit(go_surf, (gx, gy))

        score_surf = WantedFont.render(f'Cash Collected: {Money}', True, (255, 255, 255))
        window.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - 40))

        btn_w, btn_h = 280, 65
        btn_x = SCREEN_WIDTH  // 2 - btn_w // 2
        btn_y = SCREEN_HEIGHT // 2 + 60
        hovering  = Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mx, my)
        btn_color = (255, 210, 0) if hovering else (200, 150, 0)
        draw.rect(window, btn_color, (btn_x, btn_y, btn_w, btn_h), border_radius=14)
        draw.rect(window, (255, 255, 255), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=14)
        btn_text = BtnFont.render('PLAY AGAIN', True, (0, 0, 0))
        window.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width()  // 2,
                               btn_y + btn_h // 2 - btn_text.get_height() // 2))

        display.update()
        continue

    # ── GAMEPLAY ──────────────────────────────────────────────────
    window.blit(background, (0, 0))

    #detect keys
    keys = key.get_pressed()
    if keys[K_LEFT]  and GuyPosx > 0:                          GuyPosx -= GuySpeed; angle = -180
    if keys[K_RIGHT] and GuyPosx < SCREEN_WIDTH - GuySize[0]:  GuyPosx += GuySpeed; angle = 0
    if keys[K_UP]    and GuyPosy > 0:                          GuyPosy -= GuySpeed; angle = 90
    if keys[K_DOWN]  and GuyPosy < SCREEN_HEIGHT - GuySize[1]: GuyPosy += GuySpeed; angle = -90

    if keys[K_LEFT]  and keys[K_DOWN]: angle = -135
    if keys[K_LEFT]  and keys[K_UP]:   angle =  135
    if keys[K_RIGHT] and keys[K_DOWN]: angle = -45
    if keys[K_RIGHT] and keys[K_UP]:   angle =  45

    # update wanted level from elapsed time
    elapsed      = time.get_ticks() - start_time
    wanted_level = min(5, sum(1 for t in LEVEL_THRESHOLDS if elapsed >= t) - 1)

    #moving cars (level 2: car+car2, level 3+: car3 too)
    if wanted_level >= 2:
        CarPosy += CarSpeed
        if CarPosy <= 0 or CarPosy >= SCREEN_HEIGHT - 10: CarSpeed *= -1
        Car2Posy += Car2Speed
        if Car2Posy <= 0 or Car2Posy >= SCREEN_HEIGHT - 10: Car2Speed *= -1
    if wanted_level >= 3:
        Car3Posx += Car3Speed
        if Car3Posx <= 0 or Car3Posx >= SCREEN_WIDTH - 10: Car3Speed *= -1

    # cops follow guy (unless stunned)
    if cop_stunned:
        if time.get_ticks() > cop_stun_end_time:
            cop_stunned = False
    else:
        def move_cop(cx, cy):
            ca = 0
            if cx < GuyPosx: cx += CopSpeed; ca = 0
            if cx > GuyPosx: cx -= CopSpeed; ca = 180
            if cy < GuyPosy: cy += CopSpeed; ca = -90
            if cy > GuyPosy: cy -= CopSpeed; ca = 90
            if cx < GuyPosx and cy < GuyPosy: ca = -45
            if cx < GuyPosx and cy > GuyPosy: ca =  45
            if cx > GuyPosx and cy < GuyPosy: ca = -135
            if cx > GuyPosx and cy > GuyPosy: ca =  135
            return cx, cy, ca

        if wanted_level >= 1: CopPosx,  CopPosy,  Cop_angle  = move_cop(CopPosx,  CopPosy)
        if wanted_level >= 3: Cop2Posx, Cop2Posy, Cop2_angle = move_cop(Cop2Posx, Cop2Posy)
        if wanted_level >= 4: Cop3Posx, Cop3Posy, Cop3_angle = move_cop(Cop3Posx, Cop3Posy)
        if wanted_level >= 5: Cop4Posx, Cop4Posy, Cop4_angle = move_cop(Cop4Posx, Cop4Posy)

    #detecting collision
    Guy_rect  = Guy.get_rect(topleft=(GuyPosx,  GuyPosy))
    Cop_rect  = Cop.get_rect(topleft=(CopPosx,  CopPosy))
    Cop2_rect = Cop.get_rect(topleft=(Cop2Posx, Cop2Posy))
    Cop3_rect = Cop.get_rect(topleft=(Cop3Posx, Cop3Posy))
    Cop4_rect = Cop.get_rect(topleft=(Cop4Posx, Cop4Posy))
    Car_rect  = Car.get_rect(topleft=(CarPosx,  CarPosy))
    Car2_rect = Car2.get_rect(topleft=(Car2Posx, Car2Posy))
    Car3_rect = Car3.get_rect(topleft=(Car3Posx, Car3Posy))

    cop_hit = ((wanted_level >= 1 and Guy_rect.colliderect(Cop_rect))  or
               (wanted_level >= 3 and Guy_rect.colliderect(Cop2_rect)) or
               (wanted_level >= 4 and Guy_rect.colliderect(Cop3_rect)) or
               (wanted_level >= 5 and Guy_rect.colliderect(Cop4_rect)))
    car_hit = ((wanted_level >= 2 and (Guy_rect.colliderect(Car_rect) or Guy_rect.colliderect(Car2_rect))) or
               (wanted_level >= 3 and Guy_rect.colliderect(Car3_rect)))

    if cop_hit or car_hit:
        window.blit(background, (randint(-5, 5), randint(-5, 5)))
        red = Surface(ScreenSize, SRCALPHA)
        red.fill((255, 0, 0, 80))
        window.blit(red, (0, 0))
    if cop_hit: Health -= 0.1
    if car_hit: Health -= 0.2

    if Health <= 0:
        game_state = 'gameover'
        mouse.set_visible(True)
        display.update()
        continue

    #drawing everything
    moving = keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]
    if moving:
        if time.get_ticks() - anim_timer > ANIM_SPEED:
            anim_frame = (anim_frame + 1) % len(GuyRunningFrames)
            anim_timer = time.get_ticks()
        GuySprite = GuyRunningFrames[anim_frame]
    else:
        anim_frame = 0
        GuySprite  = Guy
    window.blit(transform.rotate(GuySprite, angle), (GuyPosx, GuyPosy))
    if wanted_level >= 1: window.blit(transform.rotate(Cop, Cop_angle),   (CopPosx,  CopPosy))
    if wanted_level >= 3: window.blit(transform.rotate(Cop, Cop2_angle),  (Cop2Posx, Cop2Posy))
    if wanted_level >= 4: window.blit(transform.rotate(Cop, Cop3_angle),  (Cop3Posx, Cop3Posy))
    if wanted_level >= 5: window.blit(transform.rotate(Cop, Cop4_angle),  (Cop4Posx, Cop4Posy))
    if wanted_level >= 2: window.blit(Car,  (CarPosx,  CarPosy));  window.blit(Car2, (Car2Posx, Car2Posy))
    if wanted_level >= 3: window.blit(Car3, (Car3Posx, Car3Posy))

    # draw lightning in front of guy and check cop hit
    if lightning_active:
        rad = radians(angle)
        rotated_lightning = transform.rotate(Lightning, angle)
        rlw, rlh = rotated_lightning.get_size()
        dist = GuySize[0] + rlw // 2
        lx = int(GuyPosx + GuySize[0] // 2 + cos(rad) * dist - rlw // 2)
        ly = int(GuyPosy + GuySize[1] // 2 - sin(rad) * dist - rlh // 2)
        window.blit(rotated_lightning, (lx, ly))
        lightning_rect = rotated_lightning.get_rect(topleft=(lx, ly))
        if not lightning_hit:
            active_cop_rects = (
                ([Cop_rect]  if wanted_level >= 1 else []) +
                ([Cop2_rect] if wanted_level >= 3 else []) +
                ([Cop3_rect] if wanted_level >= 4 else []) +
                ([Cop4_rect] if wanted_level >= 5 else [])
            )
            for cr in active_cop_rects:
                if lightning_rect.colliderect(cr):
                    lightning_hit     = True
                    cop_stunned       = True
                    cop_stun_end_time = time.get_ticks() + 1000
                    break
        if time.get_ticks() - lightning_timer > LIGHTNING_DURATION:
            lightning_active = False

    #drawing icons hud
    window.blit(HealthImg,   (10,              SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(font.render(str(int(Health)), True, (255, 255, 255)), (IconSize[0] + 15,     SCREEN_HEIGHT - IconSize[1] //1.5))
    window.blit(TazerImg,    (IconSize[0] * 2, SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(font.render(str(tazer),       True, (255, 255, 255)), (IconSize[0] * 3 + 15, SCREEN_HEIGHT - IconSize[1] //1.5))
    window.blit(MoneyImg,    (IconSize[0] * 4, SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(font.render(str(Money),       True, (255, 255, 255)), (IconSize[0] * 5 + 15, SCREEN_HEIGHT - IconSize[1] //1.5))
    window.blit(TopScoreImg, (IconSize[0] * 6, SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(font.render(str(TopScore),    True, (255, 255, 255)), (IconSize[0] * 7 + 15, SCREEN_HEIGHT - IconSize[1] //1.5))

    # wanted level display (top center)
    row_surf     = LevelsImg.subsurface((0, wanted_level * LevelsRowH, LevelsRowW, LevelsRowH))
    lvl_scaled   = transform.scale(row_surf, (WantedW, WantedH))
    text_str     = f'Wanted Time: {elapsed // 1000}s'
    time_label   = WantedFont.render(text_str, True, (0, 0, 139))
    time_outline = WantedFont.render(text_str, True, (255, 255, 255))
    tx = SCREEN_WIDTH // 2 - time_label.get_width() // 2
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        window.blit(time_outline, (tx + dx, 5 + dy))
    window.blit(time_label, (tx, 5))
    # progress bar to next wanted level
    bar_x = SCREEN_WIDTH // 2 - WantedW // 2
    bar_y = 5 + time_label.get_height()
    bar_h = 8
    if wanted_level < 5:
        progress = (elapsed - LEVEL_THRESHOLDS[wanted_level]) / LEVEL_DURATIONS[wanted_level]
    else:
        progress = 1.0
    draw.rect(window, (50, 50, 50), (bar_x, bar_y, WantedW, bar_h))
    draw.rect(window, (0, 0, 139),  (bar_x, bar_y, int(WantedW * progress), bar_h))
    window.blit(lvl_scaled, (bar_x, bar_y + bar_h + 2))

    #detect collision with cash and respawn it
    for pos in SpawnedCash:
        window.blit(Cash, pos)
        if Guy_rect.colliderect(Cash.get_rect(topleft=pos)):
            Money += 1
            cash_for_recharge += 1
            if cash_for_recharge >= 10:
                tazer += 1
                cash_for_recharge = 0
            SpawnedCash.remove(pos)
            SpawnedCash.append((randint(0, SCREEN_WIDTH-50), randint(0, SCREEN_HEIGHT-50)))
            break

    display.update()
