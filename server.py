#!/usr/bin/python
import web
import json
import threading
from readttys import Readttys
from write.write  import write as publish

urls = (
    '/', 'index',
    '/prs', 'prs',
    '/uts', 'uts',
    '/getdata', 'getdata'
)

class index:
    def GET(self):
        return "Web server is running"

class prs:
    def GET(self):
        # redirect to the static file ...
        raise web.seeother('/static/vyoma-prs.html')

class uts:
    def GET(self):
        # redirect to the static file ...
        raise web.seeother('/static/vyoma-uts.html')


class getdata:
    def GET(self):
        #data = "Content-Type: text/plain;charset=utf-8\n\n"
        data =  json.dumps(publish.getData())
        return data

t=threading.Thread(target=Readttys.main)

if __name__ == "__main__":
    try:
        app = web.application(urls, globals())
        t.setDaemon(True)
        #web.config.debug = False
        t.start()
        app.run()
    except Exception as e:
        print e