# YouTube Tabs Manager

A simple manager for extracting tabs from a YouTube guitar tab video, with transcription if necessary.

## Features

- Trained YOLO model to detect guitar tabs in video frames (to be implemented)
- Save the extracted guitar tab as a .pdf file (to be implemented)
- Transcription feature to move notes as necessary (to be implemented)

## Installation

```bash
git clone https://github.com/jmoon98/TabsManager.git
cd TabsManager
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt