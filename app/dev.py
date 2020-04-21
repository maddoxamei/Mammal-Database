from flask import Flask, render_template, url_for, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import traceback

app = Flask(__name__)

#/query, /update, /data HTTP update
ENDPOINT = 'http://localhost:3030/mammals'

sparql = SPARQLWrapper(ENDPOINT+"/query")
sparql.setReturnFormat(JSON)
query = "SELECT * {?subject ?predicate ?object}"
sparql.setQuery(""" +query+ """)

results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])
