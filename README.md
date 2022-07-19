# ensembl-metadata-microservice
Microservice to extract metadata defined by organism attributes. Realised with Python usage based on the Flask.

Should be prepared before runing.

1. python 3.7 should be installed 
   or switched from other version by applying ::
   
   $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.x 1
   
   $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
   
   $ sudo update-alternatives --config python3
   
   - choose 2

2. venv should be installed by applying ::

   $ sudo apt-get install python3.7-venv

3. pip should be installed by applying ::

   $ sudo apt install python3-pip

4. project code should be cloned from git storage by applying ::

   $ sudo mkdir ensembl_git
   
   $ cd ensembl_git
   
   $ git clone https://github.com/v-v-svystunov/ensembl-metadata-microservice.git 
   
To run application.

1. $mkdir ensembl

   $cd ensembl

2. $python3 -m venv e_venv

3. $source e_venv/bin/activate

4. $pip install Flask

5. $pip3 install mysql-connector-python

   $pip install requests

6. $ cd ensembl_git

   $cp config.py run.py test.py MainLib.py OrganismLib.py ensembl/

7. edit config.py - substitute return of get_db_host() and get_db_user() by real credentials

8. $export FLASK_APP=run

   $flask run

9. Examples to run in browser:
    
  http://localhost:5000/databases?name=homo_sapiens 
  
  http://localhost:5000/databases?release=100&name=homo_sapiens
  
  http://localhost:5000/databases?name=homo_sapiens&release=100&type=cdna
  
	http://localhost:5000/databases?release=100&type=cdna

To apply tests.	 

1. With activated Serving Flask app 'run' (lazy loading) by point (8) of the previous story
   do ::
   
   $source e_venv/bin/activate
   
   $export FLASK_APP=test
   
   $flask run --port 5001

2. To observe full list of available tests ::

   http://localhost:5001/test/list

3. Run over particular links from the opened list, step by step and observe the result.

4. Available tests:

   http://localhost:5001/test/http_post # Control HTTP method POST calls 
   
   http://localhost:5001/test/http_put # Control HTTP method PUT calls 
   
   http://localhost:5001/test/http_patch # Control HTTP method PATCH calls 
   
   http://localhost:5001/test/http_404 # Control Nonexistent organism return code 404
   
   http://localhost:5001/test/no_parameter # No parameter set
   
   http://localhost:5001/test/name_length # Name parameter is less than 3 chars
   
   http://localhost:5001/test/wrong_release # Release parameter is not an integer
   

