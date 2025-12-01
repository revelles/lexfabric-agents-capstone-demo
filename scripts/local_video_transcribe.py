#!/usr/bin/env python
"""
Transcribe a local video file and produce:
  - transcript.txt
  - transcript.srt

Dependencies:
    pip install openai-whisper
    ffmpeg must be installed (e.g., brew install ffmpeg)

Usage:
    python local_video_transcribe.py --input /path/to/video.mp4 --out-dir transcripts
"""

import argparse
import subprocess
from pathlib import Path
import whisper


def extract_audio(input_file: Path, output_audio: Path):
    """
    Extract audio track from video using ffmpeg.
    Output is mono 16kHz WAV for Whisper.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_file),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(output_audio),
    ]
    subprocess.run(cmd, check=True)


def srt_timestamp(seconds: float) -> str:
    """
    Convert seconds → SRT timestamp: HH:MM:SS,mmm
    """
    millis = int(seconds * 1000)
    hrs = millis // 3_600_000
    millis %= 3_600_000
    mins = millis // 60_000
    millis %= 60_000
    secs = millis // 1000
    millis %= 1000
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def write_srt(segments, output_path: Path):
    """
    Write Whisper segments → .srt
    """
    with output_path.open("w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = srt_timestamp(seg["start"])
            end = srt_timestamp(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe a local video file into text and SRT subtitles."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to local video file (.mp4, .mov, etc.)",
    )
    parser.add_argument(
        "--out-dir",
        default="transcripts",
        help="Output folder (will be created if it does not exist).",
    )
    parser.add_argument(
        "--model-size",
        default="small",
        help="Whisper model size (tiny, base, small, medium, large).",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    audio_path = out_dir / "audio.wav"
    txt_path = out_dir / "transcript.txt"
    srt_path = out_dir / "transcript.srt"

    print(f"[INFO] Extracting audio from: {input_path}")
    extract_audio(input_path, audio_path)

    print(f"[INFO] Loading Whisper model: {args.model_size}")
    model = whisper.load_model(args.model_size)

    print("[INFO] Transcribing...")
    result = model.transcribe(str(audio_path), language="en")

    # Save text transcript
    full_text = result.get("text", "").strip()
    txt_path.write_text(full_text + "\n", encoding="utf-8")
    print(f"[OK] Transcript saved → {txt_path}")

    # Save SRT
    segments = result.get("segments", [])
    write_srt(segments, srt_path)
    print(f"[OK] Subtitles saved → {srt_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
