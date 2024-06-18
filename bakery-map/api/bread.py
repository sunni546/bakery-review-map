from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Bread, db

Bread_api = Namespace(name='Bread_api', description="API for managing breads")


@Bread_api.route('')
class BreadCR(Resource):
    def get(self):
        """
          Get all breads.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "bakery_id": 1,
                "category_id": 1
              },
              {
                "id": 2,
                "bakery_id": 1,
                "category_id": 2
              },
              ...
            ]
        """
        result = []

        try:
            breads = Bread.query.all()
            for bread in breads:
                result.append(make_result(bread))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create new bread.
        """
        """
          Request:
            {
              "bakery_id": 1,
              "category_id": 1
            }
          Returns:
            {
              "id": 1,
              "bakery_id": 1,
              "category_id": 1
            }
        """
        bakery_id = request.json.get('bakery_id')
        category_id = request.json.get('category_id')
        print(bakery_id)

        try:
            if Bread.query.filter_by(bakery_id=bakery_id, category_id=category_id).first():
                result = {'result': "추가 실패", 'message': "이미 해당 빵집에 추가된 빵입니다."}

            else:
                bread = Bread(bakery_id=bakery_id, category_id=category_id)

                db.session.add(bread)
                db.session.commit()

                result = make_result(bread)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Bread_api.route('/<int:id>')
@Bread_api.doc(params={'id': 'Bread ID'})
class BreadD(Resource):
    def delete(self, id):
        """
          Delete bread.
        """
        """
          Request:
            DELETE /breads/3
          Returns:
            {}
        """
        print(id)

        try:
            bread = db.session.get(Bread, id)

            db.session.delete(bread)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(bread):
    result = {
        'id': bread.id,
        'bakery_id': bread.bakery_id,
        'category_id': bread.category_id
    }

    return result


def get_breads_category_names(bakery_id):
    print(bakery_id)

    category_names = []

    try:
        breads = Bread.query.filter_by(bakery_id=bakery_id).with_entities(Bread.category_id).all()

        for bread in breads:
            from api.category import get_category_name
            category_name = get_category_name(bread.category_id)

            category_names.append(category_name)

        return category_names

    except Exception as e:
        print(e)


def get_breads_bakery_ids(category_id):
    print(category_id)

    bakery_ids = []

    try:
        breads = Bread.query.filter_by(category_id=category_id).with_entities(Bread.bakery_id).all()

        for bread in breads:
            bakery_ids.append(bread.bakery_id)

        return bakery_ids

    except Exception as e:
        print(e)
