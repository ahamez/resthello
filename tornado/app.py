#! /usr/bin/env python3

import random

import motor
import pymongo
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.gen
import tornado.httpclient
from tornado.options import define, options


define("port", default=8080, help="run on the given port", type=int)
define("debug", default=False, help="debug mode", type=bool)
define("mongo", default='127.0.0.1', help="MongoDB host", type=str)


class PyMongo(tornado.web.RequestHandler):
    # @tornado.gen.coroutine
    def get(self):
        db = self.settings['pymongo_db']
        user = db.users.find_one({'_id': 'saucisson'})
        db.billings.update({'_id': 'saucisson'}, {'key': 'value'})
        projet = db.projects.find_one({'_id': 'cosyverif'})
        db.results.update({'_id': 'cosyverif'}, {'key': 'value'})
        locale = db.locales.find_one({'_id': 'en'})
        self.write(str(user) + str(projet) + str(locale))
        self.finish()


class PyMongoOne(tornado.web.RequestHandler):
    # @tornado.gen.coroutine
    def get(self):
        db = self.settings['pymongo_db']
        user = db.users.find_one({'_id': 'saucisson'})
        self.write(str(user))
        self.finish()


class Motor(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['motor_db']
        user = yield db.users.find_one({'_id': 'saucisson'})
        yield db.billings.update({'_id': 'saucisson'}, {'key': 'value'})
        projet = yield db.projects.find_one({'_id': 'cosyverif'})
        yield db.results.update({'_id': 'cosyverif'}, {'key': 'value'})
        locale = yield db.locales.find_one({'_id': 'en'})
        self.write(str(user) + str(projet) + str(locale))
        self.finish()


class Motor2(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['motor_db']
        user_future = db.users.find_one({'_id': 'saucisson'})
        billings_update_future = db.billings.update({'_id': 'saucisson'}, {'key': 'value'})
        project_future = db.projects.find_one({'_id': 'cosyverif'})
        results_update_future = db.results.update({'_id': 'cosyverif'}, {'key': 'value'})
        locale_future = db.locales.find_one({'_id': 'en'})
        user, _, project, _, locale = yield [user_future, billings_update_future, project_future, results_update_future,
                                             locale_future]
        self.write(str(user) + str(project) + str(locale))
        self.finish()

class MotorOne(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['motor_db']
        user = yield db.users.find_one({'_id': 'saucisson'})
        self.write(str(user))
        self.finish()

class Random3(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        t = random.randint(10, 100) / 1000
        yield tornado.gen.sleep(t)
        self.write("Slept " + str(t * 1000) + " ms")
        self.finish()


class Random4(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        t1 = random.randint(10, 100) / 1000
        t2 = random.randint(10, 100) / 1000
        yield tornado.gen.sleep(t1)
        yield tornado.gen.sleep(t2)
        self.write("Slept " + str(t1 * 1000) + " ms, then " + str(t2 * 1000))
        self.finish()


class Random5(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        res = "Slept: "
        for i in range(random.randint(2, 4)):
            t = random.randint(10, 100) / 1000
            yield tornado.gen.sleep(t)
            res += str(t * 1000) + "ms, "
        self.write(res)
        self.finish()


class Web(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        page = yield http_client.fetch('http://httpbin.org/html')
        self.write(page.body)
        self.finish()


class Root(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello world')


def main():
    tornado.options.parse_command_line()
    random.seed()

    if options.debug:
        print("Debug mode")
    print("Port", options.port)

    motor_db = motor.MotorClient(options.mongo).paquito
    pymongo_db = pymongo.MongoClient(options.mongo).paquito

    application = tornado.web.Application([(r"/", Root),
                                           (r"/pymongo", PyMongo),
                                           (r"/pymongo_one", PyMongoOne),
                                           (r"/motor", Motor),
                                           (r"/motor2", Motor2),
                                           (r"/motor_one", MotorOne),
                                           (r"/rand3", Random3),
                                           (r"/rand4", Random4),
                                           (r"/rand5", Random5),
                                           (r"/web", Web)
                                           ], motor_db=motor_db, pymongo_db=pymongo_db, debug=options.debug
                                          )

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
