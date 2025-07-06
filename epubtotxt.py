import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys

def epub_to_txt(epub_path, txt_path):
    book = epub.read_epub(epub_path)
    with open(txt_path, 'w', encoding='utf-8') as out_file:
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'lxml')
                text = soup.get_text()
                out_file.write(text + '\n')

if __name__ == "__main__":
    epub_path = sys.argv[1]
    txt_path = sys.argv[2]
    epub_to_txt(epub_path, txt_path)
