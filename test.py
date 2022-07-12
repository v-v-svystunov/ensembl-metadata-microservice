from flask import Flask, request, Response, jsonify, make_response, Markup
import requests
from pprint import pprint

app = Flask(__name__)

# an interface processor for HTTP GET request -- test POST HTTP
#
@app.route("/test/list", methods=['GET'])
def get_test_list():
    
    message = "Use <b>/test/http_post</b> to taest an interface processor for HTTP GET request -- test POST HTTP<br>"
    
    message = message+"Use <b>/test/http_put</b> to taest an interface processor for HTTP GET request -- test PUT HTTP<br>"

    message = message+"Use <b>/test/http_patch</b> to taest an interface processor for HTTP GET request -- test PATCH HTTP<br>"

    message = message+"Use <b>/test/http_404</b> to taest an interface processor for HTTP GET request -- test Case for unavailable organism with 404 code as response<br>"

    message = message+"Use <b>/test/no_parameter</b> to taest an interface processor for HTTP GET request -- test Case for empty parameters in set with 400 code as response<br>"

    message = message+"Use <b>/test/name_length</b> to taest an interface processor for HTTP GET request -- test Case for short organism name in row with 400 code as response<br>"

    message = message+"Use <b>/test/wrong_release</b> to taest an interface processor for HTTP GET request -- test Case for release as not int in row with 400 code as response<br>"

    return Response(message,status=200)

# an interface processor for HTTP GET request -- test POST HTTP
#
@app.route("/test/http_post", methods=['GET'])
def check_http_post():
    dictToSend = {'question':'what is the answer?'}
    res = requests.post('http://localhost:5000/databases', json=dictToSend)
    
    #dictFromServer = res.json()

    response = vars(res)
    pprint(response)

    message = "For <b>POST</b> HTTP request to the <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"

    #message = message+str(response)
    message = message+"</font></pre>"

    return Response(message,status=200)


# an interface processor for HTTP GET request -- test PUT HTTP
#
@app.route("/test/http_put", methods=['GET'])
def check_http_put():
    dictToSend = {'question':'what is the answer?'}
    res = requests.put('http://localhost:5000/databases', json=dictToSend)
    
    #dictFromServer = res.json()

    response = vars(res)
    pprint(response)

    message = "For <b>PUT</b> HTTP request to the <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"
        
    #message = message+str(response)
    message = message+"</font></pre>"

    return Response(message,status=200)


# an interface processor for HTTP GET request -- test PATCH HTTP
#
@app.route("/test/http_patch", methods=['GET'])
def check_http_patch():
    dictToSend = {'question':'what is the answer?'}
    res = requests.patch('http://localhost:5000/databases', json=dictToSend)
    
    #dictFromServer = res.json()

    response = vars(res)
    pprint(response)

    message = "For <b>PATCH</b> HTTP request to the <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"
        
    #message = message+str(response)
    message = message+"</font></pre>"

    return Response(message,status=200)

# an interface processor for HTTP GET request -- test Case for unavailable organism with 404 code as response
#
@app.route("/test/http_404", methods=['GET'])
def check_http_404():
    res =  requests.get('http://localhost:5000/databases?name=UNREGISTERED_ORGANISM_NAME')
    response = vars(res)
    pprint(response)

    message = "For attempt to search by unregistered organism name <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"
    
    message = message+"</font></pre>"

    return Response(message,status=200)


# an interface processor for HTTP GET request -- test Case for empty parameters in set with 400 code as response
#
@app.route("/test/no_parameter", methods=['GET'])
def check_http_400_empty_params():
    res =  requests.get('http://localhost:5000/databases')
    response = vars(res)
    pprint(response)

    message = "For attempt to search by unregistered organism name <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"
    
    message = message+"</font></pre>"

    return Response(message,status=200)

# an interface processor for HTTP GET request -- test Case for short organism name in row with 400 code as response
#
@app.route("/test/name_length", methods=['GET'])
def check_http_400_bad_organism_name():
    res =  requests.get('http://localhost:5000/databases?name=bd')
    response = vars(res)
    pprint(response)

    message = "For attempt to search by unregistered organism name <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"
    
    message = message+"</font></pre>"

    return Response(message,status=200)

# an interface processor for HTTP GET request -- test Case for release as not int in row with 400 code as response
#
@app.route("/test/wrong_release", methods=['GET'])
def check_http_400_bad_release():
    res =  requests.get('http://localhost:5000/databases?release=100o')
    response = vars(res)
    pprint(response)

    message = "For attempt to search by unregistered organism name <b>"+res.url+"</b><br>Received response:: <b>"+res.text+"</b><br>With code:: <b>"+str(res.status_code)+"</b><br><b>Full response::</b><br><pre><font color='red'>"
    for k, v in response.items():
        message = message+str(k)+" => "+str(Markup.escape(v))+"<br>"
    
    message = message+"</font></pre>"

    return Response(message,status=200)