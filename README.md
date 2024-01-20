# Audiobook MP3 Concatenation Script

This Python script concatenates multiple MP3 files within each subdirectory of a given directory, preserving the ID3 tags, including cover art, from the first file in each subdirectory. It is designed to handle special characters in file names and ensures the correct order of files based on natural sorting.

## Features

- Concatenates MP3 files in each subdirectory.
- Preserves ID3 tags, including cover art.
- Handles special characters in file paths.
- Ensures natural sorting order of files (e.g., 1, 2, ... 10, 11, ...).

## Prerequisites

Before running this script, ensure you have the following installed:
- Python 3
- FFmpeg
- Mutagen (Python library)

## Installation

1. **Clone the repository:**
```
git clone https://github.com/dursch/audiobook-joiner.git

```

2. **Install Mutagen:**

```
pip install mutagen

```

3. **Ensure FFmpeg is installed and accessible in your system's PATH.**

## Usage

1. Place the script in a directory containing subdirectories with MP3 files.

2. Open a terminal and navigate to the script's directory.

3. Run the script:

```
python mp3joiner.py
```
4. The script will process each subdirectory, concatenating MP3 files, preserving ID3 tags from the first file, and saving the output in the specified root directory.

## Known Issues

- **Special Character Handling:** The script attempts to handle special characters in file paths, but certain unique cases might cause issues. If you encounter problems, check the file names for unusual characters.

- **Order of Files:** The script uses natural sorting, but if your file naming convention is unusual, you might need to adjust the sorting function.

- **ID3 Tags Limitation:** The script currently transfers ID3 tags from the first file in the directory. If you require a different method for selecting which file's tags to preserve, additional modifications to the script are needed.
