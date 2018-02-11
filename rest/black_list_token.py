
import datetime
from rest.helper import api_database


class BlacklistToken:

    def __init__(self, app):
        self.app = app

    async def check_blacklist(self, auth_token):
        db = self.app.mongo[api_database]
        # check whether auth token has been blacklisted
        blacklist = await db.blacklists.find_one({'token': {'$eq': str(auth_token)}})
        if blacklist:
            return True
        else:
            return False

    async def post_blacklist(self, auth_token):
        # check whether auth token has been blacklisted
        db = self.app.mongo[api_database]
        try:
            d = dict(token=str(auth_token), blacklisted__on=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            await db.blacklists.insert(d)
        except Exception as inst:
            print(inst)
            raise
