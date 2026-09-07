import customtkinter as ctk
import subprocess
import threading
import json
import os
import random
import re
import shutil
from pathlib import Path
from tkinter import messagebox, simpledialog

from music_loader import config as playlist_config
from music_loader.paths import (
    ARCHIVE_FILE as archive_file,
    BASE_DIR as base_dir,
    MEGA_MIX_DIR as mega_mix_dir,
    MUSIC_DIR as music_dir,
    YTDLP as ytdlp,
)
from music_loader import theme


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
ARCHIVE_FILE = BASE_DIR / "downloaded.txt"
YTDLP = BASE_DIR / "yt-dlp.exe"

MUSIC_DIR = BASE_DIR / "Music"
MEGA_MIX_DIR = MUSIC_DIR / "Mega Mix"

MUSIC_DIR.mkdir(exist_ok=True)

DEFAULT_CONFIG = {
    "authors": {
        "Без автора": [
            {"name": "Аниме девочки", "url": "https://www.youtube.com/watch?v=91frwuPB7qg&list=PL7zP0eszV-v-fGzvjwr6m5u5Zmgdiix20"},
            {"name": "Много часавой трип", "url": "https://www.youtube.com/watch?v=XPCinyyrMAg&list=PL7zP0eszV-v_BqKkbh4mISXN0YheSgfAF"},
            {"name": "Проклятые сонги", "url": "https://www.youtube.com/watch?v=tM38NPwLsa0&list=PL7zP0eszV-v9blEUzmLl92ja_uX6FTeUD"},
            {"name": "уголок моего сознания (музыка)", "url": "https://www.youtube.com/watch?v=3Ia1ZEmNMfk&list=PL7zP0eszV-v8S_Tb6DEVh2MgY3XUnwuN&index=1"},
            {"name": "чиловый сонг", "url": "https://www.youtube.com/watch?v=7-smjiy5NSA&list=PL7zP0eszV-v9pA10SrCvv04Cuxps3V5Jd"},
            {"name": "Неповторимые произведения единые зависимостью к ним", "url": "https://www.youtube.com/watch?v=ciBAlRKs7WE&list=PL7zP0eszV-v89-s08NgRVtaHBcWP5sLtF"},
            {"name": "Музяка", "url": "https://www.youtube.com/watch?v=W5Sq71VTJ9Q&list=PL7zP0eszV-v_0F10-JWBloKyVuZ0wJyXj"}
        ],
        "pomipomi": [
            {"name": "вкусный pomipomi", "url": "https://www.youtube.com/watch?v=U8lJbinCsWI&list=PLUi7NEa3SQxA"}
        ],
        "MiatriSs": [
            {"name": "MiatriSs", "url": "https://www.youtube.com/watch?v=KJrsNbVvYlE&list=PL7zP0eszV-v9sznyX17U84Q-MeRWcwJ3X"}
        ],
        "H2M birdman": [
            {"name": "H2M birdman", "url": "https://www.youtube.com/watch?v=wIB7exGmL2A&list=PL7zP0eszV-v85eRL8j3QfNvIbuGugtDUn"}
        ],
        "Glyde": [
            {"name": "Glyde", "url": "https://www.youtube.com/watch?v=ijSIFzHTnfg&list=PL7zP0eszV-v9EXV16tcVpFaPR8UKm7-dZ"}
        ],
        "Hotline Miami Soundtracks": [
            {"name": "Hotline Miami Soundtracks", "url": "https://www.youtube.com/watch?v=QXkSYSPTpj4&list=PLk2QSht0RAUEMduNgBzaW3RrQVuokzkLE"}
        ],
        "польмихан": [
            {"name": "польмихан", "url": "https://www.youtube.com/watch?v=eA9nx32LyPc&list=PLlk05udgFTA9M3vvC_iR2vspIGJ_ZZG7j"},
            {"name": "польмихан вставай", "url": "https://www.youtube.com/watch?v=eA9nx32LyPc&list=OLAK5uy_l_N_aNe8N6giFgnUOmObMTtaDXsCLlk7k"},
            {"name": "польмихан фителёк", "url": "https://www.youtube.com/watch?v=PwQBiee-PMk&list=OLAK5uy_kk0XtD--oMInkD7fWeAioch0YKeVLNdGc"},
            {"name": "польмихан промежуток", "url": "https://www.youtube.com/watch?v=2qEqpBm0JJU&list=OLAK5uy_mN6ytr7kNy9ekCHY6s4NRJOxtiZkFDVc0"},
            {"name": "польмихан формальности", "url": "https://www.youtube.com/watch?v=Qi1T-rfgga4&list=OLAK5uy_nNPMrQfXnhroK0GyvhzsJfvM-23Fr93rA"},
            {"name": "польмихан свет мрака", "url": "https://www.youtube.com/watch?v=e4a1lfjlfsk&list=OLAK5uy_mN6ytr7kNy9ekCHY6s4NRJOxtiZkFDVc0"},
            {"name": "польмихан центр своей реальности", "url": "https://www.youtube.com/watch?v=brQAZqJ_Fek&list=OLAK5uy_kX_bCw_4qO4PKRzpfd_ScB548RXhdyjs8"}
        ],
        "Pomipomi": [
            {"name": "Pomipomi", "url": "https://www.youtube.com/watch?v=fHHB6XtjTcg&list=PLstjVgPXwnbJ0uS2vmD3FJJIPQE7sAO3R"},
            {"name": "Pomipomi 2 плейлист", "url": "https://www.youtube.com/watch?v=q_vwmeIIfW8&list=PLstjVgPXwnbKxsGeL8S-FrK7pxdBfeUlQ"}
        ],
        "Geoxor": [
            {"name": "Geoxor", "url": "https://www.youtube.com/watch?v=qDztrDlW1RE&list=PLJDb8my65gWwlSlcTvzZMuCeWlzBySIec"}
        ]
    }
}


