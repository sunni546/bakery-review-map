from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import Level, db

Level_api = Namespace(name='Level_api', description="API for managing levels")

level_fields = Level_api.model('Level', {
    'name': fields.String(description='Level name', required=True, example="초심자"),
    'point': fields.Integer(description='Level point', required=True, example=0)
})


@Level_api.route('')
class LevelCR(Resource):
    def get(self):
        """
          Get all levels.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "name": "초심자",
                "point": 0
              },
              {
                "id": 2,
                "name": "하수",
                "point": 100
              },
              ...
            ]
        """
        result = []

        try:
            levels = Level.query.all()
            for level in levels:
                result.append(make_result(level))

        except Exception as e:
            print(e)

        return jsonify(result)

    @Level_api.expect(level_fields)
    def post(self):
        """
          Create a new level.
        """
        """
          Request:
            {
              "name": "초심자",
              "point": 0
            }
          Returns:
            {
              "id": 1,
              "name": "초심자",
              "point": 0
            }
        """
        name = request.json.get('name')
        point = request.json.get('point')
        print(name, point)

        try:
            level = Level(name=name, point=point)

            db.session.add(level)
            db.session.commit()

            result = make_result(level)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Level_api.route('/<int:id>')
@Level_api.doc(params={'id': 'Level ID'})
class LevelRUD(Resource):
    def get(self, id):
        """
          Get a level with ID.
        """
        """
          Request:
            GET /levels/1
          Returns:
            {
              "id": 1,
              "name": "초심자",
              "point": 0
            }
        """
        print(id)

        try:
            level = db.session.get(Level, id)

            result = make_result(level)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    @Level_api.expect(level_fields)
    def patch(self, id):
        """
          Update a level.
        """
        """
          Request:
            PATCH /levels/3
            {
              "name": "중수",
              "point": 1000
            }
          Returns:
            {
              "id": 3,
              "name": "중수",
              "point": 1000
            }
        """
        name = request.json.get('name')
        point = request.json.get('point')
        print(id, name, point)

        if not name or not point:
            return jsonify({'result': "수정 실패", 'message': "수정할 내용을 입력해주세요."})

        try:
            level = db.session.get(Level, id)

            if name and level.name != name:
                level.name = name
            if point and level.point != point:
                level.point = point

            db.session.commit()

            result = make_result(level)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a level.
        """
        """
          Request:
            DELETE /levels/3
          Returns:
            {}
        """
        print(id)

        try:
            level = db.session.get(Level, id)

            db.session.delete(level)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(level):
    result = {
        'id': level.id,
        'name': level.name,
        'point': level.point
    }

    return result
