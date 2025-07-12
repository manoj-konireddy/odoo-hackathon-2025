from flask import Blueprint, request
from app import mysql
from app.utils import response

votes_bp = Blueprint('votes', __name__)


@votes_bp.route('/vote', methods=['POST'])
def vote():
    data = request.json
    user_id = data['user_id']
    answer_id = data['answer_id']
    vote_type = data['vote_type']  # 'upvote' or 'downvote'

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO votes (user_id, answer_id, vote_type) VALUES (%s, %s, %s)",
                (user_id, answer_id, vote_type))
    mysql.connection.commit()
    cur.close()

    return response(message=f"{vote_type} recorded")