def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        messagebox.showerror(
            "Ошибка",
            "Не удалось прочитать config.json.\n"
            "Будет загружена стандартная конфигурация."
        )
        return DEFAULT_CONFIG.copy()


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


# ============================================================
# COLORS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#07111F"
PANEL = "#0B1728"
PANEL_2 = "#101F34"
BLUE = "#147DFF"
BLUE_HOVER = "#0F68D8"
CYAN = "#00BFFF"
TEXT = "#F2F7FF"
TEXT_SECONDARY = "#7F96B2"
GREEN = "#27D17F"
RED = "#FF4D67"
YELLOW = "#FFC857"

# Общие значения находятся в пакете music_loader. Эти псевдонимы сохраняют
# совместимость с остальным UI во время поэтапной декомпозиции класса.
load_config = playlist_config.load_config
save_config = playlist_config.save_config
BASE_DIR = base_dir
ARCHIVE_FILE = archive_file
YTDLP = ytdlp
MUSIC_DIR = music_dir
MEGA_MIX_DIR = mega_mix_dir
BG = theme.BG
PANEL = theme.PANEL
PANEL_2 = theme.PANEL_2
BLUE = theme.BLUE
BLUE_HOVER = theme.BLUE_HOVER
CYAN = theme.CYAN
TEXT = theme.TEXT
TEXT_SECONDARY = theme.TEXT_SECONDARY
GREEN = theme.GREEN
RED = theme.RED
YELLOW = theme.YELLOW


# ============================================================
# MAIN APP
# ============================================================

