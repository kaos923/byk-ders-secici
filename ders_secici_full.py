import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os, sys, subprocess, urllib.request, traceback

# ================== SABİTLER ==================
GITHUB_RAW = "https://raw.githubusercontent.com/kaos923/byk-ders-secici/main/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AYAR_DOSYA = os.path.join(BASE_DIR, "ayarlar.txt")
VERSION_DOSYA = os.path.join(BASE_DIR, "version.txt")

RENK_ARKA = "#1e1e2e"
RENK_KART = "#313244"
RENK_BUTON = "#89b4fa"
RENK_CIKIS = "#f38ba8"

dersler = [
    ("Türkçe", "Turkce.pdf", "turkce.png"),
    ("Matematik", "Matematik.pdf", "matematik.png"),
    ("İngilizce", "Ingilizce.pdf", "ingilizce.png"),
    ("Fen", "Fen.pdf", "fen.png"),
    ("Sosyal", "Sosyal.pdf", "sosyal.png"),
    ("Müzik", "Muzik.pdf", "muzik.png"),
    ("Din", "Din.pdf", "din.png"),
]

# ================== VERSION ==================
def yerel_surum_oku():
    try:
        return open(VERSION_DOSYA, encoding="utf-8").read().strip()
    except:
        return "0.0"

# ================== AYAR ==================
def ayar_yukle():
    try:
        s = open(AYAR_DOSYA, encoding="utf-8").read().splitlines()
        return s[0], s[1], s[2]
    except:
        return "?", "?", "1"

def ayar_kaydet(sinif, sube, bg):
    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        f.write(f"{sinif}\n{sube}\n{bg}")

# ================== PDF ==================
def pdf_ac(pdf):
    try:
        yol = os.path.join(BASE_DIR, pdf)
        if not os.path.exists(yol):
            raise FileNotFoundError(pdf)
        os.startfile(yol) if sys.platform.startswith("win") else subprocess.Popen(["xdg-open", yol])
    except Exception as e:
        messagebox.showerror("PDF Hatası", str(e))

# ================== GÜNCELLE (DÜZELTİLDİ) ==================
def guncelle():
    try:
        yerel = yerel_surum_oku()

        yeni = urllib.request.urlopen(
            GITHUB_RAW + "version.txt?nocache=" + str(os.urandom(8)),
            timeout=5
        ).read().decode().strip()

        if yeni == yerel:
            messagebox.showinfo("Güncelleme", "Zaten en güncel sürüm.")
            return

        if not messagebox.askyesno(
            "Güncelleme Var",
            f"Yeni sürüm: {yeni}\nMevcut sürüm: {yerel}\n\nGüncellensin mi?"
        ):
            return

        kod = urllib.request.urlopen(
            GITHUB_RAW + "ders_secici_full.py?nocache=" + str(os.urandom(8))
        ).read().decode("utf-8")

        open(__file__, "w", encoding="utf-8").write(kod)
        open(VERSION_DOSYA, "w", encoding="utf-8").write(yeni)

        messagebox.showinfo("Güncellendi", "Programı yeniden başlat.")

    except Exception as e:
        messagebox.showerror("Güncelleme Hatası", str(e))

# ================== ARKA PLAN ==================
def arka_plan_yukle():
    bg_canvas.delete("bg")
    bg_canvas.configure(bg=RENK_ARKA)

    if bg_acik != "1":
        return

    try:
        img = Image.open(os.path.join(BASE_DIR, "background.png"))
        img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        bg_images[0] = ImageTk.PhotoImage(img)
        bg_canvas.create_image(0, 0, image=bg_images[0], anchor="nw", tags="bg")
    except:
        pass

