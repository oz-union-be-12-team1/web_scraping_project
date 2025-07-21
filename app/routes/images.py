from flask import Blueprint, request, jsonify
from config import db
from app.models import Image, ImageType
from sqlalchemy.exc import SQLAlchemyError

images_blp = Blueprint('images', __name__)

# 1. 이미지 생성
@images_blp.route('/image', methods=['POST'])
def create_image():
    data = request.get_json()
    url = data.get("url")
    type_str = data.get("type")

    if not url or not type_str:
        return jsonify({"error": "url과 type은 필수입니다."}), 400

    try:
        image_type = ImageType(type_str.lower())
    except ValueError:
        return jsonify({"error": "type은 'main' 또는 'sub'이어야 합니다."}), 400

    image = Image(url=url, type=image_type)

    try:
        db.session.add(image)
        db.session.commit()
        return jsonify({"message": f"ID: {image.id} Image Success Create"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500


@images_blp.route('/image/main', methods=['GET'])
def get_main_image():
    try:
        image = Image.query.filter_by(type=ImageType.MAIN).order_by(Image.created_at.desc()).first()
        if not image:
            return jsonify({"image": None}), 200
        return jsonify({"image": image.url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@images_blp.route('/image/sub', methods=['GET'])
def get_sub_images():
    try:
        sub_images = Image.query.filter_by(type=ImageType.SUB).order_by(Image.created_at.desc()).all()
        result = [{"id": img.id, "url": img.url} for img in sub_images]
        return jsonify({"images": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@images_blp.route('/image/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "해당 ID의 이미지를 찾을 수 없습니다."}), 404

    data = request.get_json()
    url = data.get("url")
    type_str = data.get("type")

    if url:
        image.url = url

    if type_str:
        try:
            image.type = ImageType(type_str.lower())
        except ValueError:
            return jsonify({"error": "type은 'main' 또는 'sub' 중 하나여야 합니다."}), 400

    try:
        db.session.commit()
        return jsonify({
            "message": f"ID {image.id}번 이미지 수정 완료",
            "image": {
                "id": image.id,
                "url": image.url,
                "type": image.type.value
            }
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500


@images_blp.route('/image/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "해당 ID의 이미지를 찾을 수 없습니다."}), 404

    try:
        db.session.delete(image)
        db.session.commit()
        return jsonify({"message": f"ID {image.id}번 이미지 삭제 완료"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"DB 오류: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500