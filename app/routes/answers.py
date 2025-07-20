from flask import Blueprint, request, jsonify
from config import db
from app.models import Answer
from sqlalchemy.exc import SQLAlchemyError

answers_bp = Blueprint('answers', __name__, url_prefix='/answers')

@answers_bp.route('', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()

        required_fields = ['question_id', 'user_id', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field}는 필수 입력입니다.'}), 400

        answer = Answer(
            question_id=data['question_id'],
            user_id=data['user_id'],
            content=data['content']
        )

        db.session.add(answer)
        db.session.commit()

        return jsonify({
            'message': '답변이 성공적으로 저장되었습니다.',
            'answer': {
                'id': answer.id,
                'question_id': answer.question_id,
                'user_id': answer.user_id,
                'content': answer.content,
                'created_at': answer.created_at.isoformat() if answer.created_at else None
            }
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'DB 오류: {str(e)}'}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500