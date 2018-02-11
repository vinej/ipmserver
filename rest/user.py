
import datetime
from bson.objectid import ObjectId
from rest.helper import api_database
import bcrypt


class UserModel:

    def __init__(self, m_id, email, password, admin=False):
        """
        :type admin: Bool
        """
        self.id = m_id
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.registered_on = datetime.datetime.now()
        self.admin = admin


class User:

    def __init__(self, app):
        self.app = app

    async def get_user(self, email):
        db = self.app.mongo[api_database]
        mongo_user = await db.users.find_one({'email': {'$eq': email}})
        if mongo_user:
            return UserModel(str(mongo_user['_id']), mongo_user['email'], mongo_user['password'])
        else:
            return None

    async def get_user_by_id(self, m_id):
        db = self.app.mongo[api_database]
        mongo_user = await db.find_one({'_id': {'$eq': ObjectId(m_id)}})
        if mongo_user:
            return UserModel(str(mongo_user['_id']), mongo_user['email'], mongo_user['password'], mongo_user['admin'])
        else:
            return None

    async def post_user(self, email, password, admin):
        db = self.app.mongo[api_database]
        try:
            d = dict(email=email,
                     password=password,
                     admin=admin,
                     register_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            mongo_id = await db.users.insert(d)
            mongo_user = await db.users.find_one({'_id': mongo_id})
            if mongo_user:
                return UserModel(str(mongo_user['_id']), mongo_user['email'],
                                 mongo_user['password'], mongo_user['admin'])
            else:
                return None
        except Exception as inst:
            print(inst)
            raise

    async def put_user(self, json):
        db = self.app.mongo[api_database]
        old_user = await db.users.find_one({'id': json["_id"]})
        db.users.replace_one(old_user, json)
