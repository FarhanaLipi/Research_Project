import os
from rdflib import Graph
from textstat import flesch_reading_ease
from fpdf import FPDF

def calculate_links_count(g):
    links_count = {}
    for subj in set(g.subjects()):
        links_count[subj] = len(list(g.predicate_objects(subj)))
    return links_count

def calculate_flesch_scores(g):
    text_fields = [str(o) for s, p, o in g if p.endswith('description')]
    flesch_scores = [flesch_reading_ease(text) for text in text_fields]
    return flesch_scores

def calculate_access_url_count(g):
    access_urls = []
    for subj, pred, obj in g:
        if pred.endswith('accessURL'):
            title = next((o for s, p, o in g.triples((subj, 'http://purl.org/dc/terms/title', None))), None)
            keyword = next((o for s, p, o in g.triples((subj, 'http://purl.org/dc/terms/keyword', None))), None)
            description = next((o for s, p, o in g.triples((subj, 'http://purl.org/dc/terms/description', None))), None)
            access_urls.append((title, keyword, description))
    return access_urls

def main(folder_path):
    total_links = 0
    max_links = 0
    total_qread_score = 0
    rdf_files_count = 0

    qlinks = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".rdf"):
            file_path = os.path.join(folder_path, filename)
            g = Graph()
            g.parse(file_path)
            rdf_files_count += 1

           
            links_count = calculate_links_count(g)
            file_total_links = sum(links_count.values())
            file_max_links = max(links_count.values(), default=0)
            total_links += file_total_links
            max_links = max(max_links, file_max_links)

         
            access_url_info = calculate_access_url_count(g)
            for title, keyword, description in access_url_info:
                qlinks.append(f"{filename}: {title}, {keyword}, {description}")

           
            flesch_scores = calculate_flesch_scores(g)
            if flesch_scores:
                avg_flesch_score = sum(flesch_scores) / len(flesch_scores)
                total_qread_score += avg_flesch_score / 100

   
    avg_qlink_score = (total_links / rdf_files_count) / max_links if max_links > 0 else 0

    
    avg_qread_score = total_qread_score / rdf_files_count if rdf_files_count > 0 else 0

 
    combined_avg_score = (avg_qlink_score + avg_qread_score) / 2

   
    print(f"Average Qlink score: {avg_qlink_score}")
    print(f"Average Qread score: {avg_qread_score}")
    print(f"Combined average score: {combined_avg_score}")

  

if __name__ == "__main__":
    folder_path = r"C:\Users\farih\metadata" 
    main(folder_path)
