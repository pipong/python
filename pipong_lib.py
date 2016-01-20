#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import datetime
import os
import ConfigParser
import cPickle
import json


class Player():
    def __init__(self, name):
        self.name = name
        self.games_started = 0
        self.games_finished = 0
        self.win = 0
        self.loss = 0
        self.id = None
        self.date_added = None

    def for_json(self):
        results = self.__dict__.copy()
        for item in results:
            if type(results[item]) is datetime.datetime:
                results[item] = results[item].isoformat()
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

    def team2_scored(self):
        self.score[1] +=1
        self.history[datetime.datetime.now()] = 'team 2 scored'
        self._check_score()
        if not self.game_over:
            self._next_serve()

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
        for i in range(0, len(self.players)):
            self.players[i].games_started +=1

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
                for i in range(0, len(self.players)):
                    self.players[i].games_finished +=1
                    if (i % 2 + 1) == self.winning_team:
                        self.players[i].win +=1
                    else:
                        self.players[i].loss +=1
                
                self.history[datetime.datetime.now()] = 'team {0} wins'.format(self.winning_team)

    def for_json(self):
        results = {}
        results['game_number'] = self.number
        results['players'] =  []
        for idx in range(0, len(self.players)):
            results['players'].append(self.players[idx].for_json())
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


class PongManager():
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        self.server_path = os.path.dirname(__file__)
        self.config_filename = '{0}\\server.ini'.format(self.server_path)
        self.player_filename = '{0}\\players.p'.format(self.server_path)
        config.read(self.config_filename)
        self.last_game_number = config.getint('server', 'game_number')
        self.last_player_number = 0
        if os.path.isfile(self.player_filename):
            self.player_directory = cPickle.load(open(self.player_filename, 'rb'))
            for name in self.player_directory:
                if self.player_directory[name].id > self.last_game_number:
                    self.last_player_number = self.player_directory[name].id
        else:
            self.player_directory = {}
        
        self.current_game = PongGame()

    def next_game_number(self):
        return self.last_game_number + 1

    def new_player(self, name):
        if name not in self.player_directory:
            new_player = Player(name)
            new_player.id = self.last_player_number + 1
            new_player.date_added = datetime.datetime.now()
            new_player.games_started = 0
            new_player.games_finished = 0

            self.last_player_number +=1
            self.player_directory[name] = new_player
            self.save_players()
        else:
            new_player = self.player_directory[name]
        return new_player

    def save_players(self):
        cPickle.dump(self.player_directory, open(self.player_filename, 'wb'))
        return

    def player_directory_for_json(self):
        results = {}
        for name in self.player_directory:
            results[name] = self.player_directory[name].for_json()
        return results

    def save_game(self):
        # save game file
        game_filename = '{0}\\{1}.p'.format(self.server_path, self.current_game.number)
        with open(game_filename, 'wb') as gamefile:
            cPickle.dump(self.current_game, gamefile)
        # update game number
        self.last_game_number = self.current_game.number
        config = ConfigParser.SafeConfigParser()
        config.read(self.config_filename)
        config.set('server', 'game_number', str(self.current_game.number))
        with open(self.config_filename, 'wb') as configfile:
            config.write(configfile)

    def get_game(self, game_number):
        game_filename = '{0}\\{1}.p'.format(self.server_path, game_number)
        with open(game_filename, 'wb') as gamefile:
            game = cPickle.load(gamefile)
        return game