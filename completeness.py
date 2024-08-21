import os
from rdflib import Graph, Namespace, RDF, Literal
from rdflib.namespace import DCTERMS
import matplotlib.pyplot as plt
import seaborn as sns


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


def extract_metadata_from_rdf_files(directory_path):
    metadata_list = []
    files_without_format = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".rdf"):
            file_path = os.path.join(directory_path, filename)
            try:
                metadata = extract_metadata_from_rdf(file_path)
                if not metadata['dct:format']:
                    files_without_format.append(filename)
                metadata_list.append(metadata)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    if files_without_format:
        print("RDF files without dct:format:")
        for filename in files_without_format:
            print(filename)
    return metadata_list


def extract_metadata_from_rdf(file_path):
    g = Graph()
    g.parse(file_path)
    
    metadata = {pred: False for pred in predicates.keys()}
    metadata['Keywords'] = []
    metadata['Distribution Formats'] = []

    for s, p, o in g:
        if p == DCTERMS.format and isinstance(o, Literal):
            format_name = str(o)
            metadata['Distribution Formats'].append(format_name)

    for pred_name, pred in predicates.items():
        if pred_name == "dcat:keyword":
            keyword_triples = g.triples((None, pred, None))
            for _, _, keyword in keyword_triples:
                metadata['Keywords'].append(str(keyword))
            metadata[pred_name] = len(metadata['Keywords']) > 0
        elif pred_name == "dcat:mediaType":
            distribution_triples = g.triples((None, pred, None))
            for _, _, format_value in distribution_triples:
                metadata['Distribution Formats'].append(str(format_value))
            metadata[pred_name] = len(metadata['Distribution Formats']) > 0
        elif pred_name == "dct:format":
            metadata[pred_name] = len(metadata['Distribution Formats']) > 0
        elif pred_name == "dcat:downloadURL":
            metadata[pred_name] = any(g.triples((None, pred, None)))
        else:
            metadata[pred_name] = any(g.triples((None, pred, None)))

    return metadata



predicates = {
    "dct:title": DCT.title,
    "dct:description": DCT.description,
    "dcat:keyword": DCAT.keyword,
    "dcat:accessURL": DCAT.accessURL,
    "dcat:contactPoint": DCAT.contactPoint,
    "dct:publisher": DCT.publisher,
    "dct:license": DCT.license,
    "dct:accrualPeriodicity": DCT.accrualPeriodicity,
    "dct:format": DCT.format,
    "dcat:mediaType": DCAT.mediaType,
    "dcat:byteSize": DCAT.byteSize,
    "dct:issued": DCT.issued,
    "dct:modified": DCT.modified,
    "dct:language": DCT.language,
    "dcat:theme": DCAT.theme,
    "dct:identifier": DCT.identifier,
    "dct:spatial": DCT.spatial,
    "dcat:downloadURL": DCAT.downloadURL
}


def calculate_mq_d_score(metadata_list):
    m_values = []
    for metadata in metadata_list:
        m_i = sum(metadata[attr] for attr in metadata if attr in predicates.keys() and metadata[attr])
        m_values.append(m_i)
    mq_d_score = sum(abs(m_i) for m_i in m_values) / len(m_values) if m_values else 0
    return mq_d_score


directory_path = r"C:\Users\farih\metadata"
metadata_list = extract_metadata_from_rdf_files(directory_path)


mq_d_score = calculate_mq_d_score(metadata_list)
print(f"MQ_D Score: {mq_d_score}")

def plot_metadata(metadata_list):
    total_datasets = len(metadata_list)
    
   
    attribute_counts = {
        'Title': sum(metadata['dct:title'] for metadata in metadata_list) / total_datasets,
        'Description': sum(metadata['dct:description'] for metadata in metadata_list) / total_datasets,
        'Keywords': sum(len(metadata['Keywords']) > 0 for metadata in metadata_list) / total_datasets,
        'Access URL': sum(metadata['dcat:accessURL'] for metadata in metadata_list) / total_datasets,
        'Contact Point': sum(metadata['dcat:contactPoint'] for metadata in metadata_list) / total_datasets,
        'Publisher': sum(metadata['dct:publisher'] for metadata in metadata_list) / total_datasets,
        'License': sum(metadata['dct:license'] for metadata in metadata_list) / total_datasets,
        'Accrual Periodicity': sum(metadata['dct:accrualPeriodicity'] for metadata in metadata_list) / total_datasets,
        'Format': sum(metadata['dct:format'] for metadata in metadata_list) / total_datasets,
        'Media Type': sum(len(metadata['Distribution Formats']) > 0 for metadata in metadata_list) / total_datasets,
        'Byte Size': sum(metadata['dcat:byteSize'] for metadata in metadata_list) / total_datasets,
        'Issued': sum(metadata['dct:issued'] for metadata in metadata_list) / total_datasets,
        'Modified': sum(metadata['dct:modified'] for metadata in metadata_list) / total_datasets,
        'Language': sum(metadata['dct:language'] for metadata in metadata_list) / total_datasets,
        'Theme': sum(metadata['dcat:theme'] for metadata in metadata_list) / total_datasets,
        'Identifier': sum(metadata['dct:identifier'] for metadata in metadata_list) / total_datasets,
        'Spatial': sum(metadata['dct:spatial'] for metadata in metadata_list) / total_datasets,
        'Download URL': sum(metadata['dcat:downloadURL'] for metadata in metadata_list) / total_datasets
    }

  
    plt.figure(figsize=(12, 7))
    sns.barplot(x=list(attribute_counts.keys()), y=list(attribute_counts.values()), palette="viridis")
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Attributes")
    plt.ylabel("Presence (0-1)")
    plt.title("Presence of Attributes in Datasets")
    plt.tight_layout()
    plt.show()


plot_metadata(metadata_list)


