from flask import Flask, render_template, url_for, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
#import requests
#import traceback

app = Flask(__name__)

#/query, /update, /data HTTP update
ENDPOINT = 'http://localhost:3030/mammals'

sparql = SPARQLWrapper(ENDPOINT+"/query")
sparql.setReturnFormat(JSON)
prefix = """ prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix m: <http://www.semanticweb.org/ontologies/2020/2/Mammal#> """
query = "SELECT ?class	where { ?class rdfs:subClassOf m:Development }"
sparql.setQuery(" "" "+prefix+query+" "" ")

results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result)
    #print(result["label"]["value"])

if __name__ == "__main__":
    app.run(debug=True)
