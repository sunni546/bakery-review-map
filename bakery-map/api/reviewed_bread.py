from flask import jsonify
from flask_restx import Namespace, Resource

from models import db, ReviewedBread

ReviewedBread_api = Namespace(name='ReviewedBread_api', description="API for managing reviewed_breads")


@ReviewedBread_api.route('')
class ReviewedBreadR(Resource):
    def get(self):
        """
          Get all reviewed_breads.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "review_id": 1,
                "category_id": 1
              },
              {
                "id": 2,
                "review_id": 2,
                "category_id": 2
              },
              ...
            ]
        """
        result = []

        try:
            reviewed_breads = ReviewedBread.query.all()

            for reviewed_bread in reviewed_breads:
                result.append(make_result(reviewed_bread))

        except Exception as e:
            print(e)

        return jsonify(result)


@ReviewedBread_api.route('/<int:id>')
@ReviewedBread_api.doc(params={'id': 'ReviewedBread ID'})
class ReviewedBreadD(Resource):
    def delete(self, id):
        """
          Delete reviewed_bread.
        """
        """
          Request:
            DELETE /reviewed_breads/3
          Returns:
            {}
        """
        print(id)

        try:
            reviewed_bread = db.session.get(ReviewedBread, id)

            db.session.delete(reviewed_bread)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(reviewed_bread):
    result = {
        'id': reviewed_bread.id,
        'review_id': reviewed_bread.review_id,
        'category_id': reviewed_bread.category_id
    }

    return result


def set_category_in_reviewed_breads(review_id, category_ids):
    print(review_id, category_ids)

    try:
        for category_id in category_ids:
            reviewed_bread = ReviewedBread(review_id=review_id, category_id=category_id)

            db.session.add(reviewed_bread)

        db.session.commit()

    except Exception as e:
        print(e)
        return e


def get_category_names_in_reviewed_breads(review_id):
    print(review_id)

    category_names = []

    try:
        reviewed_breads = (ReviewedBread.query.filter_by(review_id=review_id)
                           .with_entities(ReviewedBread.category_id).all())

        for reviewed_bread in reviewed_breads:
            from api.category import get_category_name
            category_name = get_category_name(reviewed_bread.category_id)

            category_names.append(category_name)

        return category_names

    except Exception as e:
        print(e)
