from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restx import Namespace, Resource

from api.level import get_level, get_level_name
from models import db, User
from my_jwt import create_token, validate_token, get_user_id

User_api = Namespace(name='User_api', description="API for managing users")

bcrypt = Bcrypt()


@User_api.route('')
class UserR(Resource):
    def get(self):
        """
          Get a user with jwt.
        """
        """
          Request:
            GET /users
          Returns:
            {
              "id": 1,
              "email": "email1@naver.com",
              "nickname": "nickname1",
              "image": "image1",
              "point": 0,
              "level_name": "초심자"
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(user_id)

        try:
            user = db.session.get(User, user_id)

            result = {
                'id': user.id,
                'email': user.email,
                'nickname': user.nickname,
                'image': user.image,
                'point': user.point,
                'level_name': get_level_name(user.level_id)
            }

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@User_api.route('/join')
class Join(Resource):
    def post(self):
        """
        Create a new user.
        """
        """
          Request:
            {
              "email": "email1@naver.com",
              "password": "password1",
              "nickname": "nickname1"
            }
          Returns:
            {
              "result": "{result}"
            }
        """
        email = request.json.get('email')
        password = request.json.get('password')
        nickname = request.json.get('nickname')
        print(email, password, nickname)

        if not email or not password or not nickname:
            return jsonify({'result': "회원가입 실패", 'message': "이메일, 비밀번호, 닉네임을 모두 입력해주세요."})

        try:
            if User.query.filter_by(email=email).first():
                result = {'result': "회원가입 실패", 'message': "이미 존재하는 이메일입니다. 새로운 이메일을 입력해주세요."}

            elif User.query.filter_by(nickname=nickname).first():
                result = {'result': "회원가입 실패", 'message': "이미 존재하는 닉네임입니다. 새로운 닉네임을 입력해주세요."}

            else:
                password_hash = bcrypt.generate_password_hash(password)

                user = User(email=email, password=password_hash, nickname=nickname, level_id=get_level())

                db.session.add(user)
                db.session.commit()

                result = {'result': "회원가입 성공"}

        except Exception as e:
            print(e)
            result = {'result': "회원가입 실패"}

        return jsonify(result)


@User_api.route('/login')
class Login(Resource):
    def post(self):
        """
          Create a user's jwt.
        """
        """
          Request:
            {
              "email": "email1@naver.com",
              "password": "password1"
            }
          Returns:
            {
              "result": "로그인 실패"
            }
            or
            {
              "jwt": "{jwt}",
              "result": "로그인 성공"
            }
        """
        email = request.json.get('email')
        password = request.json.get('password')
        print(email, password)

        if not email or not password:
            return jsonify({'result': "로그인 실패", 'message': "이메일, 비밀번호를 모두 입력해주세요."})

        try:
            user = User.query.filter_by(email=email).with_entities(User.id, User.password).first()

            if bcrypt.check_password_hash(user.password, password):
                result = {'result': "로그인 성공", 'jwt': create_token(user.id)}

            else:
                result = {'result': "로그인 실패", 'message': "이메일 또는 비밀번호를 확인해주세요."}

        except Exception as e:
            print(e)
            result = {'result': "로그인 실패"}

        return jsonify(result)


def plus_point(user_id, point):
    print(user_id, point)

    try:
        user = db.session.get(User, user_id)

        new_point = user.point + point
        user.point = new_point

        new_level = get_level(new_point)
        if user.level_id != new_level:
            user.level_id = new_level

    except Exception as e:
        print(e)
        return e


def minus_point(user_id, point):
    print(user_id, point)

    try:
        user = db.session.get(User, user_id)

        new_point = user.point - point
        user.point = new_point

        new_level = get_level(new_point)
        if user.level_id != new_level:
            user.level_id = new_level

    except Exception as e:
        print(e)
        return e


def get_user_nickname(user_id):
    print(user_id)

    try:
        user = db.session.get(User, user_id)

        return user.nickname

    except Exception as e:
        print(e)


def get_user_level(user_id):
    print(user_id)

    try:
        user = db.session.get(User, user_id)

        return get_level_name(user.level_id)

    except Exception as e:
        print(e)
