
import datetime
from bson.objectid import ObjectId
from rest.helper import api_database
import bcrypt

class User:

    mongo = None

    @staticmethod
    def set_app(app):
        User.mongo = app.mongo

    @staticmethod
    async def get_user(email):
        db = User.mongo[api_database]
        mongo_user = await db.users.find_one({'email': {'$eq': email}})
        if mongo_user:
            user = User(str(mongo_user['_id']), mongo_user['email'], mongo_user['password'])
            return user
        else:
            return None

    @staticmethod
    async def get_user_by_id(m_id):
        db = User.mongo[api_database]
        mongo_user = await db.find_one({'_id': {'$eq': ObjectId(m_id)}})
        if mongo_user:
            user = User(str(mongo_user['_id']), mongo_user['email'], mongo_user['password'], mongo_user['admin'])
            return user
        else:
            return None

    @staticmethod
    async def post_user(email, password, admin):
        db = User.mongo[api_database]
        try:
            d = dict(email=email,
                     password=password,
                     admin=admin,
                     register_on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            mongo_id = await db.users.insert(d)
            mongo_user = await db.users.find_one({'_id': mongo_id})
            if mongo_user:
                user = User(str(mongo_user['_id']), mongo_user['email'], mongo_user['password'], mongo_user['admin'])
                return user
            else:
                return None
        except Exception as inst:
            print(inst)
            raise

    @staticmethod
    async def put_user(json):
        db = User.mongo[api_database]
        old_user = await db.users.find_one({'id': json["_id"]})
        db.users.replace_one(old_user, json)

    def __init__(self, m_id, email, password, admin=False):
        """
        :type admin: Bool
        """
        self.id = m_id
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.registered_on = datetime.datetime.now()
        self.admin = admin
