#! /usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.options
import sys

class RootHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello, world")

class FooHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Foo")

application = tornado.web.Application([
  (r"/", RootHandler),
  (r"/foo", FooHandler)
])

if __name__ == "__main__":

  # args = sys.argv
  # args.append("--log_file_prefix=/Users/hal/Desktop/my_app.log")
  # tornado.options.parse_command_line(args)

  application.listen(8080)
  tornado.ioloop.IOLoop.instance().start()
