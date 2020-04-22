import os, subprocess, threading
from flask import Flask, render_template, url_for, request, send_from_directory
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
#import traceback

app = Flask(__name__)

ENDPOINT = 'http://localhost:3030/mammals'

#/query, /update, /data HTTP update
def init():
    subprocess.call("run.bat")

    data = open('static/Mammal.owl').read()
    headers = {'Content-Type': 'application/rdf+xml;charset=utf-8'}
    r = requests.post('http://localhost:3030/mammals/data?default', data=data, headers=headers)
    sparql = SPARQLWrapper(ENDPOINT+"/query")
    sparql.setReturnFormat(JSON)
    global server
    server = sparql
    queryex();



prefix = """ prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix m: <http://www.semanticweb.org/ontologies/2020/2/Mammal#> """
def queryex():
    query = "SELECT DISTINCT ?class ?label ?description WHERE { ?class a owl:Class. OPTIONAL { ?class rdfs:label ?label} OPTIONAL { ?class rdfs:comment ?description}}"
    server.setQuery(" "" "+prefix+query+" "" ")
    results = server.query().convert()
    for result in results["results"]["bindings"]:
        print(result)
        #print(result["class"]["value"])
        #print(result["label"]["value"])
    return results

#@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/")
@app.route("/home")
def home():
	return render_template('layout.html')

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

if __name__ == "__main__":
    threading.Thread(target=init).start()
    app.run(debug=True) #have to ctrl+C to start the app
