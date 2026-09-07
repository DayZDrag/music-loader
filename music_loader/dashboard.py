"""Построение неоновой панели управления Music Loader."""

import customtkinter as ctk

from .theme import BLUE, BLUE_HOVER, CYAN, GREEN, PANEL, PANEL_2, TEXT, TEXT_SECONDARY


SURFACE = "#09172A"
SURFACE_RAISED = "#0D2038"
OUTLINE = "#1B3556"
VIOLET = "#9B3DFF"
VIOLET_HOVER = "#7D24E8"
PINK = "#ED4CCB"


def label(parent, text, size=13, weight="normal", color=TEXT, **kwargs):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=size, weight=weight),
        text_color=color,
        **kwargs,
    )


def build_dashboard(app):
    """Создаёт UI и оставляет привычные поля приложения доступными."""
    app.header = ctk.CTkFrame(app, height=78, fg_color="#071326", corner_radius=0)
    app.header.pack(fill="x")
    app.header.pack_propagate(False)

    brand = ctk.CTkFrame(app.header, fg_color="transparent")
    brand.pack(side="left", padx=(25, 38), pady=13)
    label(brand, "ϟ", size=38, weight="bold", color=VIOLET).pack(side="left", padx=(0, 10))
    brand_text = ctk.CTkFrame(brand, fg_color="transparent")
    brand_text.pack(side="left")
    label(brand_text, "MEGA MIX", size=19, weight="bold").pack(anchor="w")
    label(brand_text, "MUSIC LOADER", size=10, weight="bold", color=TEXT_SECONDARY).pack(anchor="w")

    app.search_input = ctk.CTkEntry(
        app.header,
        width=430,
        height=42,
        corner_radius=13,
        fg_color="#0B1A30",
        border_color=OUTLINE,
        text_color=TEXT,
        placeholder_text="⌕   Поиск автора или плейлиста...",
        placeholder_text_color="#607594",
    )
    app.search_input.pack(side="left", fill="x", expand=True, padx=(0, 20), pady=18)

    app.status_label = ctk.CTkLabel(
        app.header,
        text="●  ГОТОВ К РАБОТЕ",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color=GREEN,
        fg_color="#10283A",
        corner_radius=14,
        padx=15,
        pady=8,
    )
    app.status_label.pack(side="right", padx=(8, 22))

    app.main = ctk.CTkFrame(app, fg_color="#061224", corner_radius=0)
    app.main.pack(fill="both", expand=True, padx=18, pady=(0, 10))

    app.author_panel = ctk.CTkFrame(
        app.main, width=262, fg_color=SURFACE, border_color=OUTLINE,
        border_width=1, corner_radius=18,
    )
    app.author_panel.pack(side="left", fill="y", pady=10)
    app.author_panel.pack_propagate(False)
    label(app.author_panel, "АВТОРЫ", size=13, weight="bold", color="#B7A7E8").pack(
        anchor="w", padx=18, pady=(18, 8)
    )
    app.author_list = ctk.CTkScrollableFrame(
        app.author_panel, fg_color="transparent", scrollbar_button_color="#294260",
        scrollbar_button_hover_color=VIOLET,
    )
    app.author_list.pack(fill="both", expand=True, padx=10)

    app.add_author_button = ctk.CTkButton(
        app.author_panel, text="＋  ДОБАВИТЬ АВТОРА", height=38, corner_radius=11,
        fg_color=VIOLET, hover_color=VIOLET_HOVER, font=ctk.CTkFont(size=11, weight="bold"),
        command=app.add_author,
    )
    app.add_author_button.pack(fill="x", padx=15, pady=(10, 6))
    app.delete_author_button = ctk.CTkButton(
        app.author_panel, text="−  УДАЛИТЬ АВТОРА", height=34, corner_radius=11,
        fg_color="#13243A", hover_color="#203954", text_color="#B9C6D9",
        font=ctk.CTkFont(size=10, weight="bold"), command=app.delete_author,
    )
    app.delete_author_button.pack(fill="x", padx=15, pady=(0, 15))

    app.center = ctk.CTkFrame(app.main, fg_color="transparent", corner_radius=0)
    app.center.pack(side="left", fill="both", expand=True, padx=(18, 0), pady=10)

    hero = ctk.CTkFrame(app.center, height=132, fg_color="#111A42", corner_radius=18)
    hero.pack(fill="x", pady=(0, 10))
    hero.pack_propagate(False)
    glow = ctk.CTkLabel(
        hero, text="♫", width=82, height=82, corner_radius=41, fg_color="#261D63",
        text_color=VIOLET, font=ctk.CTkFont(size=41, weight="bold"),
    )
    glow.place(x=24, y=25)
    hero_text = ctk.CTkFrame(hero, fg_color="transparent")
    hero_text.place(x=126, y=23)
    app.author_title = label(hero_text, "Выберите автора", size=27, weight="bold")
    app.author_title.pack(anchor="w")
    app.author_subtitle = label(hero_text, "Выберите автора слева, чтобы увидеть плейлисты", size=12, color="#91A4C7")
    app.author_subtitle.pack(anchor="w", pady=(5, 0))
    label(hero, "♫   ✧   ♫", size=25, weight="bold", color=PINK).place(relx=0.95, rely=0.49, anchor="e")

    playlist_card = ctk.CTkFrame(app.center, fg_color=SURFACE, border_color=OUTLINE, border_width=1, corner_radius=18)
    playlist_card.pack(fill="both", expand=True, pady=(0, 10))
    playlist_header = ctk.CTkFrame(playlist_card, height=43, fg_color="transparent")
    playlist_header.pack(fill="x", padx=16, pady=(7, 0))
    label(playlist_header, "ПЛЕЙЛИСТЫ", size=13, weight="bold", color="#C9B8F7").pack(side="left")
    app.playlist_badge = label(playlist_header, "0 плейлистов", size=10, weight="bold", color="#A5B7D4", fg_color="#11233B", corner_radius=12, padx=10, pady=5)
    app.playlist_badge.pack(side="right")
    app.playlist_list = ctk.CTkScrollableFrame(
        playlist_card, fg_color="transparent", scrollbar_button_color="#294260",
        scrollbar_button_hover_color=VIOLET,
    )
    app.playlist_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    tracks_card = ctk.CTkFrame(app.center, height=155, fg_color=SURFACE, border_color=OUTLINE, border_width=1, corner_radius=18)
    tracks_card.pack(fill="x", pady=(0, 10))
    tracks_card.pack_propagate(False)
    app.track_header = ctk.CTkFrame(tracks_card, height=34, fg_color="transparent")
    app.track_header.pack(fill="x", padx=16, pady=(8, 0))
    app.track_title = label(app.track_header, "ТРЕКИ", size=12, weight="bold", color="#C9B8F7")
    app.track_title.pack(side="left")
    app.track_count = label(app.track_header, "0 треков", size=10, weight="bold", color="#A5B7D4", fg_color="#11233B", corner_radius=12, padx=10, pady=5)
    app.track_count.pack(side="right")
    app.track_list = ctk.CTkScrollableFrame(
        tracks_card, height=104, fg_color="#08182C", corner_radius=12,
        scrollbar_button_color="#294260", scrollbar_button_hover_color=VIOLET,
    )
    app.track_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    app.controls = ctk.CTkFrame(app.center, fg_color="transparent")
    app.controls.pack(fill="x", pady=(0, 7))
    for text, command, color, hover in [
        ("＋  ДОБАВИТЬ", app.add_playlist, "#142842", "#203D60"),
        ("⌕  ИЗМЕНИТЬ", app.edit_playlist, "#142842", "#203D60"),
        ("−  УДАЛИТЬ", app.delete_playlist, "#2B1933", "#472447"),
    ]:
        button = ctk.CTkButton(app.controls, text=text, height=34, corner_radius=10, fg_color=color, hover_color=hover, font=ctk.CTkFont(size=10, weight="bold"), command=command)
        button.pack(side="left", padx=(0, 6))
    app.download_buttons = ctk.CTkFrame(app.center, fg_color="transparent")
    app.download_buttons.pack(fill="x", pady=(0, 8))
    app.download_selected = ctk.CTkButton(app.download_buttons, text="↓  ОБНОВИТЬ ВЫБРАННЫЙ", height=42, corner_radius=12, fg_color=VIOLET, hover_color=VIOLET_HOVER, font=ctk.CTkFont(size=11, weight="bold"), command=app.download_selected_playlist)
    app.download_selected.pack(side="left", fill="x", expand=True, padx=(0, 6))
    app.download_all = ctk.CTkButton(app.download_buttons, text="↓  ОБНОВИТЬ АВТОРА", height=42, corner_radius=12, fg_color="#142842", hover_color="#203D60", font=ctk.CTkFont(size=10, weight="bold"), command=app.download_author)
    app.download_all.pack(side="left", fill="x", expand=True, padx=6)
    app.download_everything = ctk.CTkButton(app.download_buttons, text="ϟ  ВСЁ СРАЗУ", height=42, corner_radius=12, fg_color=BLUE, hover_color=BLUE_HOVER, font=ctk.CTkFont(size=10, weight="bold"), command=app.download_everything)
    app.download_everything.pack(side="left", fill="x", expand=True, padx=(6, 0))

    mix = ctk.CTkFrame(app.center, height=54, fg_color="#0B1E37", corner_radius=14)
    mix.pack(fill="x")
    mix.pack_propagate(False)
    label(mix, "⚡  MEGA MIX", size=13, weight="bold", color="#D3C2FF").pack(side="left", padx=(17, 5))
    label(mix, "Перемешать всю локальную музыку", size=11, color=TEXT_SECONDARY).pack(side="left")
    app.mega_mix_button = ctk.CTkButton(mix, text="СОЗДАТЬ МИКС  ▶", width=150, height=32, corner_radius=10, fg_color="#243AFF", hover_color="#3B2CD3", font=ctk.CTkFont(size=10, weight="bold"), command=app.create_mega_mix)
    app.mega_mix_button.pack(side="right", padx=11, pady=10)

    app.log_frame = ctk.CTkFrame(app, height=164, fg_color="#071326", border_color=OUTLINE, border_width=1, corner_radius=16)
    app.log_frame.pack(fill="x", padx=18, pady=(0, 15))
    app.log_frame.pack_propagate(False)
    log_header = ctk.CTkFrame(app.log_frame, height=38, fg_color="transparent")
    log_header.pack(fill="x", padx=15, pady=(7, 0))
    label(log_header, "DOWNLOAD CONSOLE", size=11, weight="bold", color="#C9B8F7").pack(side="left")
    app.progress_label = label(log_header, "Ожидание загрузки", size=10, color="#90A6C8")
    app.progress_label.pack(side="right")
    app.download_progress = ctk.CTkProgressBar(app.log_frame, height=7, corner_radius=4, progress_color=VIOLET, fg_color="#142842")
    app.download_progress.set(0)
    app.download_progress.pack(fill="x", padx=15, pady=(0, 7))
    app.log = ctk.CTkTextbox(app.log_frame, height=82, fg_color="#050E1D", text_color="#B6C9E5", font=ctk.CTkFont(size=11, family="Consolas"), corner_radius=10, border_width=1, border_color="#102846")
    app.log.pack(fill="both", expand=True, padx=15, pady=(0, 10))
