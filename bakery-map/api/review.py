from flask import request, jsonify
from flask_restx import Namespace, Resource

from api.bakery import add_review, delete_review, change_review_score
from api.user import plus_point, minus_point
from models import Review, db
from my_jwt import validate_token, get_user_id

Review_api = Namespace(name='Review_api', description="API for managing reviews")


@Review_api.route('')
class ReviewCR(Resource):
    def get(self):
        """
          Get all reviews with jwt.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "content": "베이글 좋아요",
                "image": "review1",
                "score": 5,
                "bakery_id": 1
              },
              {
                "id": 2,
                "content": "소금빵 좋아요",
                "image": null,
                "score": 4,
                "bakery_id": 2
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
            reviews = Review.query.filter_by(user_id=user_id).all()
            for review in reviews:
                result.append(make_result(review))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new review with jwt.
        """
        """
          Request:
            {
              "content": "베이글 좋아요",
              "image": "review1",
              "score": 5,
              "categories": [1],
              "bakery_id": 1
            }
          Returns:
            {
              "id": 1,
              "content": "베이글 좋아요",
              "image": "review1",
              "score": 5,
              "bakery_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        content = request.json.get('content')
        image = request.json.get('image')
        score = request.json.get('score')
        bakery_id = request.json.get('bakery_id')
        user_id = get_user_id(token)
        print(bakery_id, user_id)

        try:
            if Review.query.filter_by(bakery_id=bakery_id, user_id=user_id).first():
                result = {'result': "추가 실패", 'message': "이미 리뷰 작성한 빵집입니다."}

            else:
                review = Review(content=content, image=image, score=score, bakery_id=bakery_id, user_id=user_id)

                add_review(bakery_id, score)
                db.session.add(review)
                plus_point(user_id, 10)

                db.session.commit()

                result = make_result(review)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Review_api.route('/<int:id>')
@Review_api.doc(params={'id': 'Review ID'})
class ReviewRUD(Resource):
    def get(self, id):
        """
          Get a review with jwt and ID.
        """
        """
          Request:
            GET /reviews/1
          Returns:
            {
              "id": 1,
              "content": "베이글 좋아요",
              "image": "review1",
              "score": 5,
              "bakery_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(id, user_id)

        try:
            review = db.session.get(Review, id)

            if review.user_id != user_id:
                return jsonify({'result': "조회 실패", 'message': "해당 리뷰를 조회할 권한이 없습니다."})

            result = make_result(review)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update a review with jwt.
        """
        """
          Request:
            PATCH /reviews/2
            {
              "content": "소금빵 좋아요",
              "score": 4
            }
          Returns:
            {
              "id": 2,
              "content": "소금빵 좋아요",
              "image": null,
              "score": 4,
              "bakery_id": 2
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        content = request.json.get('content')
        image = request.json.get('image')
        score = request.json.get('score')
        user_id = get_user_id(token)
        print(id, content, image, score, user_id)

        if not content and not image and not score:
            return jsonify({'result': "수정 실패", 'message': "수정할 내용을 입력해주세요."})

        try:
            review = db.session.get(Review, id)

            if review.user_id != user_id:
                return jsonify({'result': "수정 실패", 'message': "해당 리뷰를 수정할 권한이 없습니다."})

            if content and review.content != content:
                review.content = content

            if image and review.image != image:
                review.image = image

            if score and review.score != score:
                change_review_score(review.bakery_id, review.score, score)
                review.score = score

            db.session.commit()

            result = make_result(review)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a review with jwt.
        """
        """
          Request:
            DELETE /reviews/3
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        user_id = get_user_id(token)
        print(id, user_id)

        try:
            review = db.session.get(Review, id)

            if review.user_id != user_id:
                return jsonify({'result': "삭제 실패", 'message': "해당 리뷰를 삭제할 권한이 없습니다."})

            delete_review(review.bakery_id, review.score)
            db.session.delete(review)
            minus_point(user_id, 10)

            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(review):
    result = {
        'id': review.id,
        'content': review.content,
        'image': review.image,
        'score': review.score,
        'bakery_id': review.bakery_id
    }

    return result
