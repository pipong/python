#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import pipong_lib

VERSION = 1

def main():

    game = pipong_lib.PongGame()
    #game = pipong_lib.PongClient()
    
    game.players.append(pipong_lib.Player('Fred'))
    game.players.append(pipong_lib.Player('Matt'))
    game.players.append(pipong_lib.Player('Frank'))
    game.players.append(pipong_lib.Player('Mark'))

    if game.start():
        while not game.game_over:
            point_for = raw_input('which team scored?')

            if point_for == '1':
                game.team1_scored()
            else:
                game.team2_scored()

    for event_time in sorted(game.history):
        print '{0} - {1}'.format(event_time, game.history[event_time])

    return

if __name__ == "__main__":
    main()
 