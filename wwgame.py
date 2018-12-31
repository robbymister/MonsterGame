import sys, pygame, random
from ww import *
pygame.init()

ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/face-cool-24.png", ww))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 0, 3, 1))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 7, 4, 5))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 4, 10, 3))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 5, 20, 2))
ww.add_actor(Wall("icons/wall.jpg", ww, 3, 4))
ww.add_actor(Wall("icons/wall.jpg", ww, 5, 10))
ww.add_actor(Wall("icons/wall.jpg", ww, 5, 11))
ww.add_actor(Wall("icons/wall.jpg", ww, 5, 12))
ww.add_actor(StickyBox("icons/slimebox.png", ww, 10, 1))
ww.add_actor(StickyBox("icons/slimebox.png", ww, 15, 11))

# This loop adds boxes to level, up to 99
num_boxes=0
while num_boxes<100:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y))
        num_boxes+=1

# Determines what event is going on and does the animations
while True:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            ww.player_event(event.key)
    ww.step()
    ww.draw()
