import json
from flask import Flask, jsonify, request
import db
from pydantic import ValidationError
from models import User
from loggers import logger
from middleware import register_middleware

app = Flask(__name__)
register_middleware(app)


@app.route("/")
def index():
    return jsonify({"message": "Hello, World!"})


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    try:
        user = User.model_validate(
            {"id": db._next_id, **data},
            context={"users": db._users},
        )
    except ValidationError as e:
        return jsonify({"error": json.loads(e.json())}), 400
    db._users.append(user)
    db._next_id += 1

    return jsonify(user.model_dump()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)