
import datetime
from rest.helper import Helper, api_database


class BlacklistToken:

    mongo = None

    @staticmethod
    def set_app(app):
        BlacklistToken.mongo = app.mongo

    def __init__(self, m_id, token, blacklisted_on):
        self.id = m_id
        self.token = token
        self.blacklisted_on = blacklisted_on

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    async def check_blacklist(auth_token):
        db = BlacklistToken.mongo[api_database]
        # check whether auth token has been blacklisted
        blacklist = await db.blacklists.find_one({'token': {'$eq': str(auth_token)}})
        if blacklist:
            return True
        else:
            return False

    @staticmethod
    async def post_blacklist(auth_token):
        # check whether auth token has been blacklisted
        db = BlacklistToken.mongo[api_database]
        try:
            d = dict(token=str(auth_token), blacklisted__on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            mongo_id = await db.blacklists.insert(d)
            mongo_bl = await db.blacklists.find_one({'_id': mongo_id})
            if mongo_bl:
                blacklist = BlacklistToken(str(mongo_bl['_id']), mongo_bl['token'], mongo_bl['blacklisted__on'])
                return blacklist
            else:
                return None
        except Exception as inst:
            print(inst)
            raise
