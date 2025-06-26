import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL
import imageio_ffmpeg

def descargar():
    url = url_entry.get()
    formato = formato_var.get()
    if not url:
        messagebox.showerror("Error", "Ingresá una URL")
        return

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    ydl_opts = {}
    if formato == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,
            'outtmpl': '%(title)s.%(ext)s',
        }
    else:  # mp4
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'ffmpeg_location': ffmpeg_path,
            'outtmpl': '%(title)s.%(ext)s',
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "Descarga completada")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descargar:\n{e}")

root = tk.Tk()
root.title("YouTube Downloader")

tk.Label(root, text="URL de YouTube:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

formato_var = tk.StringVar(value="mp4")
tk.Radiobutton(root, text="MP4", variable=formato_var, value="mp4").pack()
tk.Radiobutton(root, text="MP3", variable=formato_var, value="mp3").pack()

tk.Button(root, text="Descargar", command=descargar).pack()

root.mainloop()
