from flask import Blueprint, request, jsonify
from config import db
from app.models import Choices
from sqlalchemy.exc import SQLAlchemyError

choices_blp = Blueprint('choices_blp', __name__)

# POST - 선택지 생성
@choices_blp.route('/choice', methods=['POST'])
def create_choice():
    try:
        data = request.get_json()

        content = data.get("content")
        is_active = data.get("is_active", True)
        sqe = data.get("sqe")
        question_id = data.get("question_id")

        if not content or sqe is None or question_id is None:
            return jsonify({"error": "content, sqe, question_id는 필수 입력입니다."}), 400

        choice = Choices(
            content=content,
            is_active=is_active,
            sqe=sqe,
            question_id=question_id
        )

        db.session.add(choice)
        db.session.commit()

        return jsonify({
            "message": f"Content: 새로운 선택지 choice Success Create"
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500

# GET - 특정 질문에 대한 선택지 조회
@choices_blp.route('/choice/<int:question_id>', methods=['GET'])
def get_choices_by_question_id(question_id):
    try:
        choices = (
            Choices.query
            .filter_by(question_id=question_id, is_active=True)
            .order_by(Choices.sqe)
            .all()
        )

        if not choices:
            return jsonify({"error": "해당 질문의 선택지를 찾을 수 없습니다."}), 404

        return jsonify([
            {
                "id": choice.id,
                "question_id": choice.question_id,
                "content": choice.content,
                "sqe": choice.sqe,
                "is_active": choice.is_active
            }
            for choice in choices
        ]), 200

    except Exception as e:
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500


# PUT - 선택지 수정
@choices_blp.route('/choice/<int:choice_id>', methods=['PUT'])
def update_choice(choice_id):
    try:
        choice = Choices.query.get(choice_id)
        if not choice:
            return jsonify({"error": "해당 ID의 선택지를 찾을 수 없습니다."}), 404

        data = request.get_json()

        if 'content' in data:
            choice.content = data['content']
        if 'sqe' in data:
            choice.sqe = data['sqe']
        if 'is_active' in data:
            choice.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            "message": f"ID {choice.id}번 선택지 수정 완료",
            "choice": {
                "id": choice.id,
                "question_id": choice.question_id,
                "content": choice.content,
                "sqe": choice.sqe,
                "is_active": choice.is_active
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500


# DELETE - 선택지 삭제
@choices_blp.route('/choice/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    try:
        choice = Choices.query.get(choice_id)
        if not choice:
            return jsonify({"error": "해당 ID의 선택지를 찾을 수 없습니다."}), 404

        db.session.delete(choice)
        db.session.commit()

        return jsonify({"message": f"ID {choice.id}번 선택지 삭제 완료"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500