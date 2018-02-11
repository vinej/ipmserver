import datetime
import jwt
from rest.black_list_token import BlacklistToken
from rest.helper import Helper
import logging


class AuthToken:

    def __init__(self, app):
        self.app = app
        self.black_list_token = BlacklistToken(app)

    async def check_token(self, request):
        if "Autorization" not in request.headers:
            return False

        auth_token = request.headers['Authorization']
        if not auth_token:
            return False

        # bearer TOKEN
        auth_token = auth_token[7:]
        resp = await self.decode_auth_token(auth_token)
        if Helper.is_bad_token(resp):
            return False
        return True

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        return: string
        """
        logging.debug(f'encode_auth_token : {user_id}')
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=500),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, "self.app.config.get('SECRET_KEY')", algorithm='HS256')
        except Exception as e:
            return e

    async def decode_auth_token(self, auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        logging.debug(f'decode_auth_token : {auth_token}')
        try:
            payload = jwt.decode(auth_token, "self.app.config.get('SECRET_KEY')")
            is_blacklisted_token = await self.black_list_token.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'BadToken: blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'BadToken: Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'BadToken: Invalid token. Please log in again.'
