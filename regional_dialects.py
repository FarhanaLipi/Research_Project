import os
import re
from rdflib import Graph

regional_terms = {
    'population_and_society': [
        'Leit', 'Flegel', 'Hemed', 'Pänz', 'Buam', 'Gaffee', 'Mädle', 'Knoll', 
        'Buach', 'Schlaumei', 'Heftle', 'Stift', 'Dult', 'Kehrwoche', 'Gugelhupf', 
        'Alaaf', 'Kopfweh', 'Schunkeln', 'Gosch', 'Schnüss', 'Haxn', 'Bolzen', 
        'Renne', 'Kicke', 'Schandarm', 'Büttel', 'Schdraf', 'Schmöker', 'Sanitäter', 
        'Wache', 'Blauchlicht', 'Brandwehr', 'Brotzeit', 'Mischgemüse', 'Kutteln', 
        'Pittermännchen', 'Bezirksamt', 'Ratshaus', 'Stadtkämmerer', 'Obrigkeit', 
        'Oberbayern', 'Lausitz', 'Alb', 'Eifel', 'Alm', 'Busch', 'Gärtle', 'Jebirsch', 
        'Roß', 'Schwebebahn', 'Mopedle', 'Karren', 'Zaster', 'Mark', 'Kies', 'Penunze', 
        'Erfindergeist', 'Tüftler', 'Schaffer', 'Draumsaach'
    ],
    'education': [
        'Schui', 'Kinnergarten', 'Büchle', 'Penn', 'Pauker', 'Schule', 'Blattla', 
        'Heft', 'Schüler', 'Studente', 'Lerner', 'Schular'
    ],
    'culture': [
        'Tracht', 'Räuchermann', 'Fasnet', 'Bützje', 'Biergarten', 'Stollen', 
        'Häusle', 'Kölsch', 'Schuhplattler', 'Bratwurst', 'Vesper', 'Karneval'
    ],
    'health': [
        'Schnupfa', 'Huste', 'G’sund', 'Plärren', 'Arzt', 'Salbe', 'Kittel', 
        'Pillen', 'Fieber', 'Schmerz', 'Lunge', 'Gripp'
    ],
    'sport': [
        'Wiesn', 'Fußballen', 'Sporte', 'Jöle'
    ],
    'justice_and_legal_system': [
        'Gericht', 'Räscht', 'Anwalt', 'Kruscht', 'Gefängnis', 'Urteil', 
        'Verhör', 'Schrievkrom'
    ],
    'public_safety': [
        'Feuerwehr', 'Pohlizei', 'Schdroo', 'Foyerwehr', 'Unfall', 'Rettung', 
        'Notruf', 'Blaulicht'
    ],
    'agriculture': [
        'Hoamat', 'Gaard', 'Hof', 'Äädappel', 'Kuh', 'Ernte', 'Wiese', 'Wald', 
        'Bienen', 'Obst', 'Holz', 'Jäger'
    ],
    'fisheries': [],
    'forestry': [],
    'food': [
        'Brot', 'Wurst', 'Käse', 'Futter', 'Bier', 'Wein', 'Schnaps', 'Brauerei'
    ],
    'government_and_public_sector': [
        'Rathaus', 'Amt', 'Gemeinda', 'Bürjeramt', 'Dahoam', 'Drägschn', 
        'Stuggitown', 'Kölle'
    ],
    'regions_and_cities': [
        'Woid', 'Flääz', 'Bächle', 'Rhing', 'Bim', 'Gleis', 'Schdross', 
        'Schloofbaan'
    ],
    'environment': [
        'Berg', 'Tal', 'See', 'Weid', 'Gipfel', 'Bach', 'Tal', 'Wald'
    ],
    'traffic': [
        'G’schwindigkeit', 'Bimml', 'Steuer', 'Jleis', 'Stau', 'Ampel', 
        'Gleise', 'Auto'
    ],
    'economy_and_finance': [
        'Gwinn', 'Scharm', 'Schbloos', 'Taler', 'Zins', 'Geld', 'Späne', 
        'Batzen', 'Kredit', 'Bank', 'Konto', 'Tresor'
    ],
    'science_and_technology': [
        'Draumsaach', 'Maschin', 'Gerätschaft', 'Hantwärek', 'Erfindung', 
        'Tüftler', 'Macher', 'Tüftelei', 'Wissenschaft', 'Forschung', 
        'Entwicklung', 'Wessenschafft', 'Idee', 'Plan', 'Projäkt', 'Konzept'
    ]

}

def has_regional_term(text):
    for term_list in regional_terms.values():
        for term in term_list:
            if term.lower() in text.lower():
                return True
    return False

def analyze_rdf_files(folder_path):
    regional_terms_found = False
    for filename in os.listdir(folder_path):
        if filename.endswith('.rdf'):
            file_path = os.path.join(folder_path, filename)
            g = Graph()
            g.parse(file_path, format='xml')

            keyword_pattern = re.compile(r'<dcat:keyword>(.*?)</dcat:keyword>', re.DOTALL)
            for keyword in g.objects():
                keyword_match = keyword_pattern.findall(str(keyword))
                if keyword_match:
                    for kw in keyword_match:
                        if has_regional_term(kw):
                            print(f"Regional term '{kw}' found in file: {file_path}")
                            regional_terms_found = True
    if not regional_terms_found:
        print("No regional terms found in any RDF file.")


folder_path = r"C:\Users\farih\metadata"
analyze_rdf_files(folder_path)
