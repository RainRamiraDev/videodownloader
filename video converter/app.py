import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, LEFT
from yt_dlp import YoutubeDL
import imageio_ffmpeg

def descargar():
    url = url_entry.get()
    formato = formato_var.get()
    if not url:
        messagebox.showerror("Error", "Ingresá una URL")
        return

    carpeta = carpeta_path.get()
    if not carpeta:
        messagebox.showerror("Error", "Elegí una carpeta para guardar")
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
            'outtmpl': carpeta + '/%(title)s.%(ext)s',
        }
    else:
        ydl_opts = {
            # Evitar video AV1 y audio Opus para máxima compatibilidad
            'format': 'best[ext=mp4][vcodec!=av01]+bestaudio[ext=m4a]/best[ext=mp4]',
            'ffmpeg_location': ffmpeg_path,
            'merge_output_format': 'mp4',
            'outtmpl': carpeta + '/%(title)s.%(ext)s',
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "Descarga completada")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descargar:\n{e}")

def elegir_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_path.set(carpeta)

app = tb.Window(themename="darkly")  # tema oscuro con ttkbootstrap
app.title("YouTube Downloader")

tb.Label(app, text="URL de YouTube:").pack(pady=5)
url_entry = tb.Entry(app, width=50)
url_entry.pack(pady=5)

tb.Label(app, text="Formato:").pack(pady=5)
formato_var = tb.StringVar(value="mp4")
tb.Radiobutton(app, text="MP4", variable=formato_var, value="mp4").pack()
tb.Radiobutton(app, text="MP3", variable=formato_var, value="mp3").pack()

carpeta_path = tb.StringVar()
frame_carpeta = tb.Frame(app)
frame_carpeta.pack(pady=10)

tb.Label(frame_carpeta, text="Carpeta destino:").pack(side=LEFT, padx=5)
tb.Entry(frame_carpeta, textvariable=carpeta_path, width=35, state="readonly").pack(side=LEFT, padx=5)
tb.Button(frame_carpeta, text="Elegir...", command=elegir_carpeta).pack(side=LEFT)

tb.Button(app, text="Descargar", command=descargar).pack(pady=20)

app.mainloop()
