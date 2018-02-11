
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

    '''
curl -d '{"id":"vinej", "name":"jean"}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTgzMjI0MzAsImlhdCI6MTUxODMyMTkzMCwic3ViIjoiNWE3ZmIwNmY4YmUxZjVjNmM3ZTc3MDMyIn0.Hi0EI6crSz5QuJMEGMi4yR0ijZOQRvz--314g00VtL0" -X GET http://localhost:8000/api/companies
        curl -d '{"id":"vinej", "name":"jean 23"}' -H "Content-Type: application/json" 
        -X PUT http://localhost:8000/api/companies
        
        curl -d '{"id":"vinej", "email":"jyvinet@hotmail.ca", "password":"123456"}' -H "Content-Type: application/json" -X POST http://localhost:8000/auth/login

"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTgzMjA4NTMsImlhdCI6MTUxODMyMDg0OCwic3ViIjoiNWE3ZmIwN
    '''