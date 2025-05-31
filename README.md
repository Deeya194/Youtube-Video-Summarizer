# YouTube Video Summarizer 🎥📝

This project is a Python tool that summarizes YouTube videos by extracting the transcript and generating a concise summary using NLP.

## 🚀 Features
- Extracts video transcript using `youtube-transcript-api`
- Summarizes using HuggingFace's `DistilBART` model
- Saves the summary to a `.txt` file

## 📦 Requirements
- Python 3.x
- transformers
- youtube-transcript-api

Install dependencies:
```bash
pip install -r requirements.txt
