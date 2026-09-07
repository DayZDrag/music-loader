"""Загрузка и сохранение пользовательской конфигурации плейлистов."""

import json
from tkinter import messagebox

from .paths import CONFIG_FILE

DEFAULT_CONFIG = {"authors": {}}


def load_config():
    """Возвращает конфигурацию без перезаписи повреждённого файла."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        messagebox.showerror(
            "Ошибка",
            "Не удалось прочитать config.json.\n"
            "Будет загружена стандартная конфигурация.",
        )
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Сохраняет конфигурацию в UTF-8 с читаемым форматированием."""
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