class MusicLoader(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("MEGA MIX - MUSIC LOADER")
        self.geometry("1250x800")
        self.minsize(1050, 680)
        self.configure(fg_color=BG)

        self.config = load_config()
        self.current_author = None
        self.current_playlist_index = None
        self.downloading = False
        self.stop_requested = False

        self.create_ui()
        self.refresh_authors()

    # ========================================================
    # FILE STATISTICS
    # ========================================================

    def get_playlist_folder(self, author, playlist):
        return MUSIC_DIR / author / playlist

    def get_playlist_tracks(self, author, playlist):
        folder = self.get_playlist_folder(author, playlist)
        if not folder.exists():
            return []

        try:
            tracks = [
                file for file in folder.iterdir()
                if file.is_file() and file.suffix.lower() == ".mp3"
            ]
            return sorted(tracks, key=lambda x: x.name.lower())
        except Exception:
            return []

    def get_playlist_count(self, author, playlist):
        return len(self.get_playlist_tracks(author, playlist))

    def get_author_track_count(self, author):
        total = 0
        playlists = self.config["authors"].get(author, [])
        for playlist in playlists:
            total += self.get_playlist_count(author, playlist["name"])
        return total

    # ========================================================
    # UI
    # ========================================================

    def create_ui(self):
        from music_loader.dashboard import build_dashboard

        build_dashboard(self)
        return

        # HEADER
        self.header = ctk.CTkFrame(
            self, height=70, fg_color=PANEL, corner_radius=0
        )
        self.header.pack(fill="x")

        self.logo = ctk.CTkLabel(
            self.header,
            text="MEGA",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=TEXT
        )
        self.logo.pack(side="left", padx=(25, 5))

        self.logo_blue = ctk.CTkLabel(
            self.header,
            text="MIX",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=BLUE
        )
        self.logo_blue.pack(side="left")

        self.status_label = ctk.CTkLabel(
            self.header,
            text="● READY",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=GREEN
        )
        self.status_label.pack(side="right", padx=30)

        # MAIN
        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.pack(fill="both", expand=True)

        # AUTHORS
        self.author_panel = ctk.CTkFrame(
            self.main, width=260, fg_color=PANEL, corner_radius=0
        )
        self.author_panel.pack(side="left", fill="y")
        self.author_panel.pack_propagate(False)

        ctk.CTkLabel(
            self.author_panel,
            text="AUTHORS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.author_list = ctk.CTkScrollableFrame(
            self.author_panel, fg_color="transparent"
        )
        self.author_list.pack(fill="both", expand=True, padx=10)

        self.add_author_button = ctk.CTkButton(
            self.author_panel,
            text="+  ДОБАВИТЬ АВТОРА",
            height=40,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.add_author
        )
        self.add_author_button.pack(fill="x", padx=15, pady=(10, 5))

        self.delete_author_button = ctk.CTkButton(
            self.author_panel,
            text="−  УДАЛИТЬ АВТОРА",
            height=36,
            fg_color="#18263A",
            hover_color="#263B56",
            command=self.delete_author
        )
        self.delete_author_button.pack(fill="x", padx=15, pady=(0, 15))

        # CENTER
        self.center = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        self.center.pack(side="left", fill="both", expand=True)

        self.author_title = ctk.CTkLabel(
            self.center,
            text="Выберите автора",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=TEXT
        )
        self.author_title.pack(anchor="w", padx=25, pady=(22, 5))

        self.author_subtitle = ctk.CTkLabel(
            self.center,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY
        )
        self.author_subtitle.pack(anchor="w", padx=27, pady=(0, 15))

        # PLAYLISTS
        self.playlist_list = ctk.CTkScrollableFrame(
            self.center, fg_color=PANEL, corner_radius=12
        )
        self.playlist_list.pack(
            fill="both", expand=True, padx=25, pady=(0, 15)
        )

        # TRACK PANEL
        self.track_header = ctk.CTkFrame(
            self.center, fg_color=PANEL, height=45, corner_radius=8
        )
        self.track_header.pack(
            fill="x", padx=25, pady=(0, 8)
        )

        self.track_title = ctk.CTkLabel(
            self.track_header,
            text="TRACKS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY
        )
        self.track_title.pack(side="left", padx=15)

        self.track_count = ctk.CTkLabel(
            self.track_header,
            text="0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=CYAN
        )
        self.track_count.pack(side="right", padx=15)

        self.track_list = ctk.CTkScrollableFrame(
            self.center,
            height=145,
            fg_color=PANEL,
            corner_radius=10
        )
        self.track_list.pack(fill="x", padx=25, pady=(0, 10))

        # PLAYLIST CONTROLS
        self.controls = ctk.CTkFrame(
            self.center, fg_color="transparent"
        )
        self.controls.pack(fill="x", padx=25)

        self.add_playlist_button = ctk.CTkButton(
            self.controls,
            text="+  ДОБАВИТЬ",
            height=38,
            fg_color=PANEL_2,
            hover_color="#1B304B",
            command=self.add_playlist
        )
        self.add_playlist_button.pack(side="left", padx=(0, 5))

        self.edit_playlist_button = ctk.CTkButton(
            self.controls,
            text="✎  ИЗМЕНИТЬ",
            height=38,
            fg_color=PANEL_2,
            hover_color="#1B304B",
            command=self.edit_playlist
        )
        self.edit_playlist_button.pack(side="left", padx=5)

        self.delete_playlist_button = ctk.CTkButton(
            self.controls,
            text="−  УДАЛИТЬ",
            height=38,
            fg_color="#351B28",
            hover_color="#512333",
            command=self.delete_playlist
        )
        self.delete_playlist_button.pack(side="left", padx=5)

        # DOWNLOAD BUTTONS
        self.download_buttons = ctk.CTkFrame(
            self.center, fg_color="transparent"
        )
        self.download_buttons.pack(
            fill="x", padx=25, pady=(10, 10)
        )

        self.download_selected = ctk.CTkButton(
            self.download_buttons,
            text="↓  ОБНОВИТЬ ВЫБРАННЫЙ",
            height=42,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.download_selected_playlist
        )
        self.download_selected.pack(
            side="left", fill="x", expand=True, padx=(0, 5)
        )

        self.download_all = ctk.CTkButton(
            self.download_buttons,
            text="↓  ОБНОВИТЬ АВТОРА",
            height=42,
            fg_color=PANEL_2,
            hover_color="#1B304B",
            command=self.download_author
        )
        self.download_all.pack(
            side="left", fill="x", expand=True, padx=5
        )

        self.download_everything = ctk.CTkButton(
            self.download_buttons,
            text="⚡  ВСЁ",
            height=42,
            fg_color=PANEL_2,
            hover_color="#1B304B",
            command=self.download_everything
        )
        self.download_everything.pack(
            side="left", fill="x", expand=True, padx=(5, 0)
        )

        # LOG
        self.log_frame = ctk.CTkFrame(
            self, height=145, fg_color=PANEL, corner_radius=0
        )
        self.log_frame.pack(fill="x", side="bottom")
        self.log_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.log_frame,
            text="DOWNLOAD LOG",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=20, pady=(8, 2))

        self.log = ctk.CTkTextbox(
            self.log_frame,
            height=75,
            fg_color="#050C15",
            text_color="#AFC5DD",
            font=ctk.CTkFont(size=11),
            corner_radius=8
        )
        self.log.pack(
            fill="both", expand=True, padx=20, pady=(0, 10)
        )

        # MEGA MIX
        self.mega_mix_button = ctk.CTkButton(
            self,
            text="⚡  MEGA MIX  ⚡\nПеремешать всю музыку",
            height=70,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color="#0A5FC9",
            hover_color="#0873F9",
            command=self.create_mega_mix
        )
        self.mega_mix_button.place(
            relx=0.5, rely=0.89, anchor="center"
        )

    # ========================================================
    # LOG
    # ========================================================

    def log_message(self, text):
        def update():
            self.log.insert("end", text + "\n")
            self.log.see("end")
        self.after(0, update)

    def set_download_progress(self, value, text):
        """Безопасно обновляет общий прогресс из фонового потока yt-dlp."""
        value = max(0.0, min(1.0, value))
        self.after(
            0,
            lambda: (
                self.download_progress.set(value),
                self.progress_label.configure(text=text),
            ),
        )

    # ========================================================
    # AUTHORS
    # ========================================================

    def refresh_authors(self):
        for widget in self.author_list.winfo_children():
            widget.destroy()

        for author, playlists in self.config["authors"].items():
            track_count = self.get_author_track_count(author)

            button = ctk.CTkButton(
                self.author_list,
                text=(
                    f"●  {author}\n"
                    f"    {len(playlists)} плейлистов  •  "
                    f"{track_count} треков"
                ),
                height=55,
                anchor="w",
                fg_color=BLUE if author == self.current_author else "transparent",
                hover_color="#142A45",
                command=lambda a=author: self.select_author(a)
            )
            button.pack(fill="x", pady=2)

    def select_author(self, author):
        self.current_author = author
        self.current_playlist_index = None

        self.author_title.configure(text=author)

        count = len(self.config["authors"][author])
        track_count = self.get_author_track_count(author)

        self.author_subtitle.configure(
            text=f"{count} плейлист(ов)  • {track_count} скачанных треков"
        )

        self.refresh_authors()
        self.refresh_playlists()
        self.clear_tracks()

    def add_author(self):
        name = simpledialog.askstring(
            "Новый автор",
            "Введите имя автора:"
        )

        if not name:
            return

        name = name.strip()

        if not name:
            return

        if name in self.config["authors"]:
            messagebox.showwarning(
                "Ошибка",
                "Такой автор уже существует."
            )
            return

        self.config["authors"][name] = []
        save_config(self.config)
        self.select_author(name)

    def delete_author(self):
        if not self.current_author:
            return

        answer = messagebox.askyesno(
            "Удалить автора?",
            f"Удалить автора «{self.current_author}»?\n\n"
            "Папка с музыкой НЕ удаляется.\n"
            "Удалится только автор из config.json."
        )

        if not answer:
            return

        del self.config["authors"][self.current_author]
        save_config(self.config)

        self.current_author = None
        self.current_playlist_index = None

        self.author_title.configure(text="Выберите автора")
        self.author_subtitle.configure(text="")

        self.refresh_authors()
        self.refresh_playlists()
        self.clear_tracks()

    # ========================================================
    # PLAYLISTS
    # ========================================================

    def refresh_playlists(self):
        for widget in self.playlist_list.winfo_children():
            widget.destroy()

        if not self.current_author:
            return

        playlists = self.config["authors"].get(
            self.current_author, []
        )
        self.playlist_badge.configure(
            text=f"{len(playlists)} плейлист(ов)"
        )

        for index, playlist in enumerate(playlists):

            track_count = self.get_playlist_count(
                self.current_author,
                playlist["name"]
            )

            frame = ctk.CTkFrame(
                self.playlist_list,
                fg_color=(
                    "#12345A"
                    if index == self.current_playlist_index
                    else PANEL_2
                ),
                corner_radius=8
            )
            frame.pack(
                fill="x",
                padx=10,
                pady=5
            )

            button = ctk.CTkButton(
                frame,
                text=(
                    f"  {playlist['name']}\n"
                    f"  {track_count} скачанных треков"
                ),
                anchor="w",
                fg_color="transparent",
                hover_color="#193858",
                height=55,
                font=ctk.CTkFont(size=13),
                command=lambda i=index: self.select_playlist(i)
            )
            button.pack(
                side="left",
                fill="x",
                expand=True
            )

            number = ctk.CTkLabel(
                frame,
                text=f"{index + 1:02d}",
                width=45,
                text_color=TEXT_SECONDARY
            )
            number.pack(
                side="right",
                padx=10
            )

    def select_playlist(self, index):
        self.current_playlist_index = index
        self.refresh_playlists()
        self.refresh_tracks()

    # ========================================================
    # TRACKS
    # ========================================================

    def clear_tracks(self):
        for widget in self.track_list.winfo_children():
            widget.destroy()

        self.track_title.configure(text="TRACKS")
        self.track_count.configure(text="0 треков")

    def refresh_tracks(self):
        self.clear_tracks()

        if (
            not self.current_author
            or self.current_playlist_index is None
        ):
            return

        playlists = self.config["authors"][self.current_author]

        if self.current_playlist_index >= len(playlists):
            return

        playlist = playlists[self.current_playlist_index]
        name = playlist["name"]

        tracks = self.get_playlist_tracks(
            self.current_author,
            name
        )

        self.track_title.configure(text=name)
        self.track_count.configure(text=f"{len(tracks)} треков")

        if not tracks:
            label = ctk.CTkLabel(
                self.track_list,
                text="Нет скачанных треков",
                text_color=TEXT_SECONDARY
            )
            label.pack(
                anchor="w",
                padx=10,
                pady=10
            )
            return

        for index, track in enumerate(tracks, 1):
            label = ctk.CTkLabel(
                self.track_list,
                text=f"{index:03d}  {track.name}",
                anchor="w",
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=11,
                    family="Consolas"
                )
            )
            label.pack(
                fill="x",
                padx=10,
                pady=2
            )

    # ========================================================
    # PLAYLIST CRUD
    # ========================================================

    def add_playlist(self):
        if not self.current_author:
            messagebox.showwarning(
                "Автор не выбран",
                "Сначала выберите автора."
            )
            return

        name = simpledialog.askstring(
            "Новый плейлист",
            "Название плейлиста:"
        )

        if not name:
            return

        name = name.strip()

        url = simpledialog.askstring(
            "URL плейлиста",
            "Ссылка на YouTube-плейлист:"
        )

        if not url:
            return

        self.config["authors"][self.current_author].append(
            {
                "name": name,
                "url": url.strip()
            }
        )

        save_config(self.config)
        self.refresh_playlists()
        self.refresh_authors()

    def edit_playlist(self):
        if (
            not self.current_author
            or self.current_playlist_index is None
        ):
            messagebox.showwarning(
                "Плейлист не выбран",
                "Выберите плейлист."
            )
            return

        playlist = self.config["authors"][self.current_author][
            self.current_playlist_index
        ]

        name = simpledialog.askstring(
            "Изменить плейлист",
            "Название:",
            initialvalue=playlist["name"]
        )

        if not name:
            return

        url = simpledialog.askstring(
            "Изменить URL",
            "URL:",
            initialvalue=playlist["url"]
        )

        if not url:
            return

        playlist["name"] = name.strip()
        playlist["url"] = url.strip()

        save_config(self.config)

        self.refresh_playlists()
        self.refresh_authors()
        self.clear_tracks()

    def delete_playlist(self):
        if (
            not self.current_author
            or self.current_playlist_index is None
        ):
            messagebox.showwarning(
                "Плейлист не выбран",
                "Выберите плейлист."
            )
            return

        playlist = self.config["authors"][self.current_author][
            self.current_playlist_index
        ]

        answer = messagebox.askyesno(
            "Удалить плейлист?",
            f"Удалить «{playlist['name']}» из конфигурации?\n\n"
            "Файлы MP3 НЕ будут удалены."
        )

        if not answer:
            return

        del self.config["authors"][self.current_author][
            self.current_playlist_index
        ]

        self.current_playlist_index = None

        save_config(self.config)

        self.refresh_playlists()
        self.refresh_authors()
        self.clear_tracks()

    # ========================================================
    # YT-DLP
    # ========================================================

    def build_command(self, url, author, playlist):
        output = (
            MUSIC_DIR
            / author
            / playlist
            / "%(playlist_index)02d - %(title)s.%(ext)s"
        )

        return [
            str(YTDLP),
            "--js-runtimes", "deno",
            "--cookies-from-browser", "firefox",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--add-metadata",
            "--download-archive", str(ARCHIVE_FILE),
            "-o", str(output),
            url
        ]

    # ========================================================
    # DOWNLOAD ENGINE
    # ========================================================

    def download_playlist_thread(
        self,
        author,
        playlist,
        url,
        job_index=1,
        job_total=1,
    ):
        if not YTDLP.exists():
            self.log_message(
                "ERROR: yt-dlp.exe не найден."
            )
            self.set_status(
                "● ERROR",
                RED
            )
            return

        self.log_message("")
        self.log_message(
            f"▶ {author} / {playlist}"
        )
        self.set_download_progress(
            (job_index - 1) / job_total,
            f"{job_index}/{job_total}  ·  {playlist}  ·  0%",
        )

        command = self.build_command(
            url,
            author,
            playlist
        )

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=BASE_DIR
            )

            for line in process.stdout:
                line = line.strip()

                if line:
                    self.log_message(line)

                progress_match = re.search(
                    r"\[download\]\s+(\d+(?:\.\d+)?)%", line
                )
                if progress_match:
                    playlist_progress = float(progress_match.group(1)) / 100
                    overall_progress = (
                        (job_index - 1 + playlist_progress) / job_total
                    )
                    self.set_download_progress(
                        overall_progress,
                        f"{job_index}/{job_total}  ·  {playlist}  ·  "
                        f"{playlist_progress:.0%}",
                    )

                if self.stop_requested:
                    process.terminate()
                    break

            process.wait()

            if process.returncode == 0:
                self.set_download_progress(
                    job_index / job_total,
                    f"{job_index}/{job_total}  ·  Готово: {playlist}",
                )
                self.log_message(
                    f"✓ Готово: {playlist}"
                )
            else:
                self.log_message(
                    f"✗ Ошибка: {playlist}"
                )

        except Exception as e:
            self.log_message(
                f"ERROR: {e}"
            )

    def run_downloads(self, jobs):
        if self.downloading:
            messagebox.showwarning(
                "Загрузка уже идёт",
                "Дождись завершения текущей загрузки."
            )
            return

        self.downloading = True
        self.stop_requested = False
        self.set_download_progress(0, "Подготовка загрузки…")

        self.set_status(
            "● DOWNLOADING",
            CYAN
        )

        def worker():
            try:
                total = len(jobs)

                for index, (
                    author,
                    playlist,
                    url
                ) in enumerate(jobs, 1):

                    if self.stop_requested:
                        break

                    self.log_message("")
                    self.log_message(
                        f"[{index}/{total}]"
                    )

                    self.download_playlist_thread(
                        author,
                        playlist,
                        url,
                        index,
                        total,
                    )

                    self.after(
                        0,
                        self.refresh_after_download
                    )

            finally:
                self.downloading = False

                self.set_status(
                    "● READY",
                    GREEN
                )

                self.after(
                    0,
                    self.refresh_after_download
                )

                self.log_message("")
                self.log_message(
                    "════════ DOWNLOAD COMPLETE ════════"
                )
                self.set_download_progress(
                    1 if not self.stop_requested else 0,
                    "Загрузка остановлена" if self.stop_requested else "Загрузка завершена",
                )

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    def refresh_after_download(self):
        self.refresh_authors()

        if self.current_author:
            self.refresh_playlists()

            if self.current_playlist_index is not None:
                self.refresh_tracks()

            track_count = self.get_author_track_count(
                self.current_author
            )

            playlist_count = len(
                self.config["authors"][self.current_author]
            )

            self.author_subtitle.configure(
                text=(
                    f"{playlist_count} плейлист(ов)  • "
                    f"{track_count} скачанных треков"
                )
            )

    # ========================================================
    # DOWNLOAD ACTIONS
    # ========================================================

    def download_selected_playlist(self):
        if not self.current_author:
            messagebox.showwarning(
                "Автор не выбран",
                "Выберите автора."
            )
            return

        if self.current_playlist_index is None:
            messagebox.showwarning(
                "Плейлист не выбран",
                "Выберите плейлист."
            )
            return

        playlist = self.config["authors"][
            self.current_author
        ][self.current_playlist_index]

        jobs = [
            (
                self.current_author,
                playlist["name"],
                playlist["url"]
            )
        ]

        self.run_downloads(jobs)

    def download_author(self):
        if not self.current_author:
            messagebox.showwarning(
                "Автор не выбран",
                "Выберите автора."
            )
            return

        playlists = self.config["authors"][
            self.current_author
        ]

        if not playlists:
            messagebox.showinfo(
                "Нет плейлистов",
                "У этого автора нет плейлистов."
            )
            return

        jobs = [
            (
                self.current_author,
                pl["name"],
                pl["url"]
            )
            for pl in playlists
        ]

        self.run_downloads(jobs)

    def download_everything(self):
        jobs = []

        for author, playlists in self.config[
            "authors"
        ].items():
            for playlist in playlists:
                jobs.append(
                    (
                        author,
                        playlist["name"],
                        playlist["url"]
                    )
                )

        if not jobs:
            messagebox.showinfo(
                "Нечего скачивать",
                "В конфигурации нет плейлистов."
            )
            return

        answer = messagebox.askyesno(
            "Обновить всё?",
            f"Будет проверено плейлистов: {len(jobs)}\n\n"
            "Уже скачанные треки yt-dlp пропустит."
        )

        if answer:
            self.run_downloads(jobs)

    # ========================================================
    # STATUS
    # ========================================================

    def set_status(self, text, color):
        self.after(
            0,
            lambda: self.status_label.configure(
                text=text,
                text_color=color
            )
        )

    # ========================================================
    # MEGA MIX
    # ========================================================

    def create_mega_mix(self):
        if self.downloading:
            messagebox.showwarning(
                "Загрузка идёт",
                "Дождись окончания загрузки."
            )
            return

        tracks = []

        for root, dirs, files in os.walk(MUSIC_DIR):
            root_path = Path(root)

            # Не включаем уже созданный Mega Mix,
            # чтобы он не попал сам в себя при следующем запуске.
            if (
                root_path == MEGA_MIX_DIR
                or MEGA_MIX_DIR in root_path.parents
            ):
                continue

            for file in files:
                if file.lower().endswith(".mp3"):
                    tracks.append(
                        root_path / file
                    )

        if not tracks:
            messagebox.showinfo(
                "Нет музыки",
                "В папке Music нет MP3-файлов."
            )
            return

        answer = messagebox.askyesno(
            "Создать Mega Mix?",
            f"Найдено треков: {len(tracks)}\n\n"
            "Старый Mega Mix будет пересоздан."
        )

        if not answer:
            return

        threading.Thread(
            target=self.mega_mix_worker,
            args=(tracks,),
            daemon=True
        ).start()

    def mega_mix_worker(self, tracks):
        self.set_status(
            "● CREATING MIX",
            CYAN
        )

        self.log_message("")
        self.log_message(
            "⚡ Создание MEGA MIX..."
        )

        try:
            # Удаляем старый Mega Mix.
            if MEGA_MIX_DIR.exists():
                shutil.rmtree(MEGA_MIX_DIR)

            MEGA_MIX_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            # Перемешиваем все найденные треки.
            random.shuffle(tracks)

            total = len(tracks)

            for index, source in enumerate(
                tracks,
                1
            ):
                destination = (
                    MEGA_MIX_DIR
                    / f"{index:04d} - "
                      f"{source.stem}{source.suffix}"
                )

                # Копируем файл, оригинал остаётся
                # в своей папке автора/плейлиста.
                shutil.copy2(
                    source,
                    destination
                )

                if (
                    index % 25 == 0
                    or index == total
                ):
                    self.log_message(
                        f"Mega Mix: "
                        f"{index}/{total}"
                    )

            self.log_message(
                f"✓ Mega Mix создан: {total} треков"
            )

            self.after(
                0,
                lambda: messagebox.showinfo(
                    "Mega Mix готов",
                    f"Создано {total} треков.\n\n"
                    f"Папка:\n{MEGA_MIX_DIR}"
                )
            )

        except Exception as e:
            self.log_message(
                f"✗ Mega Mix error: {e}"
            )

            self.after(
                0,
                lambda: messagebox.showerror(
                    "Ошибка Mega Mix",
                    str(e)
                )
            )

        finally:
            self.set_status(
                "● READY",
                GREEN
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    app = MusicLoader()
    app.mainloop()
