from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from transformers import pipeline
import re

def get_video_id(url):
    parsed_url = urlparse(url)
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip('/')
    query = parse_qs(parsed_url.query)
    return query.get("v", [None])[0]

def get_transcript(video_url):
    video_id = get_video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([entry['text'] for entry in transcript])
    return text

def split_text(text, max_words=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks

def summarize_chunks(chunks):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return "\n".join(summaries)

def summarize_youtube_video(url):
    transcript = get_transcript(url)
    chunks = split_text(transcript)
    summary = summarize_chunks(chunks)
    return summary

def save_summary_to_file(summary, filename="video_summary.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"\nSummary saved to {filename}")

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    print("\nGenerating Summary...\n")
    try:
        summary = summarize_youtube_video(url)
        save_summary_to_file(summary)
    except Exception as e:
        print(f"Error: {e}")
