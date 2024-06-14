from flask import request, jsonify
from flask_restx import Namespace, Resource

from api.bread import get_breads_category_names, get_breads_bakery_ids
from api.category import get_category_id
from api.interest import is_interested
from models import Bakery, db
from my_jwt import validate_token, get_user_id

Bakery_api = Namespace(name='Bakery_api', description="API for managing bakeries")


@Bakery_api.route('')
class BakeryCR(Resource):
    def get(self):
        """
          Get all bakeries.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "name": "파리바게뜨 부천중동로데오점",
                "lat": 37.5008651,
                "lng": 126.7758115,
                "interest": true
              },
              {
                "id": 2,
                "name": "비플로우",
                "lat": 37.4954714,
                "lng": 126.7763733,
                "interest": false
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
            bakeries = Bakery.query.all()
            for bakery in bakeries:
                result.append(make_result(bakery, user_id, -1))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new bakery.
        """
        """
          Request:
            {
              "name": "파리바게뜨 부천중동로데오점",
              "address": "경기 부천시 원미구 소향로 251",
              "lat": 37.5008651,
              "lng": 126.7758115
            }
          Returns:
            {
              "id": 1,
              "name": "파리바게뜨 부천중동로데오점",
              "address": "경기 부천시 원미구 소향로 251",
              "lat": 37.5008651,
              "lng": 126.7758115,
              "score": 0,
              "review_number": 0,
              "breads": []
            }
        """
        name = request.json.get('name')
        address = request.json.get('address')
        lat = request.json.get('lat')
        lng = request.json.get('lng')
        print(name, address, lat, lng)

        try:
            bakery = Bakery(name=name, address=address, lat=lat, lng=lng)

            db.session.add(bakery)
            db.session.commit()

            result = make_result(bakery)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Bakery_api.route('/<int:id>')
@Bakery_api.doc(params={'id': 'Bakery ID'})
class BakeryRUD(Resource):
    def get(self, id):
        """
          Get a bakery with ID.
        """
        """
          Request:
            GET /bakeries/1
          Returns:
            {
              "id": 1,
              "name": "파리바게뜨 부천중동로데오점",
              "address": "경기 부천시 원미구 소향로 251",
              "score": 0,
              "review_number": 0,
              "breads": [
                "베이글",
                "소금빵"
              ],
              "interest": true
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(id, user_id)

        try:
            bakery = db.session.get(Bakery, id)

            result = make_result(bakery, user_id, 1)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update a bakery.
        """
        """
          Request:
            PATCH /bakeries/2
            {
              "name": "비플로우",
              "address": "경기 부천시 원미구 부흥로307번길 23 태정빌딩 1층 104호",
              "lat": 37.4954714,
              "lng": 126.7763733
            }
          Returns:
            {
              "id": 2,
              "name": "비플로우",
              "address": "경기 부천시 원미구 부흥로307번길 23 태정빌딩 1층 104호",
              "lat": 37.4954714,
              "lng": 126.7763733,
              "score": 0,
              "review_number": 0,
              "breads": [
                "소금빵"
              ]
            }
        """
        name = request.json.get('name')
        address = request.json.get('address')
        lat = request.json.get('lat')
        lng = request.json.get('lng')
        print(id, name, address, lat, lng)

        if not name and not address and not lat and not lng:
            return jsonify({'result': "수정 실패", 'message': "수정할 내용을 입력해주세요."})

        try:
            bakery = db.session.get(Bakery, id)

            if name and bakery.name != name:
                bakery.name = name
            if address and bakery.address != address:
                bakery.address = address
            if lat and bakery.lat != lat:
                bakery.lat = lat
            if lng and bakery.lng != lng:
                bakery.lng = lng

            db.session.commit()

            result = make_result(bakery)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a bakery.
        """
        """
          Request:
            DELETE /bakeries/3
          Returns:
            {}
        """
        print(id)

        try:
            bakery = db.session.get(Bakery, id)

            db.session.delete(bakery)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


@Bakery_api.route('/location')
class BakeryP(Resource):
    def post(self):
        """
          Get a bakery with location(lat and lng).
        """
        """
          Request:
            POST /bakeries/location
            {
              "lat": 37.5008651,
              "lng": 126.7758115
            }
          Returns:
            {
              "id": 1,
              "name": "파리바게뜨 부천중동로데오점",
              "address": "경기 부천시 원미구 소향로 251",
              "score": 0,
              "review_number": 0,
              "breads": [
                "베이글",
                "소금빵"
              ],
              "interest": true
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)

        lat = request.json.get('lat')
        lng = request.json.get('lng')
        print(user_id, lat, lng)

        try:
            bakery = Bakery.query.filter_by(lat=lat, lng=lng).first()

            result = make_result(bakery, user_id, 1)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Bakery_api.route('/category/<string:category>')
