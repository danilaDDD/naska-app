import logging
from flask import Flask, jsonify, request
import db
from pydantic import ValidationError
from models import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
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
        return jsonify({"error": e.errors()}), 400
    db._users.append(user)
    db._next_id += 1
    logger.info("Created user id=%d name=%s", user.id, user.name)
    return jsonify(user.model_dump()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)