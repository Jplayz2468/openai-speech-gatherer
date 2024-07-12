import os
from mutagen import File

def get_audio_duration(file_path):
    audio = File(file_path)
    if audio is not None and audio.info is not None:
        return audio.info.length
    return 0

def total_audio_duration_in_hours(root_dir):
    total_duration = 0
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            total_duration += get_audio_duration(file_path)
    return total_duration / 3600  # Convert seconds to hours

if __name__ == "__main__":
    root_directory = "/path/to/your/directory"
    total_hours = total_audio_duration_in_hours(root_directory)
    print(f"Total audio duration in hours: {total_hours:.2f}")