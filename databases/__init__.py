from flask import Flask, Response
import databases.organism_source as organism_source
import databases.local_response as local_response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

@app.errorhandler(Exception)
def exception_handler(e):
	dext =  local_response.LocalResponse()
	if isinstance(e, HTTPException):
		return dext.buidJsonResponse(data=[],errno=500,error='HTTPException :: '+repr(e))
	
	return dext.buidJsonResponse(data=[],errno=500,error='Internal Server Error :: '+repr(e))

@app.errorhandler(404)
def pageNotFound(error):
	dext =  local_response.LocalResponse()
	return dext.buidJsonResponse(data=[],errno=404,error='404 :: Page not found')

@app.get("/databases")
def define_metadata_list():
	dext =  organism_source.OrganismSource()
	return dext.get_organism_metadata_sources_list()
