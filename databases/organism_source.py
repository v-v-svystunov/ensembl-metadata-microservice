from flask import Flask, request, Response, jsonify, make_response
import mysql.connector
from mysql.connector import Error
import databases.local_response as local_response

class OrganismSource():
    def __init__(self, *args):
        self.db = "ensembl_metadata_106"
        self.db_host = "ensembldb.ensembl.org"
        self.db_user = "anonymous"
        self.db_pass = ""
        self.dext =  local_response.LocalResponse()

    def get_organism_metadata_sources_list(self, *args):

        if request.method != 'GET':
            return self.dext.buidJsonResponse(data=[],errno=405,error="Should be used GET as HTTP Request. `"+request.method+"` was used instead.")
        
        # parse request parameters to the ini parameters
        #
        args = request.args
        organism_name = args.get('name')
        release = args.get('release')
        dtype =  args.get('type')
        

        # apply bussines rules to check parameters
        #
        if organism_name is None and release is None and dtype is None:
            return self.dext.buidJsonResponse(data=[],errno=400,error="Name and/or release and/or type should be defined by request")

        if (organism_name is not None) and (len(organism_name)<3):
            return self.dext.buidJsonResponse(data=[],errno=400,error="Name should be no less then 3 characters long")
        
        if (release is not None) and (release.isnumeric() is False):
            return self.dext.buidJsonResponse(data=[],errno=400,error="Release parameter did not place as integer")

        # open connection by prediffined parameters by config
        #
        connection = self.openDbConn(host=self.db_host,
                                     db=self.db,   
                                     user=self.db_user,
                                     password=self.db_pass)
        
        if hasattr(connection, 'is_connected') is False:
            return self.dext.buidJsonResponse(data=[],errno=500,error=connection)

        try:
            if connection.is_connected():

                db_Info = connection.get_server_info()
                
                # SQL requst builder ::
                #
                sql_select_Query = "SHOW DATABASES WHERE `database` REGEXP '"

                if organism_name is not None: 
                    sql_select_Query = sql_select_Query+str(organism_name)
                else:
                     sql_select_Query = sql_select_Query+".*"

                if dtype is not None: 
                    sql_select_Query = sql_select_Query+"_"+str(dtype)+"_"
                else:
                    if organism_name is not None:
                        sql_select_Query = sql_select_Query+".*"

                if release is not None:
                    if dtype is not None:                    
                        sql_select_Query = sql_select_Query+str(release)+"_.*'"
                    else:
                        sql_select_Query = sql_select_Query+"_"+str(release)+"_.*'"
                else:
                    if dtype is not None:
                        sql_select_Query = sql_select_Query+".*'"
                    else:
                      sql_select_Query = sql_select_Query+"'"  

                cursor = connection.cursor()
                cursor.execute(sql_select_Query)

                # get all records
                #
                records = cursor.fetchall()

                if cursor.rowcount == 0:
                    return self.dext.buidJsonResponse(data=[],errno=0,error='')

                # prepare response structure based on organism's list obtained by request
                #
                data = []
                for row in records:
                    db_attr = row[0].split("_")
                    
                    data.append({"dbname":str(row[0]),"release":db_attr[len(db_attr)-2],"dbtype":db_attr[len(db_attr)-3],"organism":"_".join(db_attr[0:len(db_attr)-3])})
                return self.dext.buidJsonResponse(data=data,errno=0,error='')

        except Error as e:
            return self.dext.buidJsonResponse(data=[],errno=500,error="Error while connecting to MySQL :: "+repr(e))
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            else:
                pass
        
        return self.dext.buidJsonResponse(data=[],errno=0,error='')

    def openDbConn(self, host, db, user, password):
        try:
            connection = mysql.connector.connect(host=host,
                                                 database=db,
                                                 user=user,
                                                 password=password)
        except Error as e:
            return "Error while connecting to MySQL :: "+str(e)
        finally:
            pass
        return connection
