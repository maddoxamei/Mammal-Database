from flask import Flask, render_template
from rdflib import Graph
from rdflib.namespace import FOAF

app = Flask(__name__)
foaf = Graph()
#foaf.parse("flask_foaf/static/Mammal.owl")


def get_me():
    res = foaf.query("""SELECT DISTINCT ?fname
                     WHERE {
                     ?me a foaf:Person .
                     ?me foaf:givenname ?fname .
                     }
                     """, initNs={"foaf": FOAF})
    return list(res)[0]

from flask import Flask, render_template, Response, request, redirect, url_for
app = Flask(__name__)

'''
@app.route("/")
def index():
    return render_template('index.html')
'''

@app.route("/")
def index():
    #Moving forward code
    forward_message = ""
    return render_template('index.html', forward_message=forward_message);

@app.route("/home", methods=['POST'])
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('index.html', forward_message=forward_message);

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


if __name__ == "__main__":
    app.run(debug=True)
