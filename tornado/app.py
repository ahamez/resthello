#! /usr/bin/env python3

import motor
import pymongo
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.gen

from tornado.options import define, options

define("port", default=8080, help="run on the given port", type=int)
define("debug", default=False, help="debug mode", type=bool)


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


class Root(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello world')


def main():

    tornado.options.parse_command_line()

    if options.debug:
        print("Debug mode")

    motor_db = motor.MotorClient().paquito
    pymongo_db = pymongo.MongoClient().paquito

    application = tornado.web.Application([(r"/", Root),
                                           (r"/pymongo", PyMongo),
                                           (r"/motor", Motor),
                                           (r"/motor2", Motor2)
                                          ], motor_db=motor_db, pymongo_db=pymongo_db, debug=options.debug
    )

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
