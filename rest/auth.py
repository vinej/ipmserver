# rest/auth.py

from rest.helper import Helper
from rest.user import User
from rest.auth_token import AuthToken
from rest.black_list_token import BlacklistToken
import bcrypt

class Auth:

    mongo = None

    @staticmethod
    def set_app(app):
        Auth.mongo = app.mongo

    @staticmethod
    async def register(request):
        # get the post data
        post_data = request.json
        # check if user already exists
        the_user = await User.get_user(post_data.get('email'))
        if not the_user:
            try:
                # insert the user
                the_user = await User.post_user(post_data.get('email'), post_data.get('password'), True)
                # generate the auth token
                auth_token = AuthToken.encode_auth_token(the_user.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return Helper.make_response(response_object, 201)
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error': str(e)
                }
                return Helper.make_response(response_object, 401)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return Helper.make_response(response_object, 202)

    @staticmethod
    async def login(request):
        # get the post data
        post_data = request.json
        print(post_data)
        try:
            # fetch the user data
            the_user = await User.get_user(post_data.get('email'))
            #if the_user and post_data.get('password') == the_user.password:
            if the_user and bcrypt.checkpw(post_data.get('password').encode('utf8'), the_user.password):
                auth_token = AuthToken.encode_auth_token(the_user.id)
                print(auth_token)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return Helper.make_response(response_object, 200)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return Helper.make_response(response_object, 404)
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return Helper.make_response(response_object, 500)

    @staticmethod
    async def user(request):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return Helper.make_response(response_object, 401)
        else:
            auth_token = ''

        if auth_token:
            resp = AuthToken.decode_auth_token(auth_token)
            if not Helper.is_bad_token(resp):
                the_user = await User.get_user_by_id(resp)
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': the_user.id,
                        'email': the_user.email,
                        'admin': the_user.admin,
                        'registered_on': the_user.registered_on
                    }
                }
                return Helper.make_response(response_object, 200)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return Helper.make_response(response_object, 401)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return Helper.make_response(response_object, 401)

    @staticmethod
    async def logout(request):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = AuthToken.decode_auth_token(auth_token)
            if not Helper.is_bad_token(resp):
                try:
                    # insert the token
                    await BlacklistToken.post_blacklist(auth_token)
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return Helper.make_response(response_object, 200)
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return Helper.make_response(response_object, 200)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return Helper.make_response(response_object, 401)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return Helper.make_response(response_object, 403)
