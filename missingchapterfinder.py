import os
import re

CHAPTERS_DIR = "LOTM Audiobook"

try:
    all_files = os.listdir(CHAPTERS_DIR)
except FileNotFoundError:
    print(f"❌ Folder not found: {CHAPTERS_DIR}")
    exit(1)

# Match only files like chapter_0001.mp3
chapter_files = []
chapter_nums = []

for f in all_files:
    match = re.fullmatch(r"chapter_(\d{4})\.mp3", f)
    if match:
        chapter_files.append(f)
        chapter_nums.append(int(match.group(1)))

if not chapter_nums:
    print("❌ No valid chapter MP3 files found.")
    exit(0)

chapter_nums.sort()
first = chapter_nums[0]
last = chapter_nums[-1]
missing = [i for i in range(first, last + 1) if i not in chapter_nums]

print(f"✅ Found {len(chapter_nums)} chapter files from {first:04} to {last:04}")

if missing:
    print("❗ Missing chapters:")
    for m in missing:
        print(f"chapter_{m:04}.mp3")
else:
    print("✅ No missing chapters.")
