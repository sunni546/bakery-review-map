from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import Category, db

Category_api = Namespace(name='Category_api', description="API for managing categories")

category_fields = Category_api.model('Category', {
    'name': fields.String(description='Category name', required=True, example="베이글")
})


@Category_api.route('')
class CategoryCR(Resource):
    def get(self):
        """
          Get all categories.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "name": "베이글"
              },
              {
                "id": 2,
                "name": "소금빵"
              },
              ...
            ]
        """
        result = []

        try:
            categories = Category.query.all()
            for category in categories:
                result.append(make_result(category))

        except Exception as e:
            print(e)

        return jsonify(result)

    @Category_api.expect(category_fields)
    def post(self):
        """
          Create a new category.
        """
        """
          Request:
            {
              "name": "베이글"
            }
          Returns:
            {
              "id": 1,
              "name": "베이글"
            }
        """
        name = request.json.get('name')
        print(name)

        try:
            category = Category(name=name)

            db.session.add(category)
            db.session.commit()

            result = make_result(category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Category_api.route('/<int:id>')
@Category_api.doc(params={'id': 'Category ID'})
class CategoryRUD(Resource):
    def get(self, id):
        """
          Get a category with ID.
        """
        """
          Request:
            GET /categories/1
          Returns:
            {
              "id": 1,
              "name": "베이글"
            }
        """
        print(id)

        try:
            category = db.session.get(Category, id)

            result = make_result(category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    @Category_api.expect(category_fields)
    def patch(self, id):
        """
          Update a category.
        """
        """
          Request:
            PATCH /categories/2
            {
              "name": "소금빵"
            }
          Returns:
            {
              "id": 2,
              "name": "소금빵"
            }
        """
        name = request.json.get('name')
        print(id, name)

        if not name:
            return jsonify({'result': "수정 실패", 'message': "수정할 내용을 입력해주세요."})

        try:
            category = db.session.get(Category, id)

            if category.name != name:
                category.name = name
                db.session.commit()

            result = make_result(category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a category.
        """
        """
          Request:
            DELETE /categories/3
          Returns:
            {}
        """
        print(id)

        try:
            category = db.session.get(Category, id)

            db.session.delete(category)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(category):
    result = {
        'id': category.id,
        'name': category.name
    }

    return result


def get_category_name(category_id):
    print(category_id)

    try:
        category = db.session.get(Category, category_id)
        return category.name

    except Exception as e:
        print(e)
