#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import web
import json
import pipong_lib
import traceback

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
    global CURRENT_GAME
    WebServer = web.application(urls, globals())
    WebServer.run()

def finish_up():
    WebServer.stop()


class index:
    def GET(self):
        return 'PiPong Server'

class newgame:
    def GET(self, url_string):
        try:
            global WebServer
            global GameManager
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            GameManager.current_game = pipong_lib.PongGame()
            GameManager.current_game.number = GameManager.next_game_number()
            return json.dumps(True)

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
                return json.dumps(True)
            else:
                return json.dumps(False)

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
            return json.dumps(new_player.for_json())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class playerdirectory():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            return json.dumps(GameManager.player_directory_for_json())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class startgame():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            return json.dumps(GameManager.current_game.start())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class currentgame():
    def GET(self, url_string):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Cache-control', 'no-cache')
        return json.dumps(GameManager.current_game.for_json())

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
                return json.dumps(True)
            return json.dumps(False)

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

if __name__ == "__main__":
    start_up()
 