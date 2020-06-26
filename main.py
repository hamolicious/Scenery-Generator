import pygame
from time import time
from random import choice, randint
from scenery import Scenery

#region initialise
pygame.init()
size = (640, 640)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

frame_start_time = 0
delta_time = 0
#endregion

trees = 10
bushes = 500

scene = Scenery(
    screen,
    trees=trees,
    bushes=bushes
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    screen.fill(0)
    frame_start_time = time()
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        scene = Scenery(
            screen,
            trees=trees,
            bushes=bushes
        )

    scene.draw()

    pygame.display.update()
    clock.tick(fps)
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
    delta_time = time() - frame_start_time




