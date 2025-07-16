import os
import re

CHAPTER_FOLDER = "chapters_txt"
CHAPTER_REGEX = re.compile(r"(?:chapter|ch\.?)\s*0*?(\d+)", re.IGNORECASE)
D_SHIFT = 3  # Shift distance for conflict resolution

def list_files():
    return sorted(
        [f for f in os.listdir(CHAPTER_FOLDER) if f.lower().startswith("chapter_") and f.lower().endswith(".txt")],
        key=lambda x: int(re.search(r"chapter_(\d+)", x).group(1)),
    )

def get_internal_chapter_number(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                m = CHAPTER_REGEX.search(line)
                if m:
                    return int(m.group(1))
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
    return None

def chapter_filename(num):
    return f"chapter_{num:04}.txt"

def merge_files(base_path, merge_path):
    with open(base_path, "a", encoding="utf-8") as base_f, open(merge_path, "r", encoding="utf-8") as merge_f:
        base_f.write("\n\n--- Merged duplicate content from file below ---\n\n")
        base_f.write(merge_f.read())
    os.remove(merge_path)
    print(f"🔀 Merged {os.path.basename(merge_path)} into {os.path.basename(base_path)}")

def cascade_rename(num):
    target_name = chapter_filename(num)
    target_path = os.path.join(CHAPTER_FOLDER, target_name)

    if not os.path.exists(target_path):
        return  # slot is free

    # Recursively free the next slot first
    cascade_rename(num + 1)

    # Now safe to move this file up
    next_name = chapter_filename(num + 1)
    next_path = os.path.join(CHAPTER_FOLDER, next_name)
    print(f"📦 Cascading rename: {target_name} -> {next_name}")
    os.rename(target_path, next_path)

def main():
    files = list_files()
    internal_map = {}

    # Step 1: Group files by internal chapter number
    for fname in files:
        path = os.path.join(CHAPTER_FOLDER, fname)
        internal_num = get_internal_chapter_number(path)
        if internal_num is None:
            print(f"⚠️ Skipping {fname}: no internal chapter number found")
            continue
        internal_map.setdefault(internal_num, []).append(fname)

    # Step 2: Merge duplicates (one merge per run)
    for internal_num, fnames in internal_map.items():
        if len(fnames) > 1:
            base_file = fnames[0]
            for duplicate_file in fnames[1:]:
                merge_files(os.path.join(CHAPTER_FOLDER, base_file), os.path.join(CHAPTER_FOLDER, duplicate_file))
                # Only one merge per run to keep it safe and incremental
                return

    # Step 3 & 4: Rename files to match internal number, handle conflicts with cascading rename
    files = list_files()  # refresh after merge
    existing_files = set(files)
    for fname in files:
        path = os.path.join(CHAPTER_FOLDER, fname)
        file_num = int(re.search(r"chapter_(\d+)", fname).group(1))
        internal_num = get_internal_chapter_number(path)

        if internal_num is None:
            continue

        if file_num == internal_num:
            continue  # no rename needed

        desired_name = chapter_filename(internal_num)
        desired_path = os.path.join(CHAPTER_FOLDER, desired_name)

        if not os.path.exists(desired_path):
            os.rename(path, desired_path)
            print(f"✅ Renamed {fname} -> {desired_name}")
            return  # one rename per run

        # Conflict! Do cascading rename to free slot
        cascade_rename(internal_num)
        os.rename(path, desired_path)
        print(f"✅ Renamed {fname} -> {desired_name} (after cascading rename)")
        return  # one rename per run

    print("✅ Nothing to merge or rename. All clean!")

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user")