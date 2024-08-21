import os
import matplotlib.pyplot as plt
from rdflib import Graph, Literal, Namespace
import urllib.parse

def preprocess_media_type(media_type):
    """
    Preprocesses the media type string to ensure uniformity.
    """
    if media_type.startswith("https://www.iana.org/assignments/media-types/"):
        # Extract the media type part from the URI
        return urllib.parse.unquote(media_type.split("/")[-1])
    return media_type

def is_machine_readable(media_type):
    """
    Checks if the media type is machine-readable.
    """
   
    if "+xml" in media_type or "+json" in media_type:
        return True
    
    structured_media_types = [
       'csv', 'text/csv','text/csv+extended', 'application/csv', 'application/json','application/xml','html','text/html',
        'text/xml', 'application/rdf+xml', 'application/ld+json', 'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ogc.wms_xml',
        'application/x-netcdf', 'application/x-hdf', 'application/x-hdf5',
        'application/vnd.google-earth.kml+xml', 'application/vnd.geo+json','AGIS_GEODATA'
    ]
    if media_type.lower() in structured_media_types:
        return True
    return False

def check_all_files_in_folder(folder_path):
    machine_readable_counts = 0
    non_machine_readable_counts = 0
    non_machine_readable_files = [] 

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

                has_machine_readable_distribution = False  
                for s, p, o in g:
                    if p == Namespace("http://www.w3.org/ns/dcat#").mediaType:
                        if isinstance(o, Literal):
                            media_type = str(o)
                        else:
                            media_type = str(o)
                        media_type = preprocess_media_type(media_type)
                        if is_machine_readable(media_type):
                            has_machine_readable_distribution = True
                            break 
                    elif p == Namespace("http://purl.org/dc/terms/").format:
                        file_format = str(o)
                        if is_machine_readable(file_format):
                            has_machine_readable_distribution = True
                            break  

               
                if not has_machine_readable_distribution:
                    for s, p, o in g.triples((None, Namespace("http://purl.org/dc/terms/").format, None)):
                        file_format = str(o)
                        if is_machine_readable(file_format):
                            has_machine_readable_distribution = True
                            break

                if has_machine_readable_distribution:
                    machine_readable_counts += 1
                else:
                    non_machine_readable_counts += 1
                    non_machine_readable_files.append(rdf_file_path)  # Add non-machine-readable file to the list

    
    labels = 'Machine Readable', 'Non-Machine Readable'
    sizes = [machine_readable_counts, non_machine_readable_counts]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Distribution of Machine-Readable and Non-Machine-Readable Formats')
    plt.show()

    
    print("Non-machine-readable files:")
    for file_path in non_machine_readable_files:
        print(file_path)


folder_path = "C:\\Users\\farih\\metadata"

check_all_files_in_folder(folder_path)
