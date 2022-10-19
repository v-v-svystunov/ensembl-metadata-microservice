from flask import jsonify, make_response

class LocalResponse():
    def __init__(self, *args):
        pass

    def buidJsonResponse(self, *args, **kwargs):
        response = {"data":kwargs["data"], "errno":kwargs["errno"], "error":kwargs["error"]}
        response = make_response(jsonify(response),200,)
        response.headers["Content-Type"] = "application/json"
        return response