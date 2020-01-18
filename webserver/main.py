import tornado.ioloop
import tornado.web
import tornado.httpclient as httpclient

elasticPort = 'https://be0044d4d6e64e0c9bb083c9a6d120ed.westeurope.azure.elastic-cloud.com:9243'
password = 'z7isN2WaZzTiGPUY6oUgYoDk'


class MainHandler(tornado.web.RequestHandler):

    async def query_elastic_clusters(self, query):
        http_client = httpclient.AsyncHTTPClient()
        # TODO: format request such that accepted by elastic cluster
        request = httpclient.HTTPRequest("http://www.google.com")
        #request = httpclient.HTTPRequest("http://www.google.com", method="POST",
        #                                 body=query)
        try:
            response = await http_client.fetch(request)
        except Exception as e:
            print("Error: %s" % e)
        else:
            print(response.body)
            self.write(response.body.decode('iso8859-1'))
            return response.body.decode('iso8859-1')

    def get(self):
        self.write("Hello, world")

    async def post(self):
        print("Received POST request\n")
        query = self.get_body_argument("data")
        print("query: ", query)
        #self.query_elastic_clusters(query)
        response = await self.query_elastic_clusters(query)
        self.write(response)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    print("Webserver started")
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()