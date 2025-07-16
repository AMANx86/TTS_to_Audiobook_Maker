import os
import re
from ebooklib import epub
from bs4 import BeautifulSoup

EPUB_FILE = 'book.epub'  # <-- Name of your EPUB file
CHAPTERS_TXT_FOLDER = 'chapters_txt'
MISSING_CHAPTERS_FOLDER = 'missing_chapters'

CHAPTER_REGEX = re.compile(r'chapter[_ ]?(\d{1,5})', re.IGNORECASE)

# --- Step 1: Load existing chapter numbers from chapters_txt/
def get_existing_chapter_numbers(folder):
    existing = set()
    for filename in os.listdir(folder):
        match = CHAPTER_REGEX.search(filename)
        if match:
            existing.add(int(match.group(1)))
    return existing

# --- Step 2: Extract all chapters from EPUB
def extract_all_epub_chapters(epub_path):
    book = epub.read_epub(epub_path)
    all_chapters = {}
    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            lines = text.strip().splitlines()
            for i, line in enumerate(lines):
                line = line.strip()
                match = re.match(r'(chapter|capítulo|ch)[\s\-:]*?(\d{1,5})\b', line, re.IGNORECASE)
                if match:
                    chapter_num = int(match.group(2))
                    # Grab some lines after for safety buffer
                    chapter_text = '\n'.join(lines[i:]).strip()
                    if chapter_num not in all_chapters:
                        all_chapters[chapter_num] = chapter_text
    return all_chapters

# --- Step 3: Save missing chapters
def save_missing_chapters(missing_chapters, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for chap_num, content in sorted(missing_chapters.items()):
        filename = f'chapter_{chap_num:04}.txt'
        path = os.path.join(output_folder, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f'✅ Saved missing: {filename}')

# --- Step 4: Main Logic
def main():
    print('📚 Checking existing chapters...')
    existing_chapters = get_existing_chapter_numbers(CHAPTERS_TXT_FOLDER)

    print(f'Found {len(existing_chapters)} existing chapters.')

    print('🔍 Scanning EPUB...')
    epub_chapters = extract_all_epub_chapters(EPUB_FILE)

    missing = {k: v for k, v in epub_chapters.items() if k not in existing_chapters}

    print(f'📂 Found {len(missing)} missing chapters.')
    if not missing:
        print('🎉 All chapters already exist. Nothing to do.')
        return

    print('✍️ Saving missing chapters...')
    save_missing_chapters(missing, MISSING_CHAPTERS_FOLDER)

    print('✅ Done.')

if __name__ == '__main__':
    main()
