import os

MP3_DIR = "chapter_mp3"

def rename_all_to_proxy():
    files = sorted([f for f in os.listdir(MP3_DIR) if f.lower().endswith(".mp3")])
    for idx, filename in enumerate(files, start=1):
        new_name = f"proxy_chapter_{idx:04}.mp3"
        src = os.path.join(MP3_DIR, filename)
        dst = os.path.join(MP3_DIR, new_name)
        print(f"Renaming '{filename}' → '{new_name}'")
        os.rename(src, dst)

if __name__ == "__main__":
    rename_all_to_proxy()
