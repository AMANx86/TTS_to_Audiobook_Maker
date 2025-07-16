import os
import re

# 🔧 Folder containing .txt chapter files
CHAPTER_FOLDER = 'chapters'

# ✅ Fixed regex: dash placed at the end to avoid bad character range
HEADER_RE = re.compile(r'(?i)^chapter\s+\d+(?:\s*[–: -]\s*.+)?$')

def fix_headers(text):
    lines = text.splitlines()
    cleaned_lines = []
    header_line = None
    header_found = False

    for line in lines:
        stripped = line.strip()

        # Detect first valid header
        if HEADER_RE.match(stripped):
            if not header_found:
                header_line = stripped  # Store first header exactly
                cleaned_lines.append(stripped)
                header_found = True
            elif stripped == header_line:
                continue  # Skip exact duplicate
            else:
                cleaned_lines.append(line)  # Keep other headings (not exact dupes)
        elif header_found and stripped == header_line:
            continue  # Remove exact dupe even if not matched by regex (extra safe)
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()

def process_folder(folder):
    fixed_count = 0
    skipped_count = 0

    for fname in sorted(os.listdir(folder)):
        if not fname.lower().endswith('.txt'):
            continue

        fpath = os.path.join(folder, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            original = f.read()

        fixed = fix_headers(original)

        if fixed != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f"🩹 Fixed headers in: {fname}")
            fixed_count += 1
        else:
            skipped_count += 1

    print(f"\n✅ Done. {fixed_count} files fixed. {skipped_count} untouched.")

if __name__ == '__main__':
    if not os.path.exists(CHAPTER_FOLDER):
        print(f"❌ Folder not found: {CHAPTER_FOLDER}")
    else:
        process_folder(CHAPTER_FOLDER)