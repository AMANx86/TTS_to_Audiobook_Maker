import os

CHAPTERS_DIR = "chapters_txt"
OUTPUT_DIR = "chapters_txt_cleaned"
UNWANTED_PATTERNS = [
    "Discord: dsc.gg/wetried","Link to donations in the discord!","Discord: /translatingnovice","freewēbnoveℓ.com"
]

REMOVE_BLANK_LINES = False  # set to True if you want to remove truly blank lines

def should_remove(line):
    stripped = line.strip()
    for pattern in UNWANTED_PATTERNS:
        if pattern.lower() in stripped.lower():
            return True
    return False

def clean_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        if REMOVE_BLANK_LINES and line.strip() == "":
            continue
        if not should_remove(line):
            cleaned_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".txt")]
    for filename in files:
        src = os.path.join(CHAPTERS_DIR, filename)
        dst = os.path.join(OUTPUT_DIR, filename)
        clean_file(src, dst)
        print(f"[SAFE CLEANED] {filename} → {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
