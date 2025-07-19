from flask import Blueprint, request, jsonify
from app.models import db, User
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/signup', methods=['POST'])
def create_user():

    data = request.get_json()

    try:
        user = User(
            name=data['name'],
            age=data['age'],
            gender=data['gender'], 
            email=data['email']
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': '등록되었습니다!',
            'user': {
                'id': user.id,
                'name': user.name,
                'age': user.age,
                'gender': user.gender,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        }), 201
    except KeyError as e:
        return jsonify({"error": f"필수 입력이 누락되었습니다: {str(e)}"}), 400

    except ValueError as e:
        return jsonify({"error": f"입력 값 오류: {str(e)}"}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "이미 존재하는 이메일입니다."}), 409

    except Exception as e:
        return jsonify({"error": f"알 수 없는 오류: {str(e)}"}), 500