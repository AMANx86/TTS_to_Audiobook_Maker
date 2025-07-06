import os

CHAPTERS_DIR = "chapters"

try:
    files = os.listdir(CHAPTERS_DIR)
    print(f"✅ Found {len(files)} files in '{CHAPTERS_DIR}':")
    for f in files:
        print(" -", f)
except Exception as e:
    print("❌ Failed to list files:", e)
