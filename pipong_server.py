#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import web
import json
import pipong_lib
import traceback

VERSION = 1

WEBSERVER = None
CURRENT_GAME = None
urls = ('/', 'index',
        '/currentgame(/?)', 'currentgame',
        '/startgame(/?)', 'startgame',
        '/register_score/(.+)', 'register_score',
        '/addplayers/(.+)', 'addplayers',
        '/newgame(/?)', 'newgame',
        )


def start_up():
    global WEBSERVER
    global CURRENT_GAME
    WEBSERVER = web.application(urls, globals())
    WEBSERVER.run()

def finish_up():
    WEBSERVER.stop()


class index:
    def GET(self):
        return 'PiPong Server'

class newgame:
    def GET(self, url_string):
        try:
            global WEBSERVER
            global CURRENT_GAME
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            CURRENT_GAME = pipong_lib.PongGame()
            return json.dumps(True)

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class addplayers():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if url_string.endswith('/'):
                url_string = url_string[:-1]
            if len(CURRENT_GAME.players) < 4:
                CURRENT_GAME.players.append(pipong_lib.Player(url_string))
                return json.dumps(True)
            else:
                return json.dumps(False)

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class startgame():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            return json.dumps(CURRENT_GAME.start())

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

class currentgame():
    def GET(self, url_string):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Cache-control', 'no-cache')
        return json.dumps(CURRENT_GAME.to_json())

class register_score():
    def GET(self, url_string):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-control', 'no-cache')
            if url_string.endswith('/'):
                url_string = url_string[:-1]
            if not CURRENT_GAME.game_over:
                if url_string == '1':
                    CURRENT_GAME.team1_scored()
                    return json.dumps(True)
                elif url_string =='2':
                    CURRENT_GAME.team2_scored()
                    return json.dumps(True)
            return json.dumps(False)

        except Exception as err:
            # HTTP 500
            print traceback.format_exc()
            return web.webapi.internalerror(json.dumps({'return_code' : -1, 'messages' : traceback.format_exc()}))

if __name__ == "__main__":
    start_up()
 