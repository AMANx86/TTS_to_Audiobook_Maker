import os
import re

CHAPTER_FOLDER = 'chapters_txt'

CENSOR_MAP = {
    r'\bf[\*\#\@]?u[\*\#\@]?c[\*\#\@]?k\b': 'fuck',
    r'\bs[\*\#\@]?h[\*\#\@]?i[\*\#\@]?t\b': 'shit',
    r'\ba[\*\#\@]?s[\*\#\@]?s\b': 'ass',
    r'\ba[\*\#\@]?s[\*\#\@]?s[\*\#\@]?h[\*\#\@]?o[\*\#\@]?l[\*\#\@]?e\b': 'asshole',
    r'\bb[\*\#\@]?i[\*\#\@]?t[\*\#\@]?c[\*\#\@]?h\b': 'bitch',
    r'\bc[\*\#\@]?u[\*\#\@]?n[\*\#\@]?t\b': 'cunt',
    r'\bd[\*\#\@]?i[\*\#\@]?c[\*\#\@]?k\b': 'dick',
    r'\bp[\*\#\@]?u[\*\#\@]?s[\*\#\@]?s[\*\#\@]?y\b': 'pussy'
}

GARBAGE_PATTERNS = [
    r'discord\.gg',
    r'telegram\.me',
    r't\.me/',
    r'join our discord',
    r'follow me on',
    r'patreon\.com',
    r'instagram\.com',
    r'facebook\.com',
    r'twitter\.com',
    r'credit.*translator',
    r'translated by',
    r'editor.*note',
    r'rehosted.*without permission',
    r'for faster updates',
    r'please rate',
    r'support.*author'
]

GARBAGE_RE = re.compile('|'.join(GARBAGE_PATTERNS), re.IGNORECASE)

TRANSLATOR_NOTE_START_RE = re.compile(
    r'(translator\'?s? note|translator notes|note from translator|translator\'?s? commentary|translator\'?s? message)',
    re.IGNORECASE
)

def uncensor_text(text):
    for pattern, replacement in CENSOR_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def remove_garbage_lines(text):
    lines = text.splitlines()
    cleaned = [line for line in lines if not GARBAGE_RE.search(line)]
    return '\n'.join(cleaned).strip()

def remove_translator_note_block(text):
    lines = text.splitlines()
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if not line:
            continue
        if TRANSLATOR_NOTE_START_RE.search(line):
            return '\n'.join(lines[:i]).rstrip()
        if GARBAGE_RE.search(line):
            garbage_start = i
            for j in range(i - 1, -1, -1):
                prev_line = lines[j].strip()
                if not prev_line or prev_line in ('***', '---'):
                    garbage_start = j
                elif TRANSLATOR_NOTE_START_RE.search(prev_line):
                    garbage_start = j
                    break
                elif GARBAGE_RE.search(prev_line):
                    garbage_start = j
                else:
                    break
            return '\n'.join(lines[:garbage_start]).rstrip()
    return text

def remove_extra_gaps(text):
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned_lines = []
    blank_count = 0
    for line in lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 1:
                cleaned_lines.append('')
        else:
            blank_count = 0
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines).strip()

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = uncensor_text(content)
    content = remove_garbage_lines(content)
    content = remove_translator_note_block(content)
    content = remove_extra_gaps(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"🧹 Cleaned: {os.path.basename(filepath)}")
    else:
        print(f"✅ No changes: {os.path.basename(filepath)}")

def process_folder(folder):
    if not os.path.exists(folder):
        print(f"❌ Folder not found: {folder}")
        return

    for fname in sorted(os.listdir(folder)):
        if fname.lower().endswith('.txt'):
            fpath = os.path.join(folder, fname)
            clean_file(fpath)

    print("\n🎉 All files processed.")

if __name__ == '__main__':
    process_folder(CHAPTER_FOLDER)
