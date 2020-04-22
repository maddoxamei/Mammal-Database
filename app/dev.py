import os
from flask import Flask, render_template, url_for, request
from SPARQLWrapper import SPARQLWrapper, JSON
#import requests
#import traceback

app = Flask(__name__)

ENDPOINT = 'http://localhost:3030/mammals'
#server = init()
#/query, /update, /data HTTP update
def init():
    os.system('/static/apache-jena-fuseki-3.14.0/fuseki-server')
    sparql = SPARQLWrapper(ENDPOINT+"/query")
    sparql.setReturnFormat(JSON)
    return sparql

prefix = """ prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix m: <http://www.semanticweb.org/ontologies/2020/2/Mammal#> """
def query(str):
    query = "SELECT ?class	where { ?class rdfs:subClassOf m:Development }"
    sparql.setQuery(" "" "+prefix+query+" "" ")
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print(result)
        #print(result["label"]["value"])
    return results

@app.route("/")
@app.route("/home")
def home():
	return render_template('layout.html')

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

if __name__ == "__main__":
    app.run(debug=True)
