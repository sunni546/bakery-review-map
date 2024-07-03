from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Interest, db
from my_jwt import validate_token, get_user_id

Interest_api = Namespace(name='Interest_api', description="API for managing interests")


@Interest_api.route('')
class InterestCR(Resource):
    def get(self):
        """
          Get all interests with jwt.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "bakery_id": 1,
                "bakery_name": "파리바게뜨 부천중동로데오점",
                "bakery_score": 3.0,
                "breads": [
                  "베이글",
                  "소금빵"
                ]
              },
              {
                "id": 2,
                "bakery_id": 2,
                "bakery_name": "비플로우",
                "bakery_score": 4.0,
                "breads": [
                  "소금빵"
                ]
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(user_id)

        result = []

        try:
            interests = Interest.query.filter_by(user_id=user_id).all()
            for interest in interests:
                r = make_result(interest)

                from api.bakery import get_bakery_score, get_bakery_name
                from api.bread import get_category_names_in_breads
                r['bakery_name'] = get_bakery_name(interest.bakery_id)
                r['bakery_score'] = round(get_bakery_score(interest.bakery_id), 1)
                r['breads'] = get_category_names_in_breads(interest.bakery_id)

                result.append(r)

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new interest with jwt.
        """
        """
          Request:
            {
              "bakery_id": 1
            }
          Returns:
            {
              "id": 1,
              "bakery_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        bakery_id = request.json.get('bakery_id')
        user_id = get_user_id(token)
        print(bakery_id, user_id)

        try:
            if Interest.query.filter_by(bakery_id=bakery_id, user_id=user_id).first():
                result = {'result': "추가 실패", 'message': "이미 관심 추가한 빵집입니다."}

            else:
                interest = Interest(bakery_id=bakery_id, user_id=user_id)

                db.session.add(interest)
                db.session.commit()

                result = make_result(interest)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Interest_api.route('/<int:id>')
@Interest_api.doc(params={'id': 'Interest ID'})
class InterestD(Resource):
    def delete(self, id):
        """
          Delete an interest with jwt.
        """
        """
          Request:
            DELETE /interests/3
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(id, user_id)

        try:
            interest = db.session.get(Interest, id)

            if interest.user_id != user_id:
                return jsonify({'result': "삭제 실패", 'message': "해당 빵집을 관심 삭제할 권한이 없습니다."})

            db.session.delete(interest)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


@Interest_api.route('/bakery/<int:id>')
@Interest_api.doc(params={'id': 'Bakery ID'})
class InterestWithBakeryIdD(Resource):
    def delete(self, id):
        """
          Delete an interest with jwt and Bakery ID.
        """
        """
          Request:
            DELETE /interests/bakery/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(id, user_id)

        try:
            interest = Interest.query.filter_by(bakery_id=id, user_id=user_id).first()

            if not interest:
                return jsonify({'result': "삭제 실패", 'message': "해당 빵집은 관심이 아닙니다."})

            db.session.delete(interest)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(interest):
    result = {
        'id': interest.id,
        'bakery_id': interest.bakery_id
    }

    return result


def is_interested(bakery_id, user_id):
    print(bakery_id, user_id)

    try:
        interest = Interest.query.filter_by(bakery_id=bakery_id, user_id=user_id).first()

        if interest:
            return True
        else:
            return False

    except Exception as e:
        print(e)
