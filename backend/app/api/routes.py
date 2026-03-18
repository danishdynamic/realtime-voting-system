from flask import Blueprint, jsonify, request
from datetime import datetime
from app.container import get_poll_service, get_vote_service
from backend.infrastructure.redis.redis_client import redis_client

api_blueprint = Blueprint("api", __name__)

#adding a health check method
@api_blueprint.route("/health", methods=["GET"])
def health():

  return {"status" : "ok"}

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
        "options": [
           {
               "id": o.id,
               "text": o.text
           }  for o in poll.options]
    })

# get method for active polls

@api_blueprint.route("/polls", methods=["GET"])
def get_polls():

    poll_service = get_poll_service()

    polls = poll_service.get_active_polls()

    result = []

    for poll in polls:
        result.append({
            "poll_id": poll.public_id,
            "question": poll.question,
            "options": [{
                "id": o.id,
                "text": o.text
            } for o in poll.options],
            "start_time": poll.start_time.isoformat(),
            "end_time": poll.end_time.isoformat()
        })

    return jsonify(result)

# endpoint for voting on a poll i.e options of a poll and user id will be sent in the request body and poll id will be sent in the url path

@api_blueprint.route("/polls/<public_id>/vote", methods=["POST"])
def vote(public_id):
     
     data = request.json

     option_id = data.get("option_id")
     user_id = data.get("user_id")

     vote_service = get_vote_service()

     vote_service.vote(public_id, option_id, user_id)

     return jsonify({"message": "Vote cast successfully"})


@api_blueprint.route("/polls/<poll_id>/results", methods=["GET"])
def get_results(poll_id):

    key = f"poll:{poll_id}"

    results : dict = redis_client.hgetall(key)

    results= {k: int(v) for k, v in results.items()}

    return jsonify({
        "poll_id": poll_id,
        "results": results
    })



