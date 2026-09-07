"""Пути к данным и локальным утилитам приложения."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
ARCHIVE_FILE = BASE_DIR / "downloaded.txt"
YTDLP = BASE_DIR / "yt-dlp.exe"
MUSIC_DIR = BASE_DIR / "Music"
MEGA_MIX_DIR = MUSIC_DIR / "Mega Mix"
