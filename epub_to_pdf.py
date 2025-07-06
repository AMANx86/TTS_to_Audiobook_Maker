import os
from ebooklib import epub
from bs4 import BeautifulSoup

def convert_epub_to_txt(epub_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    epub_path = os.path.join(current_dir, epub_filename)

    book = epub.read_epub(epub_path)
    full_text = ""
    count = 0

    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            if text.strip():
                count += 1
                full_text += f"\n\n--- Chapter {count} ---\n{text}"

    output_filename = os.path.splitext(epub_filename)[0] + ".txt"
    output_path = os.path.join(current_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Done: {output_path}")
    print(f"✅ Chapters Extracted: {count}")

convert_epub_to_txt("Lord of Mysteries - Book 1.epub")
