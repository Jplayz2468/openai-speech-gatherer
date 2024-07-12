import openai
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_paragraph(subject):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"Please generate a paragraph about {subject} for training data."}
        ]
    )
    paragraph = response.choices[0].message.content
    return paragraph

def text_to_speech(text, filename):
    client = openai.OpenAI()
    speech_file_path = Path(filename)
    response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=text
    )
    response.stream_to_file(speech_file_path)

def update_json(paragraph, filename, json_file):
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    formatted_paragraph = paragraph.replace("\n", " ").replace("{", "").replace("}", "")
    data[filename] = {"training_paragraph": formatted_paragraph}

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    categories = []
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    json_file = output_dir / 'training_data.json'

    for subject in categories:
        files_count = len(list(output_dir.glob('paragraph_audio_*.mp3')))
        audio_filename = output_dir / f'paragraph_audio_{files_count + 1}.mp3'

        paragraph = generate_paragraph(subject)
        text_to_speech(paragraph, audio_filename)
        update_json(paragraph, str(audio_filename), json_file)
        print(f"Generated paragraph: {paragraph}")
        print(f"Audio saved as: {audio_filename}")
        print(f"JSON updated: {json_file}")

if __name__ == '__main__':
    main()