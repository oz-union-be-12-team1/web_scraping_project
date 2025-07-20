from flask import Blueprint, request, jsonify
from config import db
from app.models import Image, ImageType
from sqlalchemy.exc import SQLAlchemyError

images_bp = Blueprint('images', __name__, url_prefix='/images')

@images_bp.route('', methods=['POST'])
def create_image():
    try:
        data = request.get_json()
        url = data.get("url")
        type_str = data.get("type")

        if not url or not type_str:
            return jsonify({"error": "url과 type은 필수입니다."}), 400

        try:
            image_type = ImageType(type_str.upper())
        except ValueError:
            return jsonify({"error": "type은 'main' 또는 'sub'이어야 합니다."}), 400

        image = Image(url=url, type=image_type)
        db.session.add(image)
        db.session.commit()

        return jsonify({"message": f"ID: {image.id} Image Success Create"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500