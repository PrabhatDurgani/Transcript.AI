# Automated Transcription System using Whisper

## About the Project
This project is an **automated transcription system** that utilizes OpenAI’s **Whisper model** to transcribe speech from **audio and video files**. The system continuously **monitors a directory** for newly added media files, automatically **processes them**, and saves the **transcription as a text file**.

## Features
- **Recursive File Scanning**: Automatically scans a directory and subdirectories for media files.
- **Audio Extraction**: Converts video files to audio using **FFmpeg**.
- **Automated Transcription**: Uses **Whisper** to generate accurate transcriptions.
- **Real-Time Monitoring**: Detects and transcribes new files without manual intervention.
- **Session Management**: Prevents reprocessing of already transcribed files and resumes after interruptions.

## Prerequisites
Ensure you have the following installed before running the script:

### 1. Install Python (Recommended: Python 3.8+)
Download and install Python from [python.org](https://www.python.org/downloads/).

### 2. Install FFmpeg
FFmpeg is required for extracting audio from video files.
- **Windows**: Install FFmpeg using Chocolatey:
  ```sh
  choco install ffmpeg
  ```
- **Mac (Homebrew)**:
  ```sh
  brew install ffmpeg
  ```
- **Linux (APT-based)**:
  ```sh
  sudo apt update && sudo apt install ffmpeg
  ```


## Required Python Modules
Install the following dependencies using **pip**:
```sh
pip install openai-whisper ffmpeg-python watchdog
```

## How to Run the Script
Run the script by specifying the target folder where your media files will be stored.

```sh
python main.py
```
By default, it will monitor the `media/` folder. Place your audio or video files inside this folder, and the system will **automatically transcribe them**.

## How It Works
1. The script scans the specified directory for **supported media files** (MP3, WAV, MP4, MKV, MOV, FLV, AAC, M4A).
2. If a **video file** is found, it **extracts audio** using FFmpeg.
3. The extracted audio is **transcribed** using **OpenAI’s Whisper model**.
4. The generated **transcript is saved** in the same directory as a `.txt` file.
5. The system continuously **monitors** the folder and **automatically processes new files**.
6. Already processed files are skipped to avoid redundant transcriptions.

## Example Usage
After running `python main.py`, just **add an audio or video file** to the monitored folder, and within seconds, the **transcription will be generated** in the same directory.

## Stopping the Script
To stop the monitoring process, use **CTRL + C** in the terminal.

---

### Future Enhancements
- **Web UI for uploading and managing transcriptions**
- **Multi-language support using Whisper’s advanced models**
- **Cloud-based storage integration (AWS/GCP/Azure)**

---

### Author
Developed by **[Your Name]**. Feel free to contribute and improve the project!

