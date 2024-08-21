import os
from rdflib import Graph, URIRef, Literal, Namespace
import rdflib.namespace
from datetime import datetime
import matplotlib.pyplot as plt
from rdflib import BNode

# Namespaces
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCT = Namespace("http://purl.org/dc/terms/")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

def is_valid_date(date_str):
    
    try:
        datetime.fromisoformat(date_str.replace('Z', '+00:00')) 
        return True
    except ValueError:
        return False

def validate_rdf_file(file_path):
    
    g = Graph()
    try:
        g.parse(file_path, format='xml')
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return False, []

    invalid_elements = []

   
    for s, p, o in g.triples((None, DCAT.accessURL, None)):
        if not isinstance(o, URIRef):
            invalid_elements.append(f"dcat:accessURL: {o}")

   
    for s, p, o in g.triples((None, DCAT.contactPoint, None)):
        if not isinstance(o, URIRef) and not isinstance(o, BNode):
            invalid_elements.append(f"dcat:contactPoint: {o}")

   
    for s, p, o in g.triples((None, DCT.publisher, None)):
        if not isinstance(o, URIRef) and not isinstance(o, BNode):
            invalid_elements.append(f"dct:publisher: {o}")

  
    for s, p, o in g.triples((None, DCT.issued, None)):
        if isinstance(o, Literal) and o.datatype == rdflib.namespace.XSD.dateTime:
            if not is_valid_date(str(o)):
                invalid_elements.append(f"dct:issued: {o}")
        else:
            invalid_elements.append(f"dct:issued: {o}")

   
    for s, p, o in g.triples((None, DCT.modified, None)):
        if isinstance(o, Literal) and o.datatype == rdflib.namespace.XSD.dateTime:
            if not is_valid_date(str(o)):
                invalid_elements.append(f"dct:modified: {o}")
        else:
            invalid_elements.append(f"dct:modified: {o}")

    return len(invalid_elements) == 0, invalid_elements


def check_all_files_in_folder(folder_path):
    total_files = 0
    valid_files = 0
    invalid_files = []
    invalid_elements_details = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rdf"): 
                rdf_file_path = os.path.join(root, file)
                total_files += 1
                is_valid, invalid_elements = validate_rdf_file(rdf_file_path)
                if is_valid:
                    valid_files += 1
                else:
                    invalid_files.append(rdf_file_path)
                    invalid_elements_details[rdf_file_path] = invalid_elements

   
    labels = 'Valid RDF Files', 'Invalid RDF Files'
    sizes = [valid_files, total_files - valid_files]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Validation of RDF Files')
    plt.show()

   
    if invalid_files:
        print("Invalid RDF files:")
        for file_path in invalid_files:
            print(f"{file_path}:")
            for element in invalid_elements_details[file_path]:
                print(f"  - {element}")
    else:
        print("All RDF files are valid.")


folder_path = "C:\\Users\\farih\\metadata"

check_all_files_in_folder(folder_path)
