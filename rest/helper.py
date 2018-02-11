
from sanic import response

api_database = "restdb"


class Helper:

    @staticmethod
    def make_response(data, status):
        return response.json(
            data,
            headers={'X-Served-By': 'sanic'},
            status=status)

    @staticmethod
    def is_bad_token(resp):
        return resp[0:9] == "BadToken:"

    @staticmethod
    def response_401(request):
        response_object = \
            dict(
                status='401',
                redirect=request.url,
                message='BadToken or no auth_token')
        return Helper.make_response(response_object, 401)

    @staticmethod
    def get_date(date_str="", the_format="%Y-%m-%dT%H:%M:%S%z"):
        from datetime import datetime
        if not date_str:
            return datetime.today().date()
        return datetime.strptime(date_str, the_format).date()
