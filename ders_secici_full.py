import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os, sys, subprocess, urllib.request, traceback
import ctypes

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

# ================== PC ARKA PLAN ==================
def pc_arka_plan_degistir():
    try:
        dosya = filedialog.askopenfilename(
            title="Arka Plan Seç",
            filetypes=[("Resimler", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not dosya:
            return

        ctypes.windll.user32.SystemParametersInfoW(
            20, 0, dosya, 3
        )

        messagebox.showinfo("Başarılı", "Bilgisayar arka planı değiştirildi.")

    except Exception as e:
        messagebox.showerror("Hata", str(e))

# ================== GÜNCELLE ==================
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

# ================== AYARLAR ==================
def ayarlar_pencere():
    win = tk.Toplevel(root)
    win.title("Ayarlar")
    win.geometry("380x460")
    win.configure(bg=RENK_ARKA)
    win.resizable(False, False)

    kart = tk.Frame(win, bg=RENK_KART)
    kart.pack(fill="both", expand=True, padx=18, pady=18)

    tk.Label(kart, text="⚙ Ayarlar", bg=RENK_KART, fg="white",
             font=("Segoe UI", 17, "bold")).pack(pady=20)

    tk.Button(
        kart,
        text="🖼 Bilgisayar Arka Planını Değiştir",
        command=pc_arka_plan_degistir,
        bg=RENK_BUTON
    ).pack(fill="x", padx=20, pady=10)

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

    tk.Button(bg_canvas, text="⚙ Ayarlar", command=ayarlar_pencere,
              bg=RENK_BUTON).pack(pady=5)

    tk.Button(
        bg_canvas,
        text="🖼 Bilgisayar Arka Planını Değiştir",
        command=pc_arka_plan_degistir,
        bg=RENK_BUTON
    ).pack(pady=5)

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
