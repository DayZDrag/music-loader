@echo off
chcp 65001 >nul
cd /d "%~dp0"

REM ========================================
REM        Загрузчик музыки с YouTube
REM ========================================

REM ----------------------------------------
REM Уже скачанные треки не скачиваются повторно
REM Новые треки автоматически докачиваются
REM ----------------------------------------

set "YTDLP=.\yt-dlp.exe --js-runtimes deno --cookies-from-browser firefox -x --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata --download-archive "downloaded.txt""

REM ========================================
REM БЕЗ АВТОРА
REM ========================================

REM Аниме девочки
%YTDLP% -o "Music\Без автора\Аниме девочки\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=91frwuPB7qg&list=PL7zP0eszV-v-fGzvjwr6m5u5Zmgdiix20"

REM Много часавой трип
%YTDLP% -o "Music\Без автора\Много часавой трип\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=XPCinyyrMAg&list=PL7zP0eszV-v_BqKkbh4mISXN0YheSgfAF"

REM Проклятые сонги
%YTDLP% -o "Music\Без автора\Проклятые сонги\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=tM38NPwLsa0&list=PL7zP0eszV-v9blEUzmLl92ja_uX6FTeUD"

REM уголок моего сознания (музыка)
%YTDLP% -o "Music\Без автора\уголок моего сознания (музыка)\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=3Ia1ZEmNMfk&list=PL7zP0eszV-v8S_Tb6DE8Vh2MgY3XUnwuN&index=1"

REM чиловый сонг
%YTDLP% -o "Music\Без автора\чиловый сонг\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=7-smjiy5NSA&list=PL7zP0eszV-v9pA10SrCvv04Cuxps3V5Jd"

REM Неповторимые произведения единые зависимостью к ним
%YTDLP% -o "Music\Без автора\Неповторимые произведения единые зависимостью к ним\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=ciBAlRKs7WE&list=PL7zP0eszV-v89-s08NgRVtaHBcWP5sLtF"

REM Музяка
%YTDLP% -o "Music\Без автора\Музяка\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=W5Sq71VTJ9Q&list=PL7zP0eszV-v_0F10-JWBloKyVuZ0wJyXj"


REM ========================================
REM POMIPOMI
REM ========================================

REM вкусный pomipomi
%YTDLP% -o "Music\pomipomi\вкусный pomipomi\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=U8lJbinCsWI&list=PLUi7NEa3SQxA"


REM ========================================
REM MIATRISS
REM ========================================

REM MiatriSs
%YTDLP% -o "Music\MiatriSs\MiatriSs\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=KJrsNbVvYlE&list=PL7zP0eszV-v9sznyX17U84Q-MeRWcwJ3X"


REM ========================================
REM H2M BIRDMAN
REM ========================================

REM H2M birdman
%YTDLP% -o "Music\H2M birdman\H2M birdman\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=wIB7exGmL2A&list=PL7zP0eszV-v85eRL8j3QfNvIbuGugtDUn"


REM ========================================
REM GLYDE
REM ========================================

REM Glyde
%YTDLP% -o "Music\Glyde\Glyde\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=ijSIFzHTnfg&list=PL7zP0eszV-v9EXV16tcVpFaPR8UKm7-dZ"


REM ========================================
REM HOTLINE MIAMI
REM ========================================

REM Hotline Miami Soundtracks
%YTDLP% -o "Music\Hotline Miami Soundtracks\Hotline Miami Soundtracks\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=QXkSYSPTpj4&list=PLk2QSht0RAUEMduNgBzaW3RrQVuokzkLE"


REM ========================================
REM ПОЛЬМИХАН
REM ========================================

REM польмихан
%YTDLP% -o "Music\польмихан\польмихан\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=eA9nx32LyPc&list=PLlk05udgFTA9M3vvC_iR2vspIGJ_ZZG7j"

REM польмихан вставай
%YTDLP% -o "Music\польмихан\польмихан вставай\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=eA9nx32LyPc&list=OLAK5uy_l_N_aNe8N6giFgnUOmObMTtaDXsCLlk7k"

REM польмихан фителёк
%YTDLP% -o "Music\польмихан\польмихан фителёк\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=PwQBiee-PMk&list=OLAK5uy_kk0XtD--oMInkD7fWeAioch0YKeVLNdGc"

REM польмихан промежуток
%YTDLP% -o "Music\польмихан\польмихан промежуток\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=2qEqpBm0JJU&list=OLAK5uy_mN6ytr7kNy9ekCHY6s4NRJOxtiZkFDVc0"

REM польмихан формальности
%YTDLP% -o "Music\польмихан\польмихан формальности\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=Qi1T-rfgga4&list=OLAK5uy_nNPMrQfXnhroK0GyvhzsJfvM-23Fr93rA"

REM польмихан свет мрака
%YTDLP% -o "Music\польмихан\польмихан свет мрака\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=e4a1lfjlfsk&list=OLAK5uy_mG0HjofMsYCFdk3ICSTvSjrz0cB8489Uw"

REM польмихан центр своей реальности
%YTDLP% -o "Music\польмихан\польмихан центр своей реальности\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=brQAZqJ_Fek&list=OLAK5uy_kX_bCw_4qO4PKRzpfd_ScB548RXhdyjs8"


REM ========================================
REM POMIPOMI
REM ========================================

REM Pomipomi
%YTDLP% -o "Music\Pomipomi\Pomipomi\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=fHHB6XtjTcg&list=PLstjVgPXwnbJ0uS2vmD3FJJIPQE7sAO3R"

REM Pomipomi 2 плейлист
%YTDLP% -o "Music\Pomipomi\Pomipomi 2 плейлист\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=q_vwmeIIfW8&list=PLstjVgPXwnbKxsGeL8S-FrK7pxdBfeUlQ"


REM ========================================
REM GEOXOR
REM ========================================

REM Geoxor
%YTDLP% -o "Music\Geoxor\Geoxor\%%(playlist_index)02d - %%(title)s.%%(ext)s" "https://www.youtube.com/watch?v=qDztrDlW1RE&list=PLJDb8my65gWwlSlcTvzZMuCeWlzBySIec"


REM ========================================
REM ГОТОВО
REM ========================================

echo.
echo ========================================
echo        Загрузка завершена!
echo ========================================
echo.

pause