import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox  # <-- Importar messagebox desde tkinter
from yt_dlp import YoutubeDL
import imageio_ffmpeg

PLATAFORMAS = {
    "YouTube": ['youtube.com', 'youtu.be'],
    "Instagram": ['instagram.com'],
    "Pinterest": ['pinterest.com'],
    "X (Twitter)": ['twitter.com', 'x.com'],
}

def hook_progreso(d):
    if d['status'] == 'downloading':
        porcentaje = d.get('_percent_str', '0.0%').strip().replace('%', '')
        try:
            progreso['value'] = float(porcentaje)
            app.update_idletasks()
        except:
            pass
    elif d['status'] == 'finished':
        progreso['value'] = 100
        app.update_idletasks()

def descargar():
    url = url_entry.get().strip()
    plataforma = plataforma_var.get()
    if not url:
        messagebox.showerror("Error", "Ingresá una URL", parent=app)
        return

    dominios_validos = PLATAFORMAS.get(plataforma, [])
    if not any(dominio in url.lower() for dominio in dominios_validos):
        messagebox.showerror(
            "Error",
            f"La URL no coincide con la plataforma {plataforma}.",
            parent=app
        )
        return

    carpeta = carpeta_path.get()
    if not carpeta:
        messagebox.showerror("Error", "Elegí una carpeta para guardar", parent=app)
        return

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    progreso['value'] = 0  # Resetear barra
    app.update_idletasks()

    formato = formato_var.get()
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
            'progress_hooks': [hook_progreso],
        }
    else:
        ydl_opts = {
            'format': 'best[ext=mp4][vcodec!=av01]+bestaudio[ext=m4a]/best[ext=mp4]',
            'ffmpeg_location': ffmpeg_path,
            'merge_output_format': 'mp4',
            'outtmpl': carpeta + '/%(title)s.%(ext)s',
            'progress_hooks': [hook_progreso],
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "Descarga completada", parent=app)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descargar:\n{e}", parent=app)

def elegir_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_path.set(carpeta)

app = tb.Window(themename="darkly")
app.title("Downloader Multimedia")

frame_url = tb.Frame(app)
frame_url.pack(pady=10, padx=10, fill="x")

tb.Label(frame_url, text="URL del video:").pack(anchor='w')
url_entry = tb.Entry(frame_url, width=55)
url_entry.pack(pady=3, fill="x")

tb.Label(frame_url, text="Plataforma:").pack(anchor='w', pady=(10,0))
plataforma_var = tb.StringVar(value="YouTube")
plataformas_cb = tb.Combobox(frame_url, textvariable=plataforma_var, state="readonly",
                             values=list(PLATAFORMAS.keys()), width=20)
plataformas_cb.pack(pady=3, anchor='w')

frame_formato = tb.Frame(app)
frame_formato.pack(pady=10, padx=10, fill="x")

tb.Label(frame_formato, text="Formato:").pack(anchor='w')
formato_var = tb.StringVar(value="mp4")
tb.Radiobutton(frame_formato, text="MP4", variable=formato_var, value="mp4").pack(side='left', padx=10)
tb.Radiobutton(frame_formato, text="MP3", variable=formato_var, value="mp3").pack(side='left', padx=10)

frame_carpeta = tb.Frame(app)
frame_carpeta.pack(pady=10, padx=10, fill="x")

tb.Label(frame_carpeta, text="Carpeta destino:").pack(side='left', padx=5)
carpeta_path = tb.StringVar()
tb.Entry(frame_carpeta, textvariable=carpeta_path, width=40, state="readonly").pack(side='left', padx=5)
tb.Button(frame_carpeta, text="Elegir...", command=elegir_carpeta).pack(side='left', padx=5)

progreso = tb.Progressbar(app, length=440, mode='determinate')
progreso.pack(pady=15)

tb.Button(app, text="Descargar", command=descargar, bootstyle="success").pack(pady=10)

app.mainloop()
