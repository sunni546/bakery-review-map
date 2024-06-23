from flask import request, jsonify
from flask_restx import Namespace, Resource

from api.bakery import add_review_score, subtract_review_score, change_review_score, get_bakery_name
from api.user import plus_point, minus_point, get_user_level, get_user_nickname
from models import Review, db, User
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
                "bakery_id": 1,
                "bakery_name": "파리바게뜨 부천중동로데오점",
                "breads": [
                  "베이글"
                ]
              },
              {
                "id": 2,
                "content": "소금빵 좋아요",
                "image": null,
                "score": 4,
                "bakery_id": 2,
                "bakery_name": "비플로우",
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
            reviews = Review.query.filter_by(user_id=user_id).all()

            for review in reviews:
                result.append(make_result(review, 1))

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
              "bakery_id": 1,
              "category_ids": [1]
            }
          Returns:
            {
              "id": 1,
              "content": "베이글 좋아요",
              "image": "review1",
              "score": 5,
              "bakery_id": 1,
              "bakery_name": "파리바게뜨 부천중동로데오점",
              "breads": [
                "베이글"
              ]
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        content = request.json.get('content')
        image = request.json.get('image')
        score = request.json.get('score')
        bakery_id = request.json.get('bakery_id')
        category_ids = request.json.get('category_ids')
        user_id = get_user_id(token)
        print(bakery_id, user_id)

        try:
            if Review.query.filter_by(bakery_id=bakery_id, user_id=user_id).first():
                result = {'result': "추가 실패", 'message': "이미 리뷰 작성한 빵집입니다."}

            else:
                review = Review(content=content, image=image, score=score, bakery_id=bakery_id, user_id=user_id)

                from api.bread import add_category_in_breads
                add_category_in_breads(bakery_id, category_ids)

                add_review_score(bakery_id, score)
                plus_point(user_id, 10)

                db.session.add(review)
                db.session.commit()

                from api.reviewed_bread import set_category_in_reviewed_breads
                set_category_in_reviewed_breads(review.id, category_ids)

                result = make_result(review, 1)

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
              "bakery_id": 1,
              "bakery_name": "파리바게뜨 부천중동로데오점",
              "user_nickname": "nickname1",
              "user_level": "초심자",
              "breads": [
                "베이글"
              ]
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
              "bakery_id": 2,
              "bakery_name": "비플로우",
              "breads": [
                "소금빵"
              ]
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

            from api.reviewed_bread import get_categories_in_reviewed_breads
            from api.bread import delete_category_in_breads
            categories = get_categories_in_reviewed_breads(id)
            delete_category_in_breads(review.bakery_id, categories)

            subtract_review_score(review.bakery_id, review.score)
            minus_point(user_id, 10)

            db.session.delete(review)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


@Review_api.route('/bakery/<int:id>')
@Review_api.doc(params={'id': 'Bakery ID'})
class ReviewRC(Resource):
    def get(self, id):
        """
          Get all reviews with bakery ID.
        """
        """
          Request:
            GET /reviews/bakery/1
          Returns:
            [
              {
                "id": 3,
                "content": "소금빵 좋아요",
                "image": "review3",
                "score": 1,
                "user_nickname": "nickname2",
                "user_level": "초심자",
                "breads": [
                  "소금빵"
                ]
              },
              {
                "id": 1,
                "content": "베이글 좋아요",
                "image": "review1",
                "score": 5,
                "user_nickname": "nickname1",
                "user_level": "초심자",
                "breads": [
                  "베이글"
                ]
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        print(id)

        result = []

        try:
            reviews = Review.query.filter_by(bakery_id=id).order_by(Review.id.desc()).all()

            for review in reviews:
                result.append(make_result(review, -1))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self, id):
        """
          Get all reviews with bakery ID and level ID.
        """
        """
          Request:
            POST /reviews/bakery/1
            {
              "level_id": 1
            }
          Returns:
            [
              {
                "id": 3,
                "content": "소금빵 좋아요",
                "image": "review3",
                "score": 1,
                "user_nickname": "nickname2",
                "user_level": "초심자",
                "breads": [
                  "소금빵"
                ]
              },
              {
                "id": 1,
                "content": "베이글 좋아요",
                "image": "review1",
                "score": 5,
                "user_nickname": "nickname1",
                "user_level": "초심자",
                "breads": [
                  "베이글"
                ]
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패", 'message': "올바르지 않은 JWT입니다."})

        level_id = request.json.get('level_id')
        print(level_id)

        result = []

        try:
            reviews = (Review.query.join(Review.user).filter(Review.bakery_id == id).filter(User.level_id == level_id)
                       .order_by(Review.id.desc()).all())

            for review in reviews:
                result.append(make_result(review, -1))

        except Exception as e:
            print(e)

        return jsonify(result)


def make_result(review, k=0):
    from api.reviewed_bread import get_category_names_in_reviewed_breads

    result = {
        'id': review.id,
        'content': review.content,
        'image': review.image,
        'score': review.score,
        'breads': get_category_names_in_reviewed_breads(review.id)
    }

    if k >= 0:
        result['bakery_id'] = review.bakery_id
        result['bakery_name'] = get_bakery_name(review.bakery_id)

    if k < 1:
        result['user_nickname'] = get_user_nickname(review.user_id)
        result['user_level'] = get_user_level(review.user_id)

    return result
