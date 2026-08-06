from flask import Blueprint, jsonify, request
from datetime import datetime
from backend.app.container import get_poll_service, get_vote_service
from backend.infrastructure.redis.redis_client import redis_client


api_blueprint = Blueprint("api", __name__)


# ─── Health Check ───────────────────────────────────────────────────────────

@api_blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


# ─── Create Poll ────────────────────────────────────────────────────────────

@api_blueprint.route("/polls", methods=["POST"])
def create_poll():
    data = request.get_json()
    poll_service = get_poll_service()

    question = data["question"]
    options = data["options"]
    created_by = data["created_by"]

    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])

    poll = poll_service.create_poll(
        question=question,
        options=options,
        created_by=created_by,
        start_time=start_time,
        end_time=end_time
    )

    return jsonify({
        "poll_id": poll.public_id,
        "question": poll.question,
        "options": [{"id": o.id, "text": o.text} for o in poll.options]
    })


# ─── List All Polls (with status badges for table) ──────────────────────────

@api_blueprint.route("/polls", methods=["GET"])
def get_polls():
    poll_service = get_poll_service()
    polls = poll_service.list_all_polls_with_status()
    return jsonify(polls)


# ─── Get Single Poll Detail (with timer + status) ───────────────────────────

@api_blueprint.route("/polls/<public_id>", methods=["GET"])
def get_poll_detail(public_id):
    poll_service = get_poll_service()
    poll = poll_service.get_poll_with_status(public_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404
    return jsonify(poll)


# ─── Cast Vote ──────────────────────────────────────────────────────────────

@api_blueprint.route("/polls/<public_id>/vote", methods=["POST"])
def vote(public_id):
    data = request.json

    option_id = data.get("option_id")
    user_id = data.get("user_id")
    option_text = data.get("option_text")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    vote_service = get_vote_service()

    try:
        vote_service.vote(public_id, option_id, user_id, option_text=option_text)
        return jsonify({"message": "Vote cast successfully"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# ─── Get Poll Results ───────────────────────────────────────────────────────

@api_blueprint.route("/polls/<poll_id>/results", methods=["GET"])
def get_results(poll_id):
    # 1. Try to get real-time data from Redis
    key = f"poll:{poll_id}"
    redis_results = redis_client.hgetall(key)
    if redis_results is None:
        redis_results = {}

    # 2. Convert Redis bytes to a clean dictionary
    results = {
        k.decode() if isinstance(k, bytes) else k: int(v)
        for k, v in redis_results.items()
    }

    # 3. If Redis empty, fetch options from DB so buttons appear
    if not results:
        poll_service = get_poll_service()
        poll = poll_service.get_poll(poll_id)
        if poll:
            results = {o.text: 0 for o in poll.options}

    return jsonify({
        "poll_id": poll_id,
        "results": results
    })