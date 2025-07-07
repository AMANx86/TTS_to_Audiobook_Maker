import os
import asyncio
import subprocess

# Directory config (uses absolute paths for safety)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CHAPTERS_MP3_DIR = os.path.join(BASE_DIR, "chapter_mp3")
CHAPTERS_TXT_DIR = os.path.join(BASE_DIR, "chapters_txt")
TEMP_TRANSCRIPT = os.path.join(BASE_DIR, "__transcription_temp.txt")

WHISPER_CPP_EXEC = "/data/data/com.termux/files/home/whisper.cpp/build/bin/whisper-cli"  # Adjust if needed
WHISPER_MODEL = os.path.expanduser("~/whisper.cpp/models/ggml-tiny.bin")  # Adjust if needed

def normalize(text):
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

async def transcribe_audio(mp3_path):
    command = [
        WHISPER_CPP_EXEC,
        "-m", WHISPER_MODEL,
        "-f", mp3_path,
        "-otxt",
        "-of", TEMP_TRANSCRIPT
    ]
    process = await asyncio.create_subprocess_exec(*command)
    await process.communicate()

    output_path = TEMP_TRANSCRIPT + ".txt"
    if not os.path.exists(output_path):
        return None
    with open(output_path, "r", encoding="utf-8") as f:
        return f.readlines()

def read_original_lines(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.readlines()[2:]  # Skip first 2 lines (title, chapter number)

def find_mismatch(original_lines, transcript_lines):
    mismatches = []
    for i, (orig, trans) in enumerate(zip(original_lines, transcript_lines)):
        if normalize(orig) != normalize(trans):
            mismatches.append((i + 1, orig.strip(), trans.strip()))
    return mismatches

async def verify(mp3_path, txt_path):
    print(f"🔁 Transcribing: {mp3_path}")
    transcript_lines = await transcribe_audio(mp3_path)
    if transcript_lines is None:
        print(f"❌ Transcription failed: {mp3_path}")
        return False

    original_lines = read_original_lines(txt_path)
    mismatches = find_mismatch(original_lines, transcript_lines)

    if mismatches:
        print(f"❌ Would have deleted because of mismatch in {os.path.basename(mp3_path)}:")
        for i, orig, trans in mismatches:
            print(f"[Line {i}] ORIGINAL: {orig}")
            print(f"[Line {i}] TRANSCRIBED: {trans}")
        return False
    return True

async def main():
    files = os.listdir(CHAPTERS_MP3_DIR)
    proxy_mp3s = [f for f in files if f.startswith("proxy_chapter_") and f.endswith(".mp3")]

    sem = asyncio.Semaphore(4)

    async def sem_verify(mp3_fname):
        chapter_id = mp3_fname.split("_")[-1].replace(".mp3", "")
        txt_fname = f"chapter_{chapter_id}.txt"
        mp3_path = os.path.join(CHAPTERS_MP3_DIR, mp3_fname)
        txt_path = os.path.join(CHAPTERS_TXT_DIR, txt_fname)

        if not os.path.exists(txt_path):
            print(f"⚠️ Missing txt for chapter {chapter_id}, skipping verification.\nChecked path: {txt_path}")
            return

        async with sem:
            await verify(mp3_path, txt_path)

    await asyncio.gather(*(sem_verify(f) for f in proxy_mp3s))

if __name__ == "__main__":
    asyncio.run(main())
