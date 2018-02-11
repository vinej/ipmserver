from rest.helper import Helper, api_database
from rest.auth_token import AuthToken


class Api:

    def __init__(self, app):
        self.app = app
        self.auth_token = AuthToken(app)

    async def get(self, request, document):
        db = self.app.mongo[api_database]
        #isok = await self.auth_token.check_token(request.headers['Authorization'])
        #if not isok:
        #    return Helper.response_401(request)

        output = []
        docs = await db[document].find().to_list(length=100)
        for d in docs:
            d.pop('_id')
            output.append(d)
        # for
        return Helper.make_response({'result': output}, 200)

    async def post(self, request, document):
        db = self.app.mongo[api_database]
        record = request.json
        if request.json is None:
            return

        if not self.auth_token.check_token(request.headers['auth_token']):
            return Helper.response_401(request)

        record['isNew'] = False
        record['isSync'] = True
        mongo_id = await db[document].insert(record)
        output = await db[document].find_one({'_id': mongo_id})
        output.pop("_id")
        return Helper.make_response({'result': output}, 200)

    async def put(self, request, document):
        db = self.app.mongo[api_database]
        record = request.json
        if not self.auth_token.check_token(request.headers['auth_token']):
            return Helper.response_401(request)

        record['isNew'] = False
        record['isSync'] = True
        record_old = await db[document].find_one({'id': record["id"]})
        output = await db[document].replace_one(record_old, record)
        return Helper.make_response({'result': output}, 200)

    async def find(self, request, args):
        return await self.get(request, args)

    async def insert(self, request, args):
        return await self.post(request, args)

    async def update(self, request, args):
        return await self.put(request, args)
