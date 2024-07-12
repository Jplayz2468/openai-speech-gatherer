import os
from pydub import AudioSegment

def get_audio_duration(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000  # duration in seconds
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def total_audio_duration_in_hours(root_dir):
    total_duration = 0
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            duration = get_audio_duration(file_path)
            total_duration += duration
            if duration > 0:
                print(f"Processed {file_path}: {duration/60:.2f} minutes")
    return total_duration / 3600  # Convert seconds to hours

if __name__ == "__main__":
    root_directory = "."  # Current directory or specify your path
    print(f"Scanning directory: {root_directory}")
    total_hours = total_audio_duration_in_hours(root_directory)
    print(f"Total audio duration in hours: {total_hours:.2f}")