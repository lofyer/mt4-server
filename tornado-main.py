from tornado import ioloop
from tornado import web

class MainHandler(web.RequestHandler):
    def get(self):
        self.write('''<html>
                <h1>Hello world!</h1></br>
                <h3>Hello world!</h3>
                </html>''')

class MyFormHandler(web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
            '<input type="text" name="message">'
            '<input type="submit" value="Submit">'
            '</form></body></html>')
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message"))

def prepare(self):
    if self.request.headers["Content-Type"].startswith("application/json"):
        self.json_args = json.loads(self.request.body)
    else:
        self.json_args = None

def make_app():
    return web.Application([
        web.url(r"/", MainHandler),
        web.url(r"/myform", MyFormHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
