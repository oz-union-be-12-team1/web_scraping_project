from flask import Flask, Blueprint, jsonify, abort, request
from config import db
from app.models import Choices, Question

choices_bp = Blueprint("choices", __name__, url_prefix='/choice')

# 선택지 생성
@choices_bp.route('', methods=['POST'])
def create_choice():
    data = request.get_json()

    if not all(data.get(field) for field in ['question_id', 'content', 'sqe']):
        return jsonify({"error" : "question_id, content, sqe 중 값이 없는 게 있습니다. 다시 확인해 주세요." }), 400

    new_choice = Choices(
        question_id=data['question_id'],
        content=data['content'],
        sqe=data['data'],
        is_active=True
    ) 

    db.session.add(new_choice)
    db.session.commit()

    return jsonify({
        "id" : new_choice.id,
        "question_id" : new_choice.question_id,
        "content" : new_choice.content,
        "sqe" : new_choice.sqe,
        "is_active" : new_choice.is_active
    })
