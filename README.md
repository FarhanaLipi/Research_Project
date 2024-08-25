# Metadata Quality Assessment in Open Data: Analyzing Chemnitz Datasets in GovData

This repository contains a collection of Python scripts developed to analyze and assess the quality of metadata related to Chemnitz datasets available on the GovData.de portal.
The scripts utilize the CKAN API to download and process metadata, enabling comprehensive quality assessments across multiple metrics.



## Project Structure

The repository is organized into the following scripts, each designed to assess different aspects of metadata quality:

- **file_download.py**: Downloads metadatasets from the GovData.de portal using the CKAN API, specifically targeting datasets related to Chemnitz.
- **Hasemail.py**: Assesses the presence of email addresses in metadata, which is crucial for certain metadata quality metrics.
- **accessibility.py**: Evaluates the accessibility of metadata, ensuring it meets required accessibility standards.
- **completeness.py**: Measures the completeness of metadata records, verifying that they contain all necessary fields.
- **conformance.py & conformance__1.py**: Assess the conformance of metadata to established standards, ensuring consistency and reliability.
- **IANA_registration.py**: Analyzing if the mediaTypes of datasets are registered by IANA or not
- **regional_dialects.py**: Assesses the presence of regional dialects or language variations within the metadata, which could impact the consistency and usability of the data.

## Installation

To run the scripts, ensure you have Python installed. Additionally, you may need the following libraries:

```bash
pip install matplotlib rdflib
