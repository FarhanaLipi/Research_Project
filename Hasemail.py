import os
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace

def check_all_files_in_folder(folder_path):
    has_email_counts = 0
    has_email_files = []  

    
    VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")

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

                found_has_email = False

                for s, p, o in g:
                  
                    if p == VCARD.hasEmail:
                        found_has_email = True
                        break

                if found_has_email:
                    has_email_counts += 1
                    has_email_files.append(rdf_file_path)

   
    labels = ['Has Email', 'No Email']
    sizes = [has_email_counts, len(files) - has_email_counts]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Presence of hasEmail Attribute')
    plt.show()


folder_path = "C:\\Users\\farih\\metadata"

check_all_files_in_folder(folder_path)
