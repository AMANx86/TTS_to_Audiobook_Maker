import os
import asyncio
import edge_tts
from pydub.utils import mediainfo
import re
import shutil

CHAPTERS_DIR = "chapters"
OUTPUT_DIR = "LOTM Audiobook"
VOICE = "en-US-EricNeural"
MAX_CHARS = 3900
MIN_LAST_CHUNK_CHARS = 1000  # Merge last chunk if smaller than this
MIN_DURATION_SECONDS = 5.0
MAX_PARALLEL = 5  # You can adjust

os.makedirs(OUTPUT_DIR, exist_ok=True)

def chunk_text(text, max_chars=MAX_CHARS, min_last_chunk_chars=MIN_LAST_CHUNK_CHARS):
    lines = text.splitlines()
    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 > max_chars:
            chunks.append(current.strip())
            current = ""
        current += line + "\n"

    if current.strip():
        chunks.append(current.strip())

    # Merge last chunk if too small
    if len(chunks) > 1 and len(chunks[-1]) < min_last_chunk_chars:
        chunks[-2] += "\n" + chunks[-1]
        chunks.pop()

    return chunks

def is_valid_mp3(mp3_path, expected_chunks):
    if not os.path.exists(mp3_path):
        return False
    try:
        info = mediainfo(mp3_path)
        duration = float(info["duration"])
        return duration >= expected_chunks * MIN_DURATION_SECONDS
    except:
        return False

async def convert_chapter(txt_path, mp3_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    chunks = chunk_text(text)

    temp_dir = mp3_path + "_temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_mp3 = os.path.join(temp_dir, f"part_{i}.mp3")
        tts = edge_tts.Communicate(text=chunk, voice=VOICE)
        await tts.save(temp_mp3)
        info = mediainfo(temp_mp3)
        duration = float(info["duration"])
        if duration < MIN_DURATION_SECONDS:
            raise Exception(f"Chunk {i} too short")
        temp_files.append(temp_mp3)

    with open(mp3_path, "wb") as final:
        for part in temp_files:
            with open(part, "rb") as f:
                final.write(f.read())

    shutil.rmtree(temp_dir, ignore_errors=True)

def find_missing_chapters():
    existing_mp3s = set()
    for f in os.listdir(OUTPUT_DIR):
        m = re.fullmatch(r"chapter_(\d{4})\.mp3", f)
        if m:
            existing_mp3s.add(int(m.group(1)))

    existing_txts = set()
    for f in os.listdir(CHAPTERS_DIR):
        m = re.fullmatch(r"chapter_(\d{4})\.txt", f)
        if m:
            existing_txts.add(int(m.group(1)))

    missing = sorted(existing_txts - existing_mp3s)
    return missing

def parse_input(chapter_input, available):
    chapters = set()
    parts = chapter_input.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            try:
                start_i = int(start)
                end_i = int(end)
                for i in range(start_i, end_i + 1):
                    if i in available:
                        chapters.add(i)
            except:
                pass
        else:
            try:
                i = int(part)
                if i in available:
                    chapters.add(i)
            except:
                pass
    return sorted(chapters)

async def main():
    missing = find_missing_chapters()
    if not missing:
        print("✅ No missing chapters to generate.")
        return

    print("Missing chapters detected:")
    print(", ".join(str(x) for x in missing))

    user_input = input("Enter chapters to generate (e.g. 1,3,5-7), or 'all': ").strip().lower()
    if user_input == "all":
        chapters_to_make = missing
    else:
        chapters_to_make = parse_input(user_input, set(missing))

    if not chapters_to_make:
        print("No valid chapters specified. Exiting.")
        return

    sem = asyncio.Semaphore(MAX_PARALLEL)

    async def task(chapter_num):
        txt_file = os.path.join(CHAPTERS_DIR, f"chapter_{chapter_num:04}.txt")
        mp3_file = os.path.join(OUTPUT_DIR, f"chapter_{chapter_num:04}.mp3")

        if not os.path.isfile(txt_file):
            print(f"⚠️ Text file not found for chapter {chapter_num:04}, skipping.")
            return

        async with sem:
            retry = 3
            while retry > 0:
                try:
                    print(f"🔄 Generating chapter {chapter_num:04}...")
                    await convert_chapter(txt_file, mp3_file)
                    print(f"✅ Finished chapter {chapter_num:04}")
                    break
                except Exception as e:
                    print(f"❌ Error in chapter {chapter_num:04}: {e}")
                    retry -= 1
                    if retry == 0:
                        print(f"⚠️ Failed chapter {chapter_num:04} after retries.")
                    else:
                        await asyncio.sleep(5)

    await asyncio.gather(*(task(ch) for ch in chapters_to_make))

if __name__ == "__main__":
    asyncio.run(main())
