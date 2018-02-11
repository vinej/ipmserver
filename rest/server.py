
from sanic import Sanic
from sanic_mongo import Mongo
import os

from rest.auth_token import AuthToken
from rest.api import Api
from rest.auth import Auth
from rest.black_list_token import BlacklistToken
from rest.user import User


app = Sanic(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database="restdb",
    port=27017,
    host='localhost'
)

Mongo.SetConfig(app, restdb=mongo_uri)
Mongo(app)

# ok, need that to avoid to put all import here to get the app object
AuthToken.set_app(app)
BlacklistToken.set_app(app)
User.set_app(app)
Auth.set_app(app)
Api.set_app(app)

app.add_route(Api.find, '/api/<args>', methods=['GET'])
app.add_route(Api.insert, '/api/<args>', methods=['POST'])
app.add_route(Api.update, '/api/<args>', methods=['PUT'])

app.add_route(Auth.login, '/auth/login', methods=['POST'])
app.add_route(Auth.user, '/auth/user', methods=['GET'])
app.add_route(Auth.logout, '/auth/logout', methods=['POST'])
app.add_route(Auth.register, '/auth/register', methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
