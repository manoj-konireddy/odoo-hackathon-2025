from flask import jsonify


def response(success=True, message="", data=None):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    })
