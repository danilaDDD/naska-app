import json
from flask import Flask, jsonify, request
import db
from pydantic import ValidationError
from models import User, PutUserRequest
from loggers import logger
from middleware import register_middleware

app = Flask(__name__)
app.url_map.strict_slashes = False
register_middleware(app)


@app.route("/")
def index():
    return jsonify({"message": "Hello, World!"})


@app.route("/api/users", methods=["GET"])
def list_users():
    return jsonify({"users": [u.model_dump() for u in db._users]})


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = next((u for u in db._users if u.id == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.model_dump())


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


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    user = next((u for u in db._users if u.id == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json(silent=True) or {}
    others = [u for u in db._users if u.id != user_id]
    try:
        body = PutUserRequest.model_validate(data, context={"users": others})
    except ValidationError as e:
        return jsonify({"error": json.loads(e.json())}), 400
    updated = user.model_copy(update=body.model_dump(exclude_none=True))
    db._users[db._users.index(user)] = updated
    return jsonify(updated.model_dump()), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)