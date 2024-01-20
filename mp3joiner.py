import os
import re
import shutil
import subprocess
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

# Define the root directory (edit this)
root_dir = "C:/Users/Administrator/Downloads/Audiobooks/join"

def natural_sort_key(s):
    """Natural sort helper function for sorting filenames containing numbers."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def escape_file_path(file_path):
    """Escapes file path to be safely used in shell commands."""
    return file_path.replace("'", "'\\''")

# First, calculate the total number of mp3 files
total_files = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    total_files += sum(f.endswith('.mp3') for f in filenames)

print(f"Starting the process... Total MP3 files to process: {total_files}")

processed_files = 0

# Use os.walk to traverse the directories
for dirpath, dirnames, filenames in os.walk(root_dir):
    if dirpath == root_dir:
        continue

    print(f"\nProcessing directory: {dirpath}")

    os.chdir(dirpath)

    # Sort the files using the natural sort key
    mp3_files = sorted([f for f in filenames if f.endswith('.mp3')], key=natural_sort_key)

    if not mp3_files:
        print("No MP3 files found in the directory. Skipping...")
        continue

    dir_track_count = len(mp3_files)
    print(f"Found {dir_track_count} tracks in the directory.")

    with open('ffmpeg_concat.txt', 'w', encoding='utf-8') as file:
        for f in mp3_files:
            escaped_file = escape_file_path(f)
            file.write(f"file '{escaped_file}'\n")

    folder_name = os.path.basename(dirpath)
    mp3_file_name = folder_name + ".mp3"

    print(f"Concatenating files in {dirpath}...")
    ffmpeg_command = f"ffmpeg -f concat -safe 0 -i ffmpeg_concat.txt -acodec copy \"{mp3_file_name}\""
    subprocess.run(ffmpeg_command, shell=True, encoding='utf-8')
    processed_files += dir_track_count

    print(f"Concatenation complete. {processed_files}/{total_files} files processed.")

    # Read ID3 tags and cover art from the first MP3 file
    first_file_tags = EasyID3(mp3_files[0])
    first_file_cover = None
    try:
        first_file_cover = ID3(mp3_files[0]).getall("APIC")[0]  # Assuming there's at least one image
    except Exception as e:
        print(f"Error extracting cover art: {e}")

    # Apply ID3 tags to the concatenated file
    audio = EasyID3(mp3_file_name)
    for key, value in first_file_tags.items():
        audio[key] = value
    audio.save()

    # Apply cover art if it exists
    if first_file_cover:
        audio = ID3(mp3_file_name)
        audio.add(first_file_cover)
        audio.save()

    print("Tags applied successfully.")

    shutil.move(mp3_file_name, os.path.join(root_dir, mp3_file_name))
    print(f"Final file saved to {root_dir}")

    os.chdir("..")
    os.remove(os.path.join(dirpath, 'ffmpeg_concat.txt'))

print(f"\nProcess completed. Total files processed: {processed_files}/{total_files}.")
