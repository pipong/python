#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import datetime

class Player():
    def __init__(self, name):
        self.name = name

    def to_json(self):
        results = {}
        results['name'] = self.name
        return results


class PongGame():
    def __init__(self):
        self.number = -1
        self.players = []
        self.score = [0,0]
        self.serving_player_index = 0
        self.game_started = False
        self.serve_number = 0
        self.history = {}
        self.game_over = False
        self.winning_team = None
        self.doubles = False

    def team1_scored(self):
        self.score[0] +=1
        self.history[datetime.datetime.now()] = 'team 1 scored'
        self._check_score()
        if not self.game_over:
            self._next_serve()
        self.display_score()

    def team2_scored(self):
        self.score[1] +=1
        self.history[datetime.datetime.now()] = 'team 2 scored'
        self._check_score()
        if not self.game_over:
            self._next_serve()
        self.display_score()

    def reset_score(self):
        self.score = [0,0]
        # history?

    def who_is_serving(self):
        return self.players[self.serving_player_index].name

    def display_score(self):
        print 'Team 1:{0}\tTeam 2:{1}'.format(self.score[0], self.score[1])
        if not self.game_over:
            print '{0} serve #{1}'.format(self.who_is_serving(), self.serve_number)
        else:
            print 'game over'

    def start(self):
        if len(self.players) not in [2,4]:
            print 'invalid number of players'
            self.game_over = True
            return False
        if len(self.players) == 4:
            self.doubles = True
        else:
            self.doubles = False
        self.game_started = True
        self.serving_player_index = 0
        self.winning_team = None
        self.serve_number = 1
        #print 'game started'
        if self.doubles:
            msg = 'Team 1: {0}/{1} vs Team 2: {2}/{3}'.format(self.players[0].name,
                                              self.players[2].name,
                                              self.players[1].name,
                                              self.players[3].name)
        else:
            msg = 'Team 1: {0} vs Team 2: {1}'.format(self.players[0].name,
                                              self.players[1].name)
        self.history[datetime.datetime.now()] = 'game started'
        self.history[datetime.datetime.now()] = msg

        return True
        

    def _next_serve(self):
        if self.serve_number == 2:
            self.serve_number = 1
            self.serving_player_index +=1
            if self.serving_player_index == len(self.players):
                self.serving_player_index = 0
        else:
            if (self.score[0] > 9)  and (self.score[1] > 9):
                self.serve_number = 1
                self.serving_player_index +=1
                if self.serving_player_index == len(self.players):
                    self.serving_player_index = 0
            else:
                self.serve_number +=1

    def _check_score(self):
        if (self.score[0] > 10) or (self.score[1] > 10):
            if abs(self.score[0] - self.score[1]) > 1:
                self.game_over = True
                if self.score[0] > self.score[1]:
                    self.winning_team = 1
                else:
                    self.winning_team = 2
                self.history[datetime.datetime.now()] = 'team {0} wins'.format(self.winning_team)

    def to_json(self):
        results = {}
        results['game_number'] = self.number
        results['players'] =  []
        for idx in range(0, len(self.players)):
            results['players'].append(self.players[idx].to_json())
        results['score'] = self.score
        results['serving_player_index'] = self.serving_player_index
        results['game_started'] = self.game_started
        results['serve_number'] = self.serve_number
        results['history'] = {}
        for h in self.history:
            results['history'][str(h)] = self.history[h]
        results['game_over'] = self.game_over
        results['winning_team'] = self.winning_team
        results['doubles'] = self.doubles

        return results


class PongClient():
    def __init__(self):
        pass

    def quit(self):
        pass