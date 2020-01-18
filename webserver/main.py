import tornado.ioloop
import tornado.web

elasticPort = 'https://be0044d4d6e64e0c9bb083c9a6d120ed.westeurope.azure.elastic-cloud.com:9243'
password = 'z7isN2WaZzTiGPUY6oUgYoDk'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        self.write("Received POST request")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    print("Webserver started")
    app = make_app()
    app.listen(8888) 
    tornado.ioloop.IOLoop.current().start()