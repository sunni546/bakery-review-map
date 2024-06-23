from flask import jsonify
from flask_restx import Namespace, Resource

from models import Bread, db

Bread_api = Namespace(name='Bread_api', description="API for managing breads")


@Bread_api.route('')
class BreadR(Resource):
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


def make_result(bread):
    result = {
        'id': bread.id,
        'review_count': bread.review_count,
        'bakery_id': bread.bakery_id,
        'category_id': bread.category_id
    }

    return result


def add_category_in_breads(bakery_id, category_ids):
    print(bakery_id, category_ids)

    try:
        for category_id in category_ids:
            bread = Bread.query.filter_by(bakery_id=bakery_id, category_id=category_id).first()

            if bread:
                bread.review_count += 1

            else:
                bread = Bread(bakery_id=bakery_id, category_id=category_id)
                db.session.add(bread)

    except Exception as e:
        print(e)
        return e


def delete_category_in_breads(bakery_id, category_ids):
    print(bakery_id, category_ids)

    try:
        for category_id in category_ids:
            bread = Bread.query.filter_by(bakery_id=bakery_id, category_id=category_id).first()

            if bread.review_count - 1:
                bread.review_count -= 1

            else:
                db.session.delete(bread)

    except Exception as e:
        print(e)
        return e


def get_category_names_in_breads(bakery_id):
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
