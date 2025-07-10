# TTS-
This repo is for my exp in generating audiobook using tts like edge tts

##audiobookmaker

-when used will turn everything in the (chapters)- folder into a audio files the generated audio file will look like 
chapter_0001.mp3
chapter_0002.mp3
etc.

the stuff inside the chapters folder will need to be in .txt format
special note it uses parallel processing and it can be adjusted by changing the variable (MAX PARALLEL)

the files that will be made will be put into a file called "LOTM Audiobook"
just rename it to whatever you want 

##check_files.py

-this will list out all the files in chapters folder it will also mean if this file works then the audiobookmaker.py will also work fine 

##missingchapterfinder.py

-this will find if there are any missing chapters in the( chapters ) folder if there are it will list it out it.( detects mp3)

##missingchaptergenerator.py

-this script will generate the missing chapters that is found by the (missingchaptersfinder.py) this generates mp3 files 

##epubtotxt.py

-as the name suggests it turns whatever epub is feed to it, will become txt

all the files should be placed in the same folder as the epub










# EPUB to TXT Converter

This Python script converts an EPUB ebook into a plain text (.txt) file, extracting and organizing chapters for easy reading or further processing.

## Features

- Reads an EPUB file and extracts all text content.
- Organizes output by chapter.
- Outputs a single `.txt` file, named after the original EPUB.
- Displays completion status and chapter count.

## Requirements

- Python 3.x
- [ebooklib](https://pypi.org/project/EbookLib/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Install dependencies with:
```bash
pip install ebooklib beautifulsoup4
```

## Usage

1. Place your target EPUB file (e.g., `Lord of Mysteries - Book 1.epub`) in the same directory as `epub_to_pdf.py`.
2. Edit the script (last line) if you want to convert a different EPUB file:
   ```python
   convert_epub_to_txt("YourBook.epub")
   ```
3. Run the script:
   ```bash
   python epub_to_pdf.py
   ```

The script will generate `YourBook.txt` in the same directory, with each chapter separated and labeled.

## Example Output

```
--- Chapter 1 ---
[Chapter 1 text here]

--- Chapter 2 ---
[Chapter 2 text here]
...
```

## Notes

- Only extracts text content; images, formatting, and special elements are not preserved.
- Make sure the EPUB file exists in the script’s directory.

---





---

# Audiobook Maker

Turn text (TXT) files into audiobooks using Python and Microsoft's Edge TTS.

## Requirements

- Python 3.8 or higher
- edge-tts (Text-to-Speech for Microsoft Edge)
- ffmpeg (for audio file processing)

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo
   ```

2. Install required Python packages:
   ```sh
   pip install edge-tts
   ```

3. Make sure `ffmpeg` is installed and accessible from your command line.
   - You can download it from: https://ffmpeg.org/download.html

## Usage

### Step 1: Convert EPUB to TXT

- Use any tool (such as Calibre or online converters) to convert your `.epub` ebook to a plain `.txt` file.

### Step 2: Convert TXT to Audiobook

- Run the audiobook maker script to convert your TXT file into an audiobook (MP3):

   ```sh
   python audiobookmaker.py input.txt output.mp3
   ```

   - Replace `input.txt` with the path to your text file.
   - Replace `output.mp3` with your desired output filename.

### Additional Notes

- Ensure your TXT file is clean and well-formatted for best results.
- You may need to adjust chunk sizes or script parameters for very large books.

## License

MIT License

---

