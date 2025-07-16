import zipfile
import os
import re
from bs4 import BeautifulSoup

# === USER CONFIG ===
EPUB_FILE = "A RegressorS Tale Of Cultivation c1-671.epub"  # Put your EPUB filename here
MISSING_CHAPTERS =[143, 211, 237, 238, 326, 396, 435, 441, 445] # Your manually provided list
OUTPUT_FOLDER = "extracted_missing_chapters"

# === CLEAN TEXT FROM HTML ===
def clean_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator="\n").strip()

# === FIND CHAPTER NUMBER IN TEXT ===
def match_target_chapter(text, targets):
    lines = text.splitlines()
    for line in lines[:5]:  # Only check top 5 lines for performance
        match = re.search(r'\bchapter\s+(\d{1,5})\b', line, re.IGNORECASE)
        if match:
            number = int(match.group(1))
            if number in targets:
                return number
    return None

# === SAVE FILE ===
def save_txt(content, chapter_number):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filename = f"chapter_{chapter_number:04d}.txt"
    with open(os.path.join(OUTPUT_FOLDER, filename), 'w', encoding='utf-8') as f:
        f.write(content)

# === MAIN LOGIC ===
def extract_chapters(epub_path, missing_list):
    found = set()
    with zipfile.ZipFile(epub_path, 'r') as z:
        html_files = [f for f in z.namelist() if f.endswith(('.xhtml', '.html', '.htm'))]

        for file in html_files:
            with z.open(file) as f:
                raw_html = f.read().decode('utf-8', errors='ignore')
                text = clean_text(raw_html)

                chapter_number = match_target_chapter(text, missing_list)
                if chapter_number and chapter_number not in found:
                    save_txt(text, chapter_number)
                    print(f"✅ Extracted Chapter {chapter_number}")
                    found.add(chapter_number)

    # Report anything that couldn't be found
    not_found = set(missing_list) - found
    if not_found:
        print("\n❌ Chapters not found in EPUB:")
        print(sorted(not_found))
    else:
        print("\n🎉 All missing chapters successfully extracted.")

# === RUN ===
if __name__ == "__main__":
    extract_chapters(EPUB_FILE, MISSING_CHAPTERS)
