from flask import Blueprint, jsonify
from app.models import db, Image, ImageType

images_bp = Blueprint('images', __name__, url_prefix='/images')

@images_bp.route('/main', methods=['GET'])
def get_main_images():
    images = Image.query.filter(Image.type == ImageType.MAIN).all()
    
    return jsonify([
        {
            'id': image.id,
            'url': image.url,
            'type': image.type.value,
            'created_at': image.created_at.isoformat() if image.created_at else None
        }
        for image in images
    ]), 200