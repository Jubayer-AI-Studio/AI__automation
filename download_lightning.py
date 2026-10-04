import yt_dlp

ydl_opts = {
    "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
    "outtmpl": "temp/movie_clips/thor_charges_ironman.%(ext)s",
    "quiet": False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["https://www.youtube.com/watch?v=ipQq8111IW4"])
