import os
import matplotlib.pyplot as plt
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import DCTERMS
import urllib.parse

def preprocess_media_type(media_type):
   
    if media_type.startswith("https://www.iana.org/assignments/media-types/"):
        
        return urllib.parse.unquote(media_type.split("/")[-1])
    return media_type

def check_all_files_in_folder(folder_path):
    media_type_counts = {}  

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rdf"):  
                rdf_file_path = os.path.join(root, file)
                g = Graph()
                try:
                    g.parse(rdf_file_path, format='xml')  
                except Exception as e:
                    print(f"Error parsing file {rdf_file_path}: {e}")
                    continue

                for s, p, o in g:
                    if p == Namespace("http://www.w3.org/ns/dcat#").mediaType:
                        if isinstance(o, Literal):
                            media_type = str(o)
                        else:
                            media_type = str(o)
                        media_type = preprocess_media_type(media_type)
                        media_type_counts[media_type] = media_type_counts.get(media_type, 0) + 1

   
    if media_type_counts:
        print("Media type counts:", media_type_counts)  
        plt.bar(media_type_counts.keys(), media_type_counts.values())
        plt.xlabel('Media Type')
        plt.ylabel('Count')
        plt.title('Media Types in RDF files')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("No media type information found in any RDF file.")


folder_path = "C:\\Users\\farih\\metadata"

check_all_files_in_folder(folder_path)
