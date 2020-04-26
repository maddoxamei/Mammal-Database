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
answer = queryex();
