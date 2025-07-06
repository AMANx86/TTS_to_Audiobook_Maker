# TTS-
This repo is for my exp in generating audiobook using tts like edge tts

#audiobookmaker.py
-when used will turn everything in the (chapters)- folder into a audio files the generated audio file will look like 
chapter_0001.mp3
chapter_0002.mp3
etc.
the stuff inside the chapters folder will need to be in .txt format
special note it uses parallel processing and it can be adjusted by changing the variable (MAX PARALLEL)

the files that will be made will be put into a file called "LOTM Audiobook"
just rename it to whatever you want 

#check_files.py
-this will list out all the files in chapters folder it will also mean if this file works then the audiobookmaker.py will also work fine 

#missingchapterfinder.py
-this will find if there are any missing chapters in the( chapters ) folder if there are it will list it out it.( detects mp3)

#missingchaptergenerator.py
-this script will generate the missing chapters that is found by the (missingchaptersfinder.py) this generates mp3 files 

#epubtotxt.py
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

This script, `audiobookmaker.py`, converts a directory of text chapters into an audiobook by generating MP3 files for each chapter using Microsoft's Edge TTS voices.

## Features

- **Text-to-Speech Conversion:** Converts `.txt` files in the `chapters` directory into MP3 audio using neural voices.
- **Automatic Chunking:** Splits large chapters into manageable chunks for TTS processing.
- **Parallel Processing:** Processes multiple chapters in parallel for faster audiobook generation.
- **Validation:** Verifies the output MP3s to ensure successful audio generation.
- **Error Handling & Retry:** Automatically retries failed conversions and ensures minimum duration for each audio chunk.
- **Organized Output:** Saves all generated MP3s in the `LOTM Audiobook` directory, named sequentially by chapter.

## Requirements

- Python 3.x
- [edge-tts](https://pypi.org/project/edge-tts/)
- [pydub](https://pypi.org/project/pydub/)

Install dependencies with:
```bash
pip install edge-tts pydub
```

## Usage

1. Place your chapter `.txt` files in a directory named `chapters` (e.g., `chapters/chapter_001.txt`).
2. Run the script:
   ```bash
   python audiobookmaker.py
   ```
3. The resulting MP3 files will be saved in the `LOTM Audiobook` directory.

## Notes

- The script uses the `en-US-EricNeural` voice by default. You can change the `VOICE` variable to any supported Edge TTS voice.
- Each chunk of text is limited to 3900 characters to comply with TTS API limits.
- Make sure your `.txt` files are sequentially numbered for correct chapter ordering.

---

