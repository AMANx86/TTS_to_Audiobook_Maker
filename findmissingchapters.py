import os
import re

CHAPTER_FOLDER = 'chapters_txt'

def extract_chapter_number_from_filename(filename):
    match = re.search(r'chapter_(\d+)', filename.lower())
    return int(match.group(1)) if match else None

def extract_chapter_number_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for _ in range(3):  # Check first 3 lines max
                line = f.readline().strip()
                match = re.search(r'chapter\s+(\d+)', line, re.IGNORECASE)
                if match:
                    return int(match.group(1))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return None

def find_missing_numbers(numbers):
    if not numbers:
        return []
    return sorted(set(range(min(numbers), max(numbers) + 1)) - set(numbers))

def main():
    files = sorted(os.listdir(CHAPTER_FOLDER))
    
    filename_chapters = []
    internal_chapters = []

    for file in files:
        if not file.endswith('.txt'):
            continue
        filepath = os.path.join(CHAPTER_FOLDER, file)

        # From filename
        file_chap = extract_chapter_number_from_filename(file)
        if file_chap is not None:
            filename_chapters.append(file_chap)

        # From file content
        content_chap = extract_chapter_number_from_file(filepath)
        if content_chap is not None:
            internal_chapters.append(content_chap)

    # Remove duplicates and sort
    filename_chapters = sorted(set(filename_chapters))
    internal_chapters = sorted(set(internal_chapters))

    missing_from_filenames = find_missing_numbers(filename_chapters)
    missing_from_file_content = find_missing_numbers(internal_chapters)

    print("🔍 Missing chapters based on FILENAME sequence:")
    print(missing_from_filenames or "None missing")

    print("\n📖 Missing or mismatched chapters based on FILE CONTENT:")
    print(missing_from_file_content or "None missing")

if __name__ == "__main__":
    main()
