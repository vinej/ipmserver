from rest.helper import Helper, api_database
from rest.auth_token import AuthToken


class Api:

    # the variable is really initiated when the server is running the first mnogodb call
    mongo = None

    @staticmethod
    def set_app(app):
        Api.mongo = app.mongo

    @staticmethod
    async def get(request, document):
        db = Api.mongo[api_database]
        print(request.headers)
        isok = await AuthToken.check_token(request.headers['Authorization'])
        if not isok:
            return Helper.response_401(request)

        output = []
        docs = await db[document].find().to_list(length=100)
        for d in docs:
            d.pop('_id')
            output.append(d)
        # for
        return Helper.make_response({'result': output}, 200)

    @staticmethod
    async def post(request, document):
        db = Api.mongo[api_database]
        record = request.json
        if request.json is None:
            return

        if not AuthToken.check_token(request.headers['auth_token']):
            return Helper.response_401(request)

        record['isNew'] = False
        record['isSync'] = True
        mongo_id = await db[document].insert(record)
        output = await db[document].find_one({'_id': mongo_id})
        output.pop("_id")
        return Helper.make_response({'result': output}, 200)

    @staticmethod
    async def put(request, document):
        db = Api.mongo[api_database]
        record = request.json
        if not AuthToken.check_token(request.headers['auth_token']):
            return Helper.response_401(request)

        record['isNew'] = False
        record['isSync'] = True
        record_old = await db[document].find_one({'id': record["id"]})
        output = await db[document].replace_one(record_old, record)
        return Helper.make_response({'result': output}, 200)

    @staticmethod
    async def find(request, args):
        return await Api.get(request, args)

    @staticmethod
    async def insert(request, args):
        return await Api.post(request, args)

    @staticmethod
    async def update(request, args):
        return await Api.put(request, args)
