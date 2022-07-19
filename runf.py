from flask import Flask, request, Response, jsonify, make_response
import mysql.connector
from mysql.connector import Error
from config import get_defined_method_list, get_db_host, get_db_user, get_db_pass, get_db_name
import MainLib
import OrganismLib

"""
    TODO LIST ::
        all uinterface methods lke post put... 
        should be changed into @app.post @app.put instead @app.route

        should be added escape{string} for all user input
"""

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# an interface processor for HTTP GET request
#
@app.route("/databases", methods=get_defined_method_list())
def define_organism_data():
    # check if HTTP method is kind of GET
    #
    if MainLib.check_method() is not True:
        return Response(MainLib.get_methos_problem_message(),status=MainLib.get_method_problem_code())

    # parse request parameters to the ini parameters
    #
    args = request.args
    organism_name = args.get('name')
    release = args.get('release')
    dtype =  args.get('type')
    verbose = args.get('v')

    # quick hack -- switch verbose to the True
    #
    if verbose is None:
        verbose = True

    # apply bussines rules to check parameters
    #
    checked_request_parameters = OrganismLib.check_request_parameters_rules(organism_name=organism_name,release=release,dtype=dtype)
    if checked_request_parameters['code'] != 0:
        return Response(checked_request_parameters['message'],status=checked_request_parameters['code'])        


    try:
        # open connection by prediffined parameters by config
        #
        connection = mysql.connector.connect(host=get_db_host(),
                                             database=get_db_name(),
                                             user=get_db_user(),
                                             password=get_db_pass())
        
        if connection.is_connected():

            db_Info = connection.get_server_info()
            if verbose is True:
                print("Connected to MySQL Server version ", db_Info)
            
            # SQL requst builder ::
            #

            sql_select_Query = "SELECT gd.dbname FROM genome_database AS gd WHERE "
            sql_cond_row = ""
            if dtype is not None: 
                sql_cond_row = "gd.type='"+dtype+"' "

            if release is not None:
                if sql_cond_row != "":
                    sql_cond_row = sql_cond_row + " AND gd.dbname LIKE '%_"+release+"_%'"
                else:
                    sql_cond_row = "gd.dbname LIKE '%_"+release+"_%'"

            if organism_name is not None:
                if sql_cond_row != "":
                    sql_cond_row = sql_cond_row + " AND gd.genome_id IN (SELECT distinct(genome_id) FROM genome WHERE organism_id IN (SELECT distinct(organism_id) FROM organism WHERE name='"+organism_name+"' OR scientific_name = '"+organism_name+"'))"
                else:
                    sql_cond_row = "gd.genome_id IN (SELECT distinct(genome_id) FROM genome WHERE organism_id IN (SELECT distinct(organism_id) FROM organism WHERE name='"+organism_name+"' OR scientific_name = '"+organism_name+"'))"

            sql_select_Query = sql_select_Query + sql_cond_row                     

            
            print ("\n\n"+sql_select_Query+"\n\n")
            
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)

            print ("\n\n"+sql_select_Query+"\n\n")

            # get all records
            #
            records = cursor.fetchall()

            # apply bussines rules to inform that organism was not found
            #
            if cursor.rowcount == 0:
                return OrganismLib.build_response_non_organism_found(organism_name=organism_name,cursor=cursor,verbose=verbose)
                    

            # prepare response structure based on organism's list obtained by request
            #
            response = []
            for row in records:
                db_attr = row[0].split("_")
                
                response.append({"dbname":str(row[0]),"release":db_attr[len(db_attr)-2],"dbtype":db_attr[len(db_attr)-3],"organism":"_".join(db_attr[0:len(db_attr)-3])})

            response = make_response(jsonify(response),200,)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            if verbose is True:
                print("Problem - Not connected to database")

    except Error as e:
        if verbose is True:
            print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            if verbose is True:
                print("MySQL connection is closed")

    return Response("500 - Unexpected Server problem occured",status=500)

# an interface processor for HTTP POST request
#
@app.route("/databases_post", methods=get_defined_method_list())
def do_something_by_post():
    if request.method not in ['GET']:
        return "<p>Only GET HTTP Request can be processed by this service!</p>"
    return "<p>Reserved to realize HTTP POST logic</p>"

# an interface processor for HTTP PUT request
#
@app.route("/databases_put", methods=get_defined_method_list())
def do_something_by_put():
    if request.method not in ['GET']:
        return "<p>Only GET HTTP Request can be processed by this service!</p>"
    return "<p>Reserved to realize HTTP PUT logic</p>"

# an interface processor for HTTP PATCH request
#
@app.route("/databases_patch", methods=get_defined_method_list())
def do_something_by_patch():
    if request.method not in ['GET']:
        return "<p>Only GET HTTP Request can be processed by this service!</p>"
    return "<p>Reserved to realize HTTP PATCH logic</p>"

# an interface processor for HTTP DELETE request
#
@app.route("/databases_delete", methods=get_defined_method_list())
def do_something_by_delete():
    if request.method not in ['GET']:
        return "<p>Only GET HTTP Request can be processed by this service!</p>"
    return "<p>Reserved to realize HTTP DELETE logic</p>"