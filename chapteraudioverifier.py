import os
import subprocess
import sys
import difflib
import re

def normalize_text(text):
    """Lowercase and remove punctuation from text for comparison."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def transcribe(mp3_path, output_basename):
    print(f"🔁 Transcribing: {mp3_path}")
    cmd = [
        "bash", "-c",
        f"./build/bin/whisper-cli -m models/ggml-tiny.bin -f '{mp3_path}' -otxt -of '{output_basename}'"
    ]
    subprocess.run(cmd, cwd=os.path.expanduser("~/whisper.cpp"))

def compare_texts(original_path, generated_path):
    with open(original_path, 'r', encoding='utf-8') as f1, open(generated_path, 'r', encoding='utf-8') as f2:
        original = f1.read().split('\n', 2)[2]  # Skip chapter name and number
        generated = f2.read()

    norm_original = normalize_text(original)
    norm_generated = normalize_text(generated)

    if norm_original in norm_generated or norm_generated in norm_original:
        print("✅ Match: Transcript aligns with text file.")
    else:
        ratio = difflib.SequenceMatcher(None, norm_original, norm_generated).ratio()
        print(f"❌ Mismatch! Similarity ratio: {ratio:.2f}")
        print("🧪 This would trigger reprocessing if deletion were enabled.")

def verify(mp3_file, txt_file):
    base_dir = os.path.expanduser("~/storage/shared/test.verifyscript/")
    mp3_path = os.path.join(base_dir, mp3_file)
    txt_path = os.path.join(base_dir, txt_file)
    temp_out_base = os.path.join(base_dir, "__transcription_temp")

    transcribe(mp3_path, temp_out_base)
    compare_texts(txt_path, temp_out_base + ".txt")

    # Optional: Delete temp file after testing
    os.remove(temp_out_base + ".txt")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python chapteraudioverifier.py chapter_0258.mp3 chapter_0258.txt")
        sys.exit(1)

    verify(sys.argv[1], sys.argv[2])
