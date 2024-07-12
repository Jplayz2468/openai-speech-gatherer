print("installing dependencies...")
import os
import requests
from pydub import AudioSegment
import tarfile
import zipfile
print("ensuring ffmpeg")
# Ensure ffmpeg is installed and accessible
ffmpeg_executable = "ffmpeg"

# URLs of datasets (replace these with actual download links or paths)
datasets = {
    "LJ_Speech": "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2",
    "VCTK": "https://datashare.ed.ac.uk/download/DS_10283_3443.zip",
    "LibriTTS": "https://www.openslr.org/resources/60/train-clean-100.tar.gz"
    # Add more datasets as needed
}
print("making files")
output_dir = "normalized_audio"
transcripts_file = "merged_transcripts.txt"
os.makedirs(output_dir, exist_ok=True)

# Function to download and extract datasets
def download_and_extract(url, extract_to):
    print("downloading and extracting" + url)
    local_filename = url.split('/')[-1]
    local_filepath = os.path.join(extract_to, local_filename)

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
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
# Normalize audio function
def normalize_audio(input_path, output_path, target_loudness=-20.0):
    print("normalizing")
    audio = AudioSegment.from_file(input_path)
    change_in_dBFS = target_loudness - audio.dBFS
    normalized_audio = audio.apply_gain(change_in_dBFS)
    normalized_audio.export(output_path, format="wav")
print("processing")
# Process each dataset
for dataset_name, url in datasets.items():
    extract_path = os.path.join(output_dir, dataset_name)
    os.makedirs(extract_path, exist_ok=True)
    download_and_extract(url, extract_path)
    
    # Traverse the extracted files to find audio and transcripts
    for root, _, files in os.walk(extract_path):
        for file in files:
            if file.endswith(".wav") or file.endswith(".flac"):
                input_audio_path = os.path.join(root, file)
                output_audio_path = os.path.join(output_dir, f"{dataset_name}_{file}")
                
                # Convert and normalize audio
                normalize_audio(input_audio_path, output_audio_path)
                
            elif file.endswith(".txt") or file.endswith(".csv"):
                with open(os.path.join(root, file), 'r') as transcript_file:
                    with open(transcripts_file, 'a') as merged_file:
                        merged_file.write(transcript_file.read() + '\n')

print("Download and normalization complete.")
