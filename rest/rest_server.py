
from sanic import Sanic
from sanic_mongo import Mongo
import os
from rest.api import Api
from rest.auth import Auth
from rest.admin import Admin


class Server:

    def __init__(self, myapp):
        self.myapp = myapp
        self.auth = Auth(myapp)
        self.api = Api(myapp)
        self.admin = Admin(app)
        self.myapp_settings = os.getenv(
            'APP_SETTINGS',
            'project.server.config.DevelopmentConfig'
        )

    def set(self):
        self.myapp.config.from_object(self.myapp_settings)

        mongo_uri = "mongodb://{host}:{port}/{database}".format(
            database="restdb",
            port=27017,
            host='localhost'
        )

        Mongo.SetConfig(self.myapp, restdb=mongo_uri)
        Mongo(self.myapp)

    def route(self):
        self.myapp.add_route(self.api.find, '/api/<args>', methods=['GET'])
        self.myapp.add_route(self.api.insert, '/api/<args>', methods=['POST'])
        self.myapp.add_route(self.api.update, '/api/<args>', methods=['PUT'])
        self.myapp.add_route(self.auth.register, '/auth/register', methods=['POST'])
        self.myapp.add_route(self.auth.logout, '/auth/logout', methods=['POST'])
        self.myapp.add_route(self.auth.login, '/auth/login', methods=['POST'])
        self.myapp.add_route(self.auth.user, '/auth/user', methods=['GET'])
        self.myapp.add_route(self.admin.command, '/admin/<cmd>', methods=['GET'])

    def set_get_app(self):
        self.set()
        self.route()
        return self.myapp


if __name__ == '__main__':
    app = Sanic(__name__)
    Server(app).set_get_app().run(host='0.0.0.0', port=8000)
