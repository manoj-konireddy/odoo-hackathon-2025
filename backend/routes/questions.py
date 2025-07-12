from flask import Blueprint, request, jsonify
from backend.main import db
from models.question import Question
from models.user import User
from datetime import datetime

questions_bp = Blueprint('questions', __name__)

# Create a question


@questions_bp.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags', '')
    user_id = data.get('user_id')

    if not title or not description or not user_id:
        return jsonify({'error': 'Title, description, and user_id are required'}), 400

    question = Question(
        title=title,
        description=description,
        tags=tags,
        timestamp=datetime.utcnow(),
        user_id=user_id
    )

    db.session.add(question)
    db.session.commit()

    return jsonify({'message': 'Question submitted successfully'}), 201

# Get all questions


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    result = []

    for q in questions:
        result.append({
            'id': q.id,
            'title': q.title,
            'description': q.description,
            'tags': q.tags,
            'timestamp': q.timestamp.isoformat(),
            'user_id': q.user_id
        })

    return jsonify(result)

# Get a single question by ID


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_single_question(question_id):
    question = Question.query.get_or_404(question_id)

    return jsonify({
        'id': question.id,
        'title': question.title,
        'description': question.description,
        'tags': question.tags,
        'timestamp': question.timestamp.isoformat(),
        'user_id': question.user_id
    })
