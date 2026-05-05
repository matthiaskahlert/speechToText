# speechToText

Production-ready Python CLI tool for local speech-to-text transcription of `.ogg` audio files using Whisper.

## Folder Structure

```text
speechToText/
├── README.md
├── requirements.txt
└── transcribe.py
```

## Prerequisites

- Python 3.10+
- `ffmpeg` installed and available in `PATH`

### Install ffmpeg

Windows (winget):

```powershell
winget install --id Gyan.FFmpeg -e
```

macOS (Homebrew):

```bash
brew install ffmpeg
```

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y ffmpeg
```

## Setup

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic:

```bash
python transcribe.py path/to/audio.ogg
```

With custom output path:

```bash
python transcribe.py path/to/audio.ogg --output path/to/result.txt
```

With model selection:

```bash
python transcribe.py path/to/audio.ogg --model small
```

Verbose mode (includes more logs and segment progress output):

```bash
python transcribe.py path/to/audio.ogg --verbose
```

## CLI Arguments

- `input` (required): Path to `.ogg` file.
- `-o, --output` (optional): Output text file path. Defaults to input filename with `.txt` extension.
- `-m, --model` (optional): Whisper model size. Choices: `tiny`, `base`, `small`, `medium`, `large`. Default: `base`.
- `-v, --verbose` (optional): Enable verbose logging and progress output.

## Output

- Prints transcription to the console.
- Saves transcription to a `.txt` file.

Default output path example:

- Input: `recordings/interview.ogg`
- Output: `recordings/interview.txt`

## Error Handling

The CLI handles common failure scenarios gracefully:

- Missing input file
- Invalid input type (not `.ogg`)
- `ffmpeg` not installed or not in `PATH`
- Empty transcription output
- Unexpected runtime errors with clear logging
