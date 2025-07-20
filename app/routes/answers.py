from flask import Blueprint, request, jsonify
from config import db
from app.models import Answer
from sqlalchemy.exc import SQLAlchemyError

answers_blp = Blueprint('answers_blp', __name__)

@answers_blp.route('/submit', methods=['POST'])
def submit_answers():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({'error': '리스트 형식의 데이터가 필요합니다.'}), 400

        if not data:
            return jsonify({'error': '빈 리스트는 허용되지 않습니다.'}), 400

        user_id = data[0].get("user_id")
        if user_id is None:
            return jsonify({'error': 'user_id는 필수입니다.'}), 400

        for entry in data:
            if 'user_id' not in entry or 'choice_id' not in entry:
                return jsonify({'error': 'user_id와 choice_id는 필수입니다.'}), 400

            if entry['user_id'] != user_id:
                return jsonify({'error': '모든 항목의 user_id는 동일해야 합니다.'}), 400

            answer = Answer(
                user_id=entry['user_id'],
                choice_id=entry['choice_id']
            )
            db.session.add(answer)

        db.session.commit()

        return jsonify({
            "message": f"User: {user_id}'s answers Success Create"
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'DB 오류: {str(e)}'}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500