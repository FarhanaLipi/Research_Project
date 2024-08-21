import requests
import os
import re

def clean_filename(filename):
    cleaned_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return cleaned_filename

api_endpoint = "https://www.govdata.de/ckan/api/3/action/package_search"

keyword = "Chemnitz"

params = {
    "q": keyword,
    "start": 0, 
   
    
}

response = requests.get(api_endpoint, params=params)

if response.status_code == 200:
    os.makedirs("metadata", exist_ok=True)
    
    data = response.json()["result"]["results"]
    
    for result in data:
        dataset_title = result["title"]
        metadata_url = f"https://www.govdata.de/ckan/dataset/{result['name']}.rdf"
        
        metadata_response = requests.get(metadata_url)
        
        if metadata_response.status_code == 200:
            cleaned_title = clean_filename(dataset_title)
            
            with open(f"metadata/{cleaned_title}.rdf", "wb") as f:
                f.write(metadata_response.content)
            print(f"Metadata downloaded for dataset: {dataset_title}")
        else:
            print(f"Error downloading metadata for dataset: {dataset_title}")
else:
    print("Error:", response.status_code)
