import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import threading


wnd = tk.Tk()
wnd.title("Video İndirme Uygulaması")
wnd.attributes("-fullscreen", True)
wnd.configure(bg="#222")


def toggle_fullscreen(event=None):
    wnd.attributes("-fullscreen", not wnd.attributes("-fullscreen"))

wnd.bind("<F11>", toggle_fullscreen)
wnd.bind("<Escape>", lambda e: wnd.attributes("-fullscreen", False))


url_var = tk.StringVar()
status_var = tk.StringVar(value="")


style = ttk.Style()
try:
    style.theme_use("clam")
except:
    pass
style.configure("TFrame", background="#222")
style.configure("TLabel", background="#222", foreground="#eee", font=("Segoe UI", 12))
style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
style.configure("TEntry", fieldbackground="#111", foreground="#eee")
style.configure("TButton", font=("Segoe UI", 12, "bold"))


root_frame = ttk.Frame(wnd, padding=24, style="TFrame")
root_frame.place(relx=0.5, rely=0.5, anchor="center")

title_lbl = ttk.Label(root_frame, text="YouTube Video İndirici", style="Header.TLabel")
title_lbl.grid(row=0, column=0, columnspan=2, pady=(0, 16))

url_lbl = ttk.Label(root_frame, text="URL:")
url_lbl.grid(row=1, column=0, sticky="e", padx=(0, 8))

url_entry = ttk.Entry(root_frame, width=46, textvariable=url_var)
url_entry.grid(row=1, column=1, sticky="we")

status_lbl = ttk.Label(root_frame, textvariable=status_var)
status_lbl.grid(row=2, column=0, columnspan=2, pady=(12, 4))

btn_frame = ttk.Frame(root_frame, style="TFrame")
btn_frame.grid(row=3, column=0, columnspan=2, pady=(12, 0))

def indir():
    url = url_var.get().strip()
    if not url:
        messagebox.showwarning("Uyarı", "Lütfen bir YouTube URL'si giriniz.")
        return

    indirme_butonu.config(state="disabled")
    status_var.set("İndiriliyor... Lütfen bekleyin.")
    wnd.update_idletasks()

    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()  
        status_var.set("İndirme tamamlandı ✅")
    except Exception as e:
        status_var.set("")
        messagebox.showerror("Hata", f"URL indirilemedi. Lütfen geçerli bir YouTube bağlantısı deneyin.\n\nDetay: {e}")
    finally:
        indirme_butonu.config(state="normal")

def indir_baslat(*_):
   
    threading.Thread(target=indir, daemon=True).start()

indirme_butonu = ttk.Button(btn_frame, text="İndir", command=indir_baslat)
indirme_butonu.grid(row=0, column=0, padx=6)

kapat_butonu = ttk.Button(btn_frame, text="Kapat", command=wnd.destroy)
kapat_butonu.grid(row=0, column=1, padx=6)


url_entry.bind("<Return>", indir_baslat)


root_frame.columnconfigure(1, weight=1)

url_entry.focus()

wnd.mainloop()
