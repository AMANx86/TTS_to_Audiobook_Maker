import os
import asyncio
import edge_tts
from pydub.utils import mediainfo
from concurrent.futures import ThreadPoolExecutor
import re
import shutil

CHAPTERS_DIR = "chapters"
OUTPUT_DIR = "LOTM Audiobook"
VOICE = "en-US-EricNeural"
MAX_CHARS = 3900
MAX_PARALLEL = 5
MIN_DURATION_SECONDS = 5.0  # Each chunk must be at least this long

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Break chapter text into safe chunks
def chunk_text(text, max_chars=MAX_CHARS):
    chunks = []
    current = ""
    for line in text.splitlines():
        if len(current) + len(line) + 1 > max_chars:
            chunks.append(current.strip())
            current = ""
        current += line + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

# Validate completed MP3
def is_valid_mp3(mp3_path, expected_chunks):
    if not os.path.exists(mp3_path):
        return False
    try:
        info = mediainfo(mp3_path)
        duration = float(info["duration"])
        return duration >= expected_chunks * MIN_DURATION_SECONDS
    except:
        return False

# Create a chapter MP3 safely
async def convert_chapter(txt_path, mp3_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    chunks = chunk_text(text)

    temp_dir = mp3_path + "_temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_mp3 = os.path.join(temp_dir, f"part_{i}.mp3")
        try:
            tts = edge_tts.Communicate(text=chunk, voice=VOICE)
            await tts.save(temp_mp3)
            info = mediainfo(temp_mp3)
            duration = float(info["duration"])
            if duration < MIN_DURATION_SECONDS:
                raise Exception("Chunk too short")
            temp_files.append(temp_mp3)
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise Exception(f"Failed chunk {i}: {e}")

    with open(mp3_path, "wb") as final:
        for part in temp_files:
            with open(part, "rb") as f:
                final.write(f.read())

    shutil.rmtree(temp_dir, ignore_errors=True)

# Run all chapters
async def generate_all():
    sem = asyncio.Semaphore(MAX_PARALLEL)
    tasks = []

    txt_files = sorted(
        [f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".txt")],
        key=lambda x: int(re.search(r"\d+", x).group())
    )

    for file in txt_files:
        chapter_num = int(re.search(r"\d+", file).group())
        txt_path = os.path.join(CHAPTERS_DIR, file)
        mp3_path = os.path.join(OUTPUT_DIR, f"chapter_{chapter_num:04}.mp3")

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        chunk_count = len(chunk_text(text))

        if is_valid_mp3(mp3_path, chunk_count):
            continue

        async def task(txt=txt_path, mp3=mp3_path, chunks=chunk_count):
            async with sem:
                while True:
                    try:
                        print(f"🔄 Converting {os.path.basename(txt)}")
                        await convert_chapter(txt, mp3)
                        print(f"✅ Finished {os.path.basename(mp3)}")
                        break
                    except Exception as e:
                        print(f"❌ Error: {e} — Retrying {os.path.basename(mp3)}")
                        if os.path.exists(mp3):
                            os.remove(mp3)
                        await asyncio.sleep(5)

        tasks.append(task())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(generate_all())
