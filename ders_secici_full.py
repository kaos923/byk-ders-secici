import tkinter as tk
from tkinter import messagebox
import os, sys, subprocess, urllib.request

# ================== GITHUB ==================
GITHUB_RAW = "https://raw.githubusercontent.com/kaos923/byk-ders-secici/main/"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AYAR_DOSYA = os.path.join(BASE_DIR, "ayarlar.txt")
VERSION_DOSYA = os.path.join(BASE_DIR, "version.txt")

dersler = [
    ("Türkçe", "Turkce.pdf", "turkce.png"),
    ("Matematik", "Matematik.pdf", "matematik.png"),
    ("İngilizce", "Ingilizce.pdf", "ingilizce.png"),
    ("Fen", "Fen.pdf", "fen.png"),
    ("Sosyal", "Sosyal.pdf", "sosyal.png"),
    ("Müzik", "Muzik.pdf", "muzik.png"),
    ("Din", "Din.pdf", "din.png"),
]

# ================== VERSION OKU ==================
def yerel_surum_oku():
    if not os.path.exists(VERSION_DOSYA):
        return "0.0"
    with open(VERSION_DOSYA, "r", encoding="utf-8") as f:
        return f.read().strip()

MEVCUT_SURUM = yerel_surum_oku()

# ================== AYAR OKU / YAZ ==================
def ayar_yukle():
    if not os.path.exists(AYAR_DOSYA):
        return "?", "?"
    with open(AYAR_DOSYA, "r", encoding="utf-8") as f:
        s = f.read().splitlines()
        return s[0], s[1]

def ayar_kaydet(sinif, sube):
    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        f.write(sinif + "\n" + sube)

# ================== PDF AÇ ==================
def pdf_ac(pdf):
    yol = os.path.join(BASE_DIR, pdf)
    if not os.path.exists(yol):
        messagebox.showerror("Hata", f"{pdf} bulunamadı!")
        return
    if sys.platform.startswith("win"):
        os.startfile(yol)
    else:
        subprocess.Popen(["xdg-open", yol])

# ================== GÜNCELLE ==================
def guncelle():
    try:
        with urllib.request.urlopen(GITHUB_RAW + "version.txt", timeout=5) as r:
            yeni_surum = r.read().decode().strip()

        if yeni_surum == MEVCUT_SURUM:
            messagebox.showinfo("Güncelleme", "Zaten en güncel sürüm.")
            return

        if not messagebox.askyesno(
            "Güncelleme Var",
            f"Yeni sürüm: {yeni_surum}\nGüncellensin mi?"
        ):
            return

        with urllib.request.urlopen(GITHUB_RAW + "ders_secici_full.py") as r:
            yeni_kod = r.read().decode("utf-8")

        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(yeni_kod)

        with open(VERSION_DOSYA, "w", encoding="utf-8") as f:
            f.write(yeni_surum)

        messagebox.showinfo(
            "Güncellendi",
            "Güncelleme tamamlandı.\nProgramı yeniden başlat."
        )

    except Exception as e:
        messagebox.showerror("Hata", f"Güncelleme başarısız:\n{e}")

# ================== AYARLAR ==================
def ayarlar_pencere():
    win = tk.Toplevel(root)
    win.title("Ayarlar")
    win.geometry("300x260")

    tk.Label(win, text="Sınıf").pack(pady=5)
    sinif_e = tk.Entry(win)
    sinif_e.insert(0, sinif)
    sinif_e.pack()

    tk.Label(win, text="Şube").pack(pady=5)
    sube_e = tk.Entry(win)
    sube_e.insert(0, sube)
    sube_e.pack()

    def kaydet():
        global sinif, sube
        sinif = sinif_e.get()
        sube = sube_e.get()
        ayar_kaydet(sinif, sube)
        baslik.config(text=f"📚 BYK Ders Kitaplığı – {sinif}/{sube} (v{MEVCUT_SURUM})")
        win.destroy()

    tk.Button(win, text="💾 Kaydet", command=kaydet).pack(pady=8)
    tk.Button(win, text="🔄 Güncellemeleri Kontrol Et", command=guncelle).pack(pady=5)

# ================== ANA PENCERE ==================
sinif, sube = ayar_yukle()

root = tk.Tk()
root.title("BYK Ders Kitaplığı")
root.geometry("1200x700")

# ===== ARKA PLAN =====
bg_image = tk.PhotoImage(file=os.path.join(BASE_DIR, "background.png"))

bg_canvas = tk.Canvas(root, width=1200, height=700, highlightthickness=0)
bg_canvas.pack(fill="both", expand=True)
bg_canvas.create_image(0, 0, image=bg_image, anchor="nw")

baslik = tk.Label(
    bg_canvas,
    text=f"📚 BYK Ders Kitaplığı – {sinif}/{sube} (v{MEVCUT_SURUM})",
    bg="#000000",
    fg="white",
    font=("Segoe UI", 20, "bold")
)
baslik.pack(pady=10)

tk.Button(
    bg_canvas,
    text="⚙ Ayarlar",
    command=ayarlar_pencere,
    bg="#89b4fa",
    relief="flat"
).pack(pady=5)

# ================== SCROLL ==================
canvas = tk.Canvas(bg_canvas, bg="", highlightthickness=0)
scroll = tk.Scrollbar(bg_canvas, orient="vertical", command=canvas.yview)
icerik = tk.Frame(canvas, bg="#1e1e2e")

icerik.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=icerik, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
scroll.pack(side="right", fill="y")

resimler = []

for i, (ad, pdf, resim) in enumerate(dersler):
    kart = tk.Frame(icerik, bg="#313244", padx=10, pady=10)
    kart.grid(row=i//4, column=i%4, padx=25, pady=25)

    img_yol = os.path.join(BASE_DIR, resim)
    img = tk.PhotoImage(file=img_yol) if os.path.exists(img_yol) else tk.PhotoImage(width=200, height=260)
    resimler.append(img)

    tk.Button(
        kart,
        image=img,
        command=lambda p=pdf: pdf_ac(p),
        bd=0,
        bg="#313244",
        activebackground="#45475a"
    ).pack()

    tk.Label(
        kart,
        text=ad,
        bg="#313244",
        fg="white",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=5)

root.mainloop()
