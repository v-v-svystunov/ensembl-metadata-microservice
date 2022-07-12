from flask import Response, jsonify, make_response

def check_request_parameters_rules(organism_name,release,dtype):
    if organism_name is None and release is None and dtype is None:
        return {'message': '400 - Name and/or release and/or type should be defined by request', 'code': 400}

    if (organism_name is not None) and (len(organism_name)<3):
        return {'message': '400 - Name should be no less then 3 characters long', 'code': 400}
    
    if (release is not None) and (release.isnumeric() is False):
        return {'message': '400 - Release parameter did not place as integer', 'code': 400}

    return {'message': '', 'code': 0}

def build_response_non_organism_found(organism_name,cursor,verbose):
    if organism_name is not None:
        sql_select_Query = "SHOW DATABASES WHERE `database` LIKE '"+str(organism_name)+"_%'"
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            return  Response("404 - Organism is not found",status=404)
        else:
            response = make_response(jsonify([]),200,)
        response.headers["Content-Type"] = "application/json"
        return response
    
    response = make_response(jsonify([]),200,)
    response.headers["Content-Type"] = "application/json"

    return response
