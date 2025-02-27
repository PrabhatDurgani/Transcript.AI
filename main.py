import os
import time
import json
import whisper
import ffmpeg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to monitor
TARGET_DIRECTORY = "./media"

# Supported file formats
SUPPORTED_FORMATS = {".mp3", ".wav", ".mp4", ".mkv", ".mov", ".flv", ".aac", ".m4a"}

# JSON file to track processed files
PROCESSED_FILES_DB = "processed_files.json"

# Load previously processed files
if os.path.exists(PROCESSED_FILES_DB):
    with open(PROCESSED_FILES_DB, "r") as f:
        processed_files = json.load(f)
else:
    processed_files = {}

def save_processed_files():
    """Saves the list of processed files to prevent redundant transcriptions."""
    with open(PROCESSED_FILES_DB, "w") as f:
        json.dump(processed_files, f, indent=4)

def transcribe_audio(file_path):
    """Uses Whisper model to transcribe audio and save the text output."""
    if file_path in processed_files:
        print(f"Skipping {file_path}, already processed.")
        return

    print(f"Processing: {file_path}")
    model = whisper.load_model("small")  # Load a lightweight Whisper model
    result = model.transcribe(file_path)
    
    transcript_path = file_path.rsplit(".", 1)[0] + ".txt"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"Transcription saved at: {transcript_path}")

    # Mark file as processed
    processed_files[file_path] = True
    save_processed_files()

def process_file(file_path):
    """Converts video to audio if needed and transcribes the file."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in SUPPORTED_FORMATS:
        if file_path in processed_files:
            print(f"Skipping {file_path}, already processed.")
            return
        
        if ext in {".mp4", ".mkv", ".mov", ".flv"}:  # Convert video to audio
            audio_path = file_path.rsplit(".", 1)[0] + ".wav"
            
            if not os.path.exists(audio_path):  # Avoid redundant conversion
                print(f"Extracting audio from: {file_path}")
                try:
                    ffmpeg.input(file_path).output(audio_path, format="wav", acodec="pcm_s16le").run(overwrite_output=True, quiet=True)
                except Exception as e:
                    print(f"Error converting {file_path}: {e}")
                    return

            transcribe_audio(audio_path)
        else:
            transcribe_audio(file_path)

def scan_directory(directory):
    """Scans the specified directory for media files and processes them."""
    print(f"Scanning directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

class FileHandler(FileSystemEventHandler):
    """Handles newly added files by triggering transcription automatically."""
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            process_file(event.src_path)

if __name__ == "__main__":
    print("Starting initial directory scan...")
    scan_directory(TARGET_DIRECTORY)
    
    print("Monitoring for new files...")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_DIRECTORY, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitoring...")
        observer.stop()
    observer.join()
