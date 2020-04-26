import requests, rdflib, pprint
from flask import Flask, render_template, url_for, request, send_from_directory
from rdflib.namespace import FOAF, OWL, RDF, RDFS , XSD, XMLNS
from rdflib import BNode, Literal, Namespace

app = Flask(__name__)

#/query, /update, /data HTTP update

g = rdflib.Graph()
g.parse('static/Mammal.owl', format="application/rdf+xml")

namespaces = {
    "rdf":rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    "rdfs":rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#"),
    "owl":rdflib.URIRef("http://www.w3.org/2002/07/owl#"),
    "xsd":rdflib.URIRef("http://www.w3.org/2001/XMLSchema#"),
    "xml":rdflib.URIRef("http://www.w3.org/XML/1998/namespace#"),
    "m":rdflib.URIRef("http://www.semanticweb.org/ontologies/2020/2/Mammal#")
}

g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('owl', OWL)
g.bind('xsd', XSD)
g.bind('xml', XMLNS)
g.bind('foaf', FOAF)
g.bind('m', namespaces['m'])
#print(g.serialize().decode("utf-8"))
print("Total Tripples:\t",len(g))

response = {
    'p':[],
    'q':[]
}

def getArguments(sub, pred, obj):
    subject = sub.split(':')
    predicate = pred.split(':')
    object = obj.split(':')
    s = None
    p = None
    o = None
    if(len(subject)==2):
        s = rdflib.URIRef(namespaces[subject[0]]+subject[1])
    if(len(predicate)==2):
        p = rdflib.URIRef(namespaces[predicate[0]]+predicate[1])
    if(len(object)==2):
        o = rdflib.URIRef(namespaces[object[0]]+object[1])
    return s, p, o

@app.route("/")
def index():
    return render_template('layout.html', response=response)

@app.route("/query_page", methods=['POST'])
def query():
    value = request.form.get('query_type')
    print(value)
    s, p, o = getArguments(request.form.get('sub'), request.form.get('pred'), request.form.get('obj'))
    if(value==None):
        response.update(p=["Error. Please select a query method."],q=[])
    elif(value=='generator'):
        print(g.triples((s, p, o)))
        response.update(p=[],q=list(g.triples((s, p, o))))
    else:
        query = request.form.get('search');
        response.update(p=[],q=list(g.query(query)))
    #iter(graph)
    #graph.predicate_objects(subject)
    #graph.objects(subject, predicate)
    #graph.predicates(subject, object)
    #graph.subjects(predicate, object) #A generator of subjects with the given predicate and object
    return render_template('layout.html', response=response)

@app.route("/add_page", methods=['POST'])
def add():
    response.update(p = "Incorrect Input Method. A tripple consists of an :", q=[])
    s, p, o = getArguments(request.form.get('sub'), request.form.get('pred'), request.form.get('obj'))

    if(s!=None and p!=None and o!=None):
        g.add((s, p, o))
        line = ["After the ADDITION, there are {} triples in the graph.".format(len(g))]
        response.update(p=line, q=[])
    return render_template('layout.html', response=response)

@app.route("/remove_page", methods=['POST'])
def remove():
    response.update(p = "Incorrect Input Method. A tripple consists of an :", q=[])

    s, p, o = getArguments(request.form.get('sub'), request.form.get('pred'), request.form.get('obj'))
    value = request.form.get('removal_type')

    if(s!=None):
        if(p==None and o==None):
            if(value=='Purge'):
                response.update(p = ["Purging all..", "After the REMOVAL, there are {} triples in the graph.".format(len(g))], q=[])
                g.remove((s, p, o))
            else:
                response.update(p = ["Careful! The purge option must be selected to purge"], q=[])
        else:
            if(value=='Single'):
                g.remove((s, p, o))
                response.update(p = ["Removing: "+sub+" "+pred+" "+obj, "After the REMOVAL, there are {} triples in the graph.".format(len(g))], q=[])
            else:
                response.update(p = ["Careful! The single option must be selected to remove a specific tripple"], q=[])
    return render_template('layout.html', response=response)

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

if __name__ == "__main__":
    app.run(debug=True) #have to ctrl+C to start the app
