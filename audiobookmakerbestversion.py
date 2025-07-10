import os
import asyncio
import edge_tts
import re
import shutil

CHAPTERS_DIR = "chapters"
OUTPUT_DIR = "LOTM Audiobook"
VOICE = "en-US-EricNeural"
CHUNK_SIZE = 1000
MAX_PARALLEL = 80

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Clean text chunking with no empty results
def chunk_text(text, max_chars=CHUNK_SIZE):
    words = text.split()
    chunks = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            chunks.append(current.strip())
            current = word
        else:
            current += " " + word
    if current.strip():
        chunks.append(current.strip())
    return chunks

# Check if MP3 exists and is valid (non-zero)
def is_valid_mp3(mp3_path):
    return os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1000

# Convert a single chapter to MP3
async def convert_chapter(txt_path, mp3_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        raw = f.read()

    text = raw.strip()
    if not text:
        raise Exception("Chapter is empty")

    chunks = chunk_text(text)
    if not chunks:
        raise Exception("No valid chunks found")

    temp_dir = mp3_path + "_temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_mp3 = os.path.join(temp_dir, f"part_{i}.mp3")
        try:
            print(f"🔊 Generating part_{i}.mp3 ({len(chunk)} chars)")
            tts = edge_tts.Communicate(text=chunk, voice=VOICE)
            await tts.save(temp_mp3)
            await asyncio.sleep(0.5)  # Let the file finish writing
            if not os.path.exists(temp_mp3) or os.path.getsize(temp_mp3) < 1000:
                raise Exception(f"Part {i} failed — file not written or too small")
            temp_files.append(temp_mp3)
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise Exception(f"Chunk {i} failed: {e}")

    # Stitch parts together
    with open(mp3_path, "wb") as final:
        for part in temp_files:
            with open(part, "rb") as f:
                final.write(f.read())

    shutil.rmtree(temp_dir, ignore_errors=True)

# Run all chapters
async def generate_all():
    sem = asyncio.Semaphore(MAX_PARALLEL)
    tasks = []

    files = sorted(
        [f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".txt")],
        key=lambda x: int(re.search(r"\d+", x).group())
    )

    for file in files:
        chapter_num = int(re.search(r"\d+", file).group())
        txt_path = os.path.join(CHAPTERS_DIR, file)
        mp3_path = os.path.join(OUTPUT_DIR, f"chapter_{chapter_num:04}.mp3")

        if is_valid_mp3(mp3_path):
            continue

        async def task(txt=txt_path, mp3=mp3_path):
            async with sem:
                while True:
                    try:
                        print(f"📘 Converting {os.path.basename(txt)}")
                        await convert_chapter(txt, mp3)
                        print(f"✅ Done: {os.path.basename(mp3)}")
                        break
                    except Exception as e:
                        print(f"❌ Error: {e} — Retrying...")
                        if os.path.exists(mp3):
                            os.remove(mp3)
                        await asyncio.sleep(3)

        tasks.append(task())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(generate_all())
