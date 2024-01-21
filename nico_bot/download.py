from typing import Optional

from yt_dlp import YoutubeDL

from nico_bot import env


def download(url: str, dir_path: str, username: Optional[str] = None, password: Optional[str] = None):
    username = env.get(username, "NICO_USER_NAME")
    password = env.get(password, "NICO_PASSWORD")
    with YoutubeDL(params={"username": username,
                           "password": password,
                           "outtmpl": f"{dir_path}/%(title)s.%(ext)s",
                           }) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        download_path = ydl.prepare_filename(info_dict)
        ydl.download([url])
    return download_path
