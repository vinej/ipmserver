from rest.helper import Helper, api_database


class Admin:

    def __init__(self, app):
        self.app = app

    async def command(self, request, cmd):
        if cmd == "drop_users":
            return await self.drop_users()

        response_object = {
            'status': 'failed',
            'message': 'Failed drop users'
        }
        return Helper.make_response(response_object, 500)

    async def drop_users(self):
        db = self.app.mongo[api_database]
        await db.drop_collection('users')
        response_object = {
            'status': 'success',
            'message': 'drop collection users'
        }
        return Helper.make_response(response_object, 200)
