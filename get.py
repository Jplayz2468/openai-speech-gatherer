import os
import requests
import tarfile
import zipfile

print("Script started")

# URLs of datasets (replace these with actual download links or paths)
datasets = {
    "LJ_Speech": "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2",
    "VCTK": "https://datashare.ed.ac.uk/download/DS_10283_3443.zip",
    "LibriTTS": "https://www.openslr.org/resources/60/train-clean-100.tar.gz",
    # Add more datasets as needed
}

output_dir = "extracted_data"
os.makedirs(output_dir, exist_ok=True)

# Function to download and extract datasets
def download_and_extract(url, extract_to):
    print(f"Downloading {url}")
    local_filename = url.split('/')[-1]
    local_filepath = os.path.join(extract_to, local_filename)

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print(f"Extracting {local_filepath}")
    # Extract the file (assuming tar.gz, tar.bz2, or zip formats)
    if local_filename.endswith('.tar.gz'):
        with tarfile.open(local_filepath, 'r:gz') as tar:
            tar.extractall(path=extract_to)
    elif local_filename.endswith('.tar.bz2'):
        with tarfile.open(local_filepath, 'r:bz2') as tar:
            tar.extractall(path=extract_to)
    elif local_filename.endswith('.zip'):
        with zipfile.ZipFile(local_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    print(f"Finished extracting {local_filepath}")

# Process each dataset
for dataset_name, url in datasets.items():
    print(f"Processing dataset {dataset_name}")
    extract_path = os.path.join(output_dir, dataset_name)
    os.makedirs(extract_path, exist_ok=True)
    download_and_extract(url, extract_path)

print("Download and extraction complete.")
