#!/usr/bin/env python3
"""Local Whisper-based CLI for transcribing .ogg audio files."""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path
from typing import Optional


LOGGER = logging.getLogger("transcribe")
SUPPORTED_MODELS = ("tiny", "base", "small", "medium", "large")


class TranscriptionError(Exception):
    """Raised when transcription cannot proceed."""


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe a .ogg audio file into text using local Whisper models.",
    )
    parser.add_argument(
        "input",
        help="Path to the input .ogg file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional path to the output .txt file. Defaults to input filename with .txt extension.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="base",
        choices=SUPPORTED_MODELS,
        help="Whisper model size to use (default: base).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logs and Whisper segment progress output.",
    )
    return parser.parse_args(argv)


def validate_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise TranscriptionError(
            "ffmpeg is not installed or not available in PATH. Install ffmpeg to process .ogg files."
        )


def validate_input_file(input_path: Path) -> None:
    if not input_path.exists():
        raise TranscriptionError(f"Input file does not exist: {input_path}")
    if not input_path.is_file():
        raise TranscriptionError(f"Input path is not a file: {input_path}")
    if input_path.suffix.lower() != ".ogg":
        raise TranscriptionError(
            f"Unsupported file extension '{input_path.suffix}'. Expected a .ogg file."
        )


def resolve_output_path(input_path: Path, output_arg: Optional[str]) -> Path:
    if output_arg:
        output_path = Path(output_arg).expanduser().resolve()
    else:
        output_path = input_path.with_suffix(".txt")
    if output_path.suffix.lower() != ".txt":
        output_path = output_path.with_suffix(".txt")
    return output_path


def transcribe_audio(input_path: Path, model_name: str, verbose: bool) -> str:
    try:
        import whisper
    except ImportError as exc:
        raise TranscriptionError(
            "Missing dependency 'openai-whisper'. Install requirements first."
        ) from exc

    LOGGER.info("Loading Whisper model: %s", model_name)
    model = whisper.load_model(model_name)

    LOGGER.info("Starting transcription: %s", input_path)
    result = model.transcribe(str(input_path), verbose=verbose)
    text = (result.get("text") or "").strip()

    if not text:
        raise TranscriptionError("Transcription completed but produced empty text.")

    LOGGER.info("Transcription completed successfully")
    return text


def write_output(output_path: Path, text: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text + "\n", encoding="utf-8")
    LOGGER.info("Saved transcription to: %s", output_path)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    try:
        input_path = Path(args.input).expanduser().resolve()
        validate_ffmpeg()
        validate_input_file(input_path)

        output_path = resolve_output_path(input_path, args.output)
        text = transcribe_audio(input_path, args.model, args.verbose)
        write_output(output_path, text)

        print(text)
        return 0
    except KeyboardInterrupt:
        LOGGER.error("Interrupted by user")
        return 130
    except TranscriptionError as exc:
        LOGGER.error("%s", exc)
        return 1
    except Exception as exc:  # pragma: no cover
        LOGGER.exception("Unexpected error during transcription: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
