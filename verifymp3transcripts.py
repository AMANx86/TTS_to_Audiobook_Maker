import os
import re
import argparse
import subprocess
from difflib import SequenceMatcher

CHAPTERS_MP3 = "D:\\Audibook_process\\chapters_mp3"
CHAPTERS_TXT = "D:\\Audibook_process\\chapters_txt"

def sanitize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    substitutions = {
        "f*ck": "fuck", "sh*t": "shit", "d*mn": "damn", "h*ll": "hell",
        "hmph": "hmm", "uhhh": "uh", "ummm": "um"
    }
    for bad, good in substitutions.items():
        text = text.replace(bad, good)
    return text.strip()

def get_transcription(mp3_path):
    print(f"🔁 Transcribing: {mp3_path}")
    command = ["whisper", mp3_path, "--language", "en", "--task", "transcribe", "--model", "medium", "--output_format", "txt", "--output_dir", "."]
    try:
        subprocess.run(command, check=True)
        txt_file = os.path.splitext(os.path.basename(mp3_path))[0] + ".txt"
        if not os.path.exists(txt_file):
            print(f"❌ No transcription output for {mp3_path}")
            return []
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = [sanitize(line) for line in f.readlines() if line.strip()]
        os.remove(txt_file)
        return lines
    except subprocess.CalledProcessError:
        print(f"❌ Transcription failed for {mp3_path}")
        return []

def compare_texts(transcribed, original):
    mismatches = []
    for i, (t_line, o_line) in enumerate(zip(transcribed, original)):
        if SequenceMatcher(None, t_line, o_line).ratio() < 0.85:
            mismatches.append((i, t_line, o_line))
    if len(original) > len(transcribed):
        for j in range(len(transcribed), len(original)):
            mismatches.append((j, '', original[j]))
    return mismatches

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapters', type=str, help="Specify chapters like 12 or 5-10")
    args = parser.parse_args()

    files = sorted(f for f in os.listdir(CHAPTERS_MP3) if f.startswith("proxy_chapter_") and f.endswith(".mp3"))
    if args.chapters:
        selected = set()
        parts = args.chapters.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                selected.update(range(start, end + 1))
            else:
                selected.add(int(part))
        files = [f for f in files if int(re.findall(r'\d+', f)[0]) in selected]

    if not files:
        print("No MP3 files found to process.")
        return

    for mp3_file in files:
        chapter_num = re.findall(r'\d+', mp3_file)[0]
        txt_file = f"chapter_{chapter_num.zfill(4)}.txt"
        mp3_path = os.path.join(CHAPTERS_MP3, mp3_file)
        txt_path = os.path.join(CHAPTERS_TXT, txt_file)

        if not os.path.exists(txt_path):
            print(f"⚠️ Missing txt for chapter {chapter_num}, skipping.")
            continue

        with open(txt_path, 'r', encoding='utf-8') as f:
            original_lines = [sanitize(line) for line in f.readlines() if line.strip()]

        transcribed_lines = get_transcription(mp3_path)
        if not transcribed_lines:
            continue

        mismatches = compare_texts(transcribed_lines, original_lines)

        base_name = f"chapter_{chapter_num.zfill(4)}"
        new_name = f"{base_name}.verified.mp3" if not mismatches else f"{base_name}.failed.mp3"
        new_path = os.path.join(CHAPTERS_MP3, new_name)
        os.rename(mp3_path, new_path)

        if mismatches:
            print(f"❌ Mismatches found in {base_name}.mp3 — would have been deleted:")
            for idx, t, o in mismatches[:3]:  # limit output
                print(f"   Line {idx+1}:")
                print(f"     Expected: {o}")
                print(f"     Found:    {t}")
        else:
            print(f"✅ {base_name}.mp3 passed verification.")

if __name__ == "__main__":
    main()
