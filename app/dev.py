import requests, rdflib, pprint
from flask import Flask, render_template, url_for, request, send_from_directory
from rdflib.namespace import FOAF, OWL, RDF, RDFS , XSD, XMLNS
from rdflib import BNode, Literal, Namespace

app = Flask(__name__)

#/query, /update, /data HTTP update

g = rdflib.Graph()
g.parse('static/Mammal.owl', format="application/rdf+xml")

rdf = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#")
owl = rdflib.URIRef("http://www.w3.org/2002/07/owl#")
xsd = rdflib.URIRef("http://www.w3.org/2001/XMLSchema#")
xml = rdflib.URIRef("http://www.w3.org/XML/1998/namespace#")
mammal = rdflib.URIRef("http://www.semanticweb.org/ontologies/2020/2/Mammal#")
g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('owl', OWL)
g.bind('xsd', XSD)
g.bind('xml', XMLNS)
g.bind('foaf', FOAF)
g.bind('m', mammal)
#print(g.serialize().decode("utf-8"))
print("Total Tripples:\t",len(g))


#@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    response = ""
    return render_template('layout.html', response=response)

@app.route("/query_page", methods=['POST'])
def query():
    query = request.form.get('search');
    response = list(g.query(query))
    return render_template('layout.html', response=response)

@app.route("/add_page", methods=['POST'])
def add():
    print (namespace.Development)
    #g.add((m.Development.test, rdfs.subClassOf, m.Development))
    query = "SELECT ?class	where { ?class rdfs:subClassOf m:Development }"
    #response = "After the ADDITION, there are {} triples in the graph".format(len(g))
    test = rdflib.URIRef(namespace.Development+"/test")
    response = namespace.Development.test
    return render_template('layout.html', response=response)

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

if __name__ == "__main__":
    app.run(debug=True) #have to ctrl+C to start the app
