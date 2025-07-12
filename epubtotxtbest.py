import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
import os

# Suppress the XML-as-HTML warning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def epub_to_txt(epub_path, txt_path):
    book = epub.read_epub(epub_path)
    with open(txt_path, 'w', encoding='utf-8') as out_file:
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), features="xml")
                text = soup.get_text()
                out_file.write(text + '\n')

def convert_all_epubs_in_directory():
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if filename.lower().endswith('.epub'):
            epub_path = os.path.join(current_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(current_dir, txt_filename)
            print(f"Converting: {filename} → {txt_filename}")
            epub_to_txt(epub_path, txt_path)

if __name__ == "__main__":
    convert_all_epubs_in_directory()
