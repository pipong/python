#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import web
import json
import pipong_lib
import traceback
import datetime

VERSION = 1

WebServer = None
GameManager = pipong_lib.PongManager()

urls = ('/', 'index',
        '/currentgame(/?)', 'currentgame',
        '/startgame(/?)', 'startgame',
        '/playerdirectory(/?)', 'playerdirectory',
        '/register_score/(.+)', 'register_score',
        '/newplayer/(.+)', 'newplayer',
        '/retrievegame/(.+)', 'retrievegame',
        '/addplayers/(.+)', 'addplayers',
        '/newgame(/?)', 'newgame',
        )


def start_up():
    global WebServer
    global GameManager
    WebServer = web.application(urls, globals())
    WebServer.run()

def finish_up():
    WebServer.stop()

class GameResponse():
    def __init__(self, contents, return_code):
        self.timestamp = datetime.datetime.now()
        self.contents = contents
        self.return_code = return_code

    def prepare(self):
        results = self.__dict__.copy()
        for item in results:
            if type(results[item]) is datetime.datetime:
                results[item] = results[item].isoformat()
        return results


class index:
    def GET(self):
        return 'PiPong Server'

class newgame:
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            GameManager.current_game = pipong_lib.PongGame()
            GameManager.current_game.number = GameManager.next_game_number()
            return json.dumps(GameResponse(GameManager.current_game.prepare(), 0).prepare())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class addplayers():
    def GET(self, player_name):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if player_name.endswith('/'):
                player_name = player_name[:-1]
            if len(GameManager.current_game.players) < 4:
                if player_name not in GameManager.player_directory:
                    GameManager.new_player(player_name)
                GameManager.current_game.players.append(GameManager.player_directory[player_name])
                return json.dumps(GameResponse(GameManager.current_game.prepare(), 0).prepare())
            else:
                return json.dumps(GameResponse(GameManager.current_game.prepare(), 1).prepare())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class newplayer():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if url_string.endswith('/'):
                url_string = url_string[:-1]
            new_player = GameManager.new_player(url_string)
            return json.dumps(GameResponse(new_player.prepare(), 0).prepare())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class playerdirectory():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            return json.dumps(GameResponse(GameManager.player_directory_prepare(), 0).prepare())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class startgame():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if GameManager.current_game.start():
                return json.dumps(GameResponse(GameManager.current_game.prepare(), 0).prepare())
            else:
                return json.dumps(GameResponse('Failed', 1).prepare())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class currentgame():
    def GET(self, url_string):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Cache-control', 'no-cache')
        return json.dumps(GameResponse(GameManager.current_game.prepare(), 0).prepare())

class retrievegame():
    def GET(self, game_number):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if game_number.endswith('/'):
                game_number = game_number[:-1]
            

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class register_score():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if url_string.endswith('/'):
                url_string = url_string[:-1]
            if not GameManager.current_game.game_over:
                if url_string == '1':
                    GameManager.current_game.team1_scored()
                elif url_string =='2':
                    GameManager.current_game.team2_scored()
                if GameManager.current_game.game_over:
                    GameManager.save_players()
                    GameManager.save_game()
                return json.dumps(GameResponse(GameManager.current_game.prepare(), 0).prepare())
            return json.dumps(GameResponse(GameManager.current_game.prepare(), 1).prepare())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

if __name__ == "__main__":
    start_up()
 