@Bakery_api.doc(params={'category': 'Category ID or name'})
class BakeryR(Resource):
    def get(self, category):
        """
          Get all bakeries with category ID or name.
        """
        """
          Request:
            GET /bakeries/category/2
            or
            GET /bakeries/category/소금빵
          Returns:
            [
              {
                "id": 1,
                "name": "파리바게뜨 부천중동로데오점",
                "address": "경기 부천시 원미구 소향로 251",
                "score": 0,
                "review_number": 0,
                "breads": [
                  "베이글",
                  "소금빵"
                ],
                "interest": true
              },
              {
                "id": 2,
                "name": "비플로우",
                "address": "경기 부천시 원미구 부흥로307번길 23 태정빌딩 1층 104호",
                "score": 0,
                "review_number": 0,
                "breads": [
                  "소금빵"
                ],
                "interest": false
              },
              ...
            ]
            or
            [
              {
                "id": 1,
                "name": "파리바게뜨 부천중동로데오점",
                "lat": 37.5008651,
                "lng": 126.7758115,
                "interest": true
              },
              {
                "id": 2,
                "name": "비플로우",
                "lat": 37.4954714,
                "lng": 126.7763733,
                "interest": false
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(category, user_id)

        result = []

        try:
            if category.isdecimal():
                ids = get_breads_bakery_ids(int(category))

                for id in ids:
                    bakery = db.session.get(Bakery, id)
                    result.append(make_result(bakery, user_id, 1))

            else:
                category_id = get_category_id(category)
                ids = get_breads_bakery_ids(category_id)

                for id in ids:
                    bakery = db.session.get(Bakery, id)
                    result.append(make_result(bakery, user_id, -1))

        except Exception as e:
            print(e)

        return jsonify(result)


def make_result(bakery, user_id=0, k=0):
    result = {
        'id': bakery.id,
        'name': bakery.name
    }

    if k >= 0:
        result['address'] = bakery.address
        result['score'] = bakery.score
        result['review_number'] = bakery.review_number
        result['breads'] = get_breads_category_names(bakery.id)

    if k < 1:
        result['lat'] = float(bakery.lat)
        result['lng'] = float(bakery.lng)

    if k and user_id:
        result['interest'] = is_interested(bakery.id, user_id)

    return result


def add_review(bakery_id, review_score):
    print(bakery_id, review_score)

    try:
        bakery = db.session.get(Bakery, bakery_id)

        bakery.score = (bakery.score * bakery.review_number + review_score) / (bakery.review_number + 1)
        bakery.review_number += 1

        db.session.commit()

    except Exception as e:
        print(e)


def delete_review(bakery_id, review_score):
    print(bakery_id, review_score)

    try:
        bakery = db.session.get(Bakery, bakery_id)

        bakery.score = (bakery.score * bakery.review_number - review_score) / (bakery.review_number - 1)
        bakery.review_number -= 1

        db.session.commit()

    except Exception as e:
        print(e)