# ================== MODERN AYARLAR ==================
def ayarlar_pencere():
    win = tk.Toplevel(root)
    win.title("Ayarlar")
    win.geometry("380x460")
    win.configure(bg=RENK_ARKA)
    win.resizable(False, False)

    kart = tk.Frame(win, bg=RENK_KART)
    kart.pack(fill="both", expand=True, padx=18, pady=18)

    tk.Label(
        kart,
        text="⚙ Uygulama Ayarları",
        bg=RENK_KART,
        fg="white",
        font=("Segoe UI", 17, "bold")
    ).pack(pady=(15, 20))

    form = tk.Frame(kart, bg=RENK_KART)
    form.pack(fill="x", padx=20)

    tk.Label(form, text="Sınıf", bg=RENK_KART, fg="#cdd6f4").pack(anchor="w")
    sinif_e = tk.Entry(form)
    sinif_e.insert(0, sinif)
    sinif_e.pack(fill="x", pady=(4, 12))

    tk.Label(form, text="Şube", bg=RENK_KART, fg="#cdd6f4").pack(anchor="w")
    sube_e = tk.Entry(form)
    sube_e.insert(0, sube)
    sube_e.pack(fill="x", pady=(4, 16))

    tk.Frame(form, bg="#45475a", height=1).pack(fill="x", pady=12)

    bg_var = tk.IntVar(value=int(bg_acik))
    tk.Checkbutton(
        form,
        text="🖼 Arka Plan Açık",
        variable=bg_var,
        bg=RENK_KART,
        fg="white",
        selectcolor=RENK_ARKA,
        activebackground=RENK_KART,
        activeforeground="white"
    ).pack(anchor="w", pady=10)

    def kaydet():
        global sinif, sube, bg_acik
        sinif = sinif_e.get()
        sube = sube_e.get()
        bg_acik = str(bg_var.get())
        ayar_kaydet(sinif, sube, bg_acik)
        baslik.config(text=f"📚 BYK Ders Kitaplığı – {sinif}/{sube} (v{yerel_surum_oku()})")
        arka_plan_yukle()
        win.destroy()

    tk.Button(kart, text="💾 Kaydet", command=kaydet, bg=RENK_BUTON).pack(fill="x", padx=20, pady=6)
    tk.Button(kart, text="🔄 Güncellemeleri Kontrol Et", command=guncelle, bg=RENK_BUTON).pack(fill="x", padx=20)

# ================== ANA ==================
try:
    sinif, sube, bg_acik = ayar_yukle()

    root = tk.Tk()
    root.title("BYK Ders Kitaplığı")
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    bg_canvas = tk.Canvas(root, bg=RENK_ARKA, highlightthickness=0)
    bg_canvas.pack(fill="both", expand=True)

    bg_images = [None]
    arka_plan_yukle()

    baslik = tk.Label(
        bg_canvas,
        text=f"📚 BYK Ders Kitaplığı – {sinif}/{sube} (v{yerel_surum_oku()})",
        bg=RENK_ARKA,
        fg="white",
        font=("Segoe UI", 20, "bold")
    )
    baslik.pack(pady=10)

    tk.Button(bg_canvas, text="⚙ Ayarlar", command=ayarlar_pencere, bg=RENK_BUTON).pack(pady=5)

    canvas = tk.Canvas(bg_canvas, bg=RENK_ARKA, highlightthickness=0)
    scroll = tk.Scrollbar(bg_canvas, command=canvas.yview)
    icerik = tk.Frame(canvas, bg=RENK_ARKA)

    icerik.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=icerik, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(fill="both", expand=True, padx=20, pady=20)
    scroll.pack(side="right", fill="y")

    resimler = []

    for i, (ad, pdf, resim) in enumerate(dersler):
        kart = tk.Frame(icerik, bg=RENK_KART, padx=10, pady=10)
        kart.grid(row=i//4, column=i%4, padx=25, pady=25)

        try:
            yol = os.path.join(BASE_DIR, resim)
            img = ImageTk.PhotoImage(Image.open(yol)) if os.path.exists(yol) else None
        except:
            img = None

        resimler.append(img)

        tk.Button(
            kart,
            image=img,
            text=ad if not img else "",
            command=lambda p=pdf: pdf_ac(p),
            bg=RENK_KART,
            fg="white",
            bd=0
        ).pack()

        tk.Label(kart, text=ad, bg=RENK_KART, fg="white").pack(pady=5)

    tk.Button(
        bg_canvas,
        text=" Çıkış",
        command=root.destroy,
        bg=RENK_CIKIS,
        font=("Segoe UI", 12, "bold")
    ).pack(pady=15)

    root.mainloop()

except Exception:
    messagebox.showerror("KRİTİK HATA", traceback.format_exc())
