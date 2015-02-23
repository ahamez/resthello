#! /usr/bin/env python3

import concurrent.futures

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.gen
import motor

import mongoengine

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

class Foo(mongoengine.Document):
    field1 = mongoengine.StringField(required=True)
    field2 = mongoengine.StringField(max_length=50)


class Simple(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        query_res = yield tornado.gen.Task(Simple.do_query)
        self.write("Simple" + query_res)
        # self.write({'Foo':'simple'})
        self.finish()

    @staticmethod
    def do_query(callback):
        query = Foo.objects(field1="1")
        query.no_cache()
        res = "".join(foo.field1 for foo in query)
        return callback(res)


class Pool(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        query_res = yield self.settings['pool'].submit(Pool.do_query)
        self.write("Pool" + query_res)

    @staticmethod
    def do_query():
        query = Foo.objects(field1="1")
        query.no_cache()
        res = "".join(foo.field1 for foo in query)
        return res


class Motor(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['db']
        user = yield db.users.find_one({'_id': 'saucisson'})
        yield db.billings.update({'_id': 'saucisson'}, {'key': 'value'})
        projet = yield db.projects.find_one({'_id': 'cosyverif'})
        yield db.results.update({'_id': 'cosyverif'}, {'key': 'value'})
        locale = yield db.locales.find_one({'_id': 'en'})
        self.write('foo' + str(user) + str(projet) + str(locale))
        self.finish()

class Root(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello world')

def main():
    tornado.options.parse_command_line()

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    db = motor.MotorClient().paquito

    mongoengine.connect('localhost')

    application = tornado.web.Application([(r"/",Root),
                                           (r"/simple", Simple),
                                           (r"/pool", Pool),
                                           (r"/motor", Motor)
                                           ], db=db, pool=pool, debug=False
    )

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
