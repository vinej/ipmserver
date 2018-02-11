import datetime
import jwt
from rest.black_list_token import BlacklistToken
from rest.helper import Helper


class AuthToken:

    app = None

    @staticmethod
    def set_app(app):
        AuthToken.app = app

    @staticmethod
    async def check_token(auth_token):
        if not auth_token:
            return False

        # bearer TOKEN
        auth_token = auth_token[7:]
        resp = await AuthToken.decode_auth_token(auth_token)
        print(f'rest = {resp}')
        if Helper.is_bad_token(resp):
            return False
        return True

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=500),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            #return jwt.encode(payload, AuthToken.app.config.get('SECRET_KEY'), algorithm='HS256')
            return jwt.encode(payload, 'my_precious', algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    async def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            #payload = jwt.decode(auth_token, AuthToken.app.config.get('SECRET_KEY'))
            print(auth_token)
            payload = jwt.decode(auth_token, 'my_precious')
            is_blacklisted_token = await BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'BadToken: blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'BadToken: Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'BadToken: Invalid token. Please log in again.'
