from flask import request
def check_method():
    if request.method not in ['GET']:
        return False 
    return True

def get_methos_problem_message():
    return "405 - Should be used GET as HTTP Request"

def get_method_problem_code():
    return 405