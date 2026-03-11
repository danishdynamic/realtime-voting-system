from flask import Blueprint

api_blueprint = Blueprint("api", __name__)

#adding a health check 

@api_blueprint.route("/health", methods = ["GET"])
def health():

    return {"status" : "ok"}