from flask import Blueprint, request, jsonify
from app.models import User, Age, Gender
from config import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

user_blp = Blueprint('users', __name__)

@user_blp.route("/", methods=["GET"])
def root_index():
    return jsonify({"message": "Success Connect"}), 200


@user_blp.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()

    required_fields = ['name', 'age', 'gender', 'email']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"message": f"다음 필드가 누락되었습니다: {', '.join(missing_fields)}"}), 400

    try:
        user = User(
            name=data['name'],
            age=Age(data['age'].lower()),
            gender=Gender(data['gender'].lower()),
            email=data['email'],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": f"{user.name}님 회원가입을 축하합니다!",
            "user_id": user.id
        }), 200

    except ValueError as e:
        return jsonify({"message": f"입력 값 오류: {str(e)}"}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "이미 존재하는 계정 입니다."}), 409

    except Exception as e:
        return jsonify({"message": f"알 수 없는 오류: {str(e)}"}), 500