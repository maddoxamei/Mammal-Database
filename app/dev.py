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
#@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    return render_template('layout.html', response=response)

@app.route("/query_page", methods=['POST'])
def query():
    query = request.form.get('search');
    response.update(p=[],q=list(g.query(query)))
    return render_template('layout.html', response=response)

@app.route("/add_page", methods=['POST'])
def add():
    response.update(p = "Incorrect Input Method. A tripple consists of an :", q=[])

    sub = request.form.get('sub')
    pred = request.form.get('pred')
    obj = request.form.get('obj')

    subject = sub.split(':')
    predicate = pred.split(':')
    object = obj.split(':')

    if(len(subject)==2 and len(predicate)==2 and len(object)==2):
        subject = rdflib.URIRef(namespaces[subject[0]]+subject[1])
        predicate = rdflib.URIRef(namespaces[predicate[0]]+predicate[1])
        object = rdflib.URIRef(namespaces[object[0]]+object[1])
        g.add((subject, predicate, object))
        line = ["After the ADDITION, there are {} triples in the graph.".format(len(g)),
                " To view the recent addition use the following query:",
                "Select ?"+obj.split(':')[1]+" Where { ?"+obj.split(':')[1]+" "+pred+" "+obj+"}"]
        response.update(p=line, q=[])
    return render_template('layout.html', response=response)

@app.route("/remove_page", methods=['POST'])
def remove():
    response.update(p = "Incorrect Input Method. A tripple consists of an :", q=[])

    sub = request.form.get('sub')
    pred = request.form.get('pred')
    obj = request.form.get('obj')
    value = request.form.get('removal_type')

    subject = sub.split(':')
    predicate = pred.split(':')
    object = obj.split(':')

    if(len(subject)==2):
        subject = rdflib.URIRef(namespaces[subject[0]]+subject[1])
        if(predicate == [''] and object == ['']):
            if(value=='Purge'):
                response.update(p = ["Purging all..", "After the REMOVAL, there are {} triples in the graph.".format(len(g))], q=[])
                g.remove((subject, None, None))
            else:
                response.update(p = ["Careful! The purge option must be selected to purge"], q=[])
        else:
            if(value=='Single'):
                predicate = rdflib.URIRef(namespaces[predicate[0]]+predicate[1])
                object = rdflib.URIRef(namespaces[object[0]]+object[1])
                g.remove((subject, predicate, object))
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
