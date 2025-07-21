from flask import Blueprint, jsonify, request
from app.models import Question, Choices
from config import db

questions_blp = Blueprint('questions_blp', __name__)

@questions_blp.route('/questions/<int:question_sqe>', methods=['GET'])
def get_question_by_sqe(question_sqe):
    try:
        question = Question.query.filter_by(sqe=question_sqe, is_active=True).first()

        if not question:
            return jsonify({"error": "해당 질문을 찾을 수 없습니다."}), 404

        image_url = question.image.url if question.image else None

        choices = (
            Choices.query
            .filter_by(question_id=question.id, is_active=True)
            .order_by(Choices.sqe)
            .all()
        )

        result = {
            "id": question.id,
            "title": question.title,
            "image": image_url,
            "choices": [
                {
                    "id": choice.id,
                    "content": choice.content,
                    "is_active": choice.is_active,
                    "sqe": choice.sqe,
                    "question_id": choice.question_id
                }
                for choice in choices
            ]
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@questions_blp.route('/questions/count', methods=['GET'])
def get_question_count():
    try:
        count = Question.query.filter_by(is_active=True).count()
        return jsonify({"total": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@questions_blp.route('/question', methods=['POST'])
def create_question():
    try:
        data = request.get_json()
        title = data.get("title")
        sqe = data.get("sqe")
        is_active = data.get("is_active", True)
        image_id = data.get("image_id")

        if not title or sqe is None or image_id is None:
            return jsonify({"error": "title, sqe, image_id는 필수입니다."}), 400

        question = Question(
            title=title,
            sqe=sqe,
            is_active=is_active,
            image_id=image_id
        )

        db.session.add(question)
        db.session.commit()

        return jsonify({
            "message": f"Title: {title} question Success Create"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@questions_blp.route('/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.get(question_id)

        if not question:
            return jsonify({"error": "해당 ID의 질문을 찾을 수 없습니다."}), 404

        db.session.delete(question)
        db.session.commit()

        return jsonify({
            "message": f"ID {question_id}번 질문 삭제 완료"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500