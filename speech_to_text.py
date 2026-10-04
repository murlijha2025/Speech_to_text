"""Transcribe an audio file to text with IBM Watson Speech to Text.

Set your credentials as environment variables first:
    IBM_STT_APIKEY   your IBM Cloud API key
    IBM_STT_URL      your Speech to Text service URL

Usage:
    python speech_to_text.py speech.mp3
    python speech_to_text.py speech.wav -m en-AU_Multimedia -o transcript.txt
"""

import argparse
import os
import re
import sys
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1

DEFAULT_MODEL = "en-US_Multimedia"

CONTENT_TYPES = {
    ".mp3": "audio/mp3",
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".ogg": "audio/ogg",
    ".webm": "audio/webm",
}


def connect():
    """Create the Speech to Text client from environment variables."""
    apikey = os.environ.get("IBM_STT_APIKEY")
    url = os.environ.get("IBM_STT_URL")
    if not apikey or not url:
        sys.exit("Set IBM_STT_APIKEY and IBM_STT_URL environment variables first.")
    stt = SpeechToTextV1(authenticator=IAMAuthenticator(apikey))
    stt.set_service_url(url)
    return stt


def transcribe(stt, audio_path, model):
    """Send the audio file to Watson and return the list of result segments."""
    content_type = CONTENT_TYPES.get(audio_path.suffix.lower())
    if content_type is None:
        sys.exit(f"Unsupported file type. Use one of: {', '.join(CONTENT_TYPES)}")
    with open(audio_path, "rb") as f:
        response = stt.recognize(audio=f, content_type=content_type, model=model)
    return response.get_result()["results"]


def format_transcript(results):
    """Join all segments into readable sentences (the original only used the first one)."""
    sentences = []
    for result in results:
        segment = result["alternatives"][0]["transcript"].strip()
        if segment:
            sentences.append(segment[0].upper() + segment[1:] + ".")
    text = " ".join(sentences)
    return re.sub(r"\bi\b", "I", text)  # fixes "i" and "i'm" mid-sentence


def average_confidence(results):
    """Average confidence across segments that report one (None if none do)."""
    scores = [
        r["alternatives"][0]["confidence"]
        for r in results
        if "confidence" in r["alternatives"][0]
    ]
    return sum(scores) / len(scores) if scores else None


def parse_args():
    parser = argparse.ArgumentParser(description="Audio file to text with IBM Watson.")
    parser.add_argument("audio", type=Path, help="path to an audio file (mp3, wav, flac, ogg, webm)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"Watson model name (default: {DEFAULT_MODEL})")
    parser.add_argument("-o", "--output", type=Path, default=Path("output.txt"),
                        help="where to save the transcript (default: output.txt)")
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.audio.is_file():
        sys.exit(f"File not found: {args.audio}")

    results = transcribe(connect(), args.audio, args.model)
    if not results:
        sys.exit("No speech detected in the audio.")

    text = format_transcript(results)
    args.output.write_text(text, encoding="utf-8")

    print(text)
    confidence = average_confidence(results)
    if confidence is not None:
        print(f"\nAverage confidence: {confidence:.2f}")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
