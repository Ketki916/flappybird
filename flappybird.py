'''This program immitates the game Flappybird. The 'q' key begins the games and the spacebar moves the bird. The game
will end if a pillar is hit, or if the bird moves off the screen. The score is displayed at the end of the game.'''

import gamebox
import pygame
import random

Width = 800
Height = 600
camera = gamebox.Camera(Width, Height)
bird = gamebox.from_color(100, 300, 'blue', 20, 20)
startbox = gamebox.from_text(camera.x, camera.y, 'Press "q" to begin', 50, 'white')
originalpillars = [gamebox.from_color(400, 150, 'red', 50, 300), gamebox.from_color(400, 500, 'red', 50, 200),
           gamebox.from_color(800, 100, 'red', 50, 200), gamebox.from_color(800, 450, 'red', 50, 300),
           gamebox.from_color(1200, 200, 'red', 50, 400), gamebox.from_color(1200, 550, 'red', 50, 100),
           gamebox.from_color(1600, 50, 'red', 50, 100), gamebox.from_color(1600, 400, 'red', 50, 400)]

pillars = originalpillars.copy()

count = 0
score = 0
pillarlocation = 1600


game_start = False


def tick(keys):
    global game_start
    global pillarlocation
    global count
    global score
    global pillars

    camera.clear('black')
    if pygame.K_q in keys and (game_start != 1):
        pillars = originalpillars[:]
        for pillar in originalpillars:
            camera.draw(pillar)
        game_start = 1
        score = 0
        count = 0
        pillarlocation = 1600

    if game_start == 1:
        count += 1
        bird.move_speed()
        bird.speedy += 1
        camera.x += 3
        bird.x += 3

        if count % 100 == 0:
            pillarlocation += 300
            pillar_center = random.randint(0, 250)
            newpillar = [gamebox.from_color(pillarlocation, pillar_center, 'red', 50, pillar_center*2),
                         gamebox.from_color(pillarlocation, (600 + ((pillar_center*2) + 100))/2, 'red', 50, 600 -
                                            ((pillar_center*2) + 100))]
            pillars.extend(newpillar)

        if count % 30 == 0:
            score += 1

        if count % 100 == 0 and count > 300:
            pillars.pop(0)

        if pygame.K_UP in keys:
            bird.speedy = -7
            keys.clear()
        camera.draw(bird)

        for pillar in pillars:
            if bird.touches(pillar) or bird.y <= 0 or bird.y >= 600:
                bird.move_to_stop_overlapping(pillar)
                game_start = 2
                camera.x = 400
                bird.x = 100
                bird.y = 300
                bird.speedy = 0
                break
            camera.draw(pillar)

    elif game_start == 2:
        totalscore = gamebox.from_text(camera.x, camera.y - 50, "Your score is: " + str(score), 50, 'white')
        restartbox = gamebox.from_text(camera.x, camera.y + 50, 'Press "q" to restart', 50, 'white')
        camera.draw(totalscore)
        camera.draw(restartbox)
    else:
        camera.draw(startbox)
    camera.display()


ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)
