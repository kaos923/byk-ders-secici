import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os, sys, subprocess, ctypes

# ================== SABİTLER ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KITAP_DIR = os.path.join(BASE_DIR, "kitaplar")
AYAR_DOSYA = os.path.join(BASE_DIR, "ayarlar.txt")

RENK_ARKA = "#1e1e2e"
RENK_KART = "#313244"
RENK_YAZI = "white"

# ================== AYAR ==================
def ayar_yukle():
    try:
        return open(AYAR_DOSYA, encoding="utf-8").read().strip()
    except:
        return ""

def ayar_kaydet(son):
    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        f.write(son)

son_acilan = ayar_yukle()

# ================== PDF ==================
def pdf_ac(yol):
    try:
        ayar_kaydet(yol)
        os.startfile(yol)
    except Exception as e:
        messagebox.showerror("PDF Hatası", str(e))

# ================== PC ARKA PLAN ==================
def pc_arka_plan():
    dosya = filedialog.askopenfilename(
        title="Arka Plan Seç",
        filetypes=[("Resimler", "*.jpg *.png *.bmp")]
    )
    if dosya:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, dosya, 3)

# ================== KİTAPLAR ==================
def kitaplari_getir():
    kitaplar = []
    if not os.path.exists(KITAP_DIR):
        messagebox.showerror("Hata", "'kitaplar' klasörü yok!")
        return kitaplar

    for f in sorted(os.listdir(KITAP_DIR)):
        if f.lower().endswith(".pdf"):
            ad = os.path.splitext(f)[0]
            pdf = os.path.join(KITAP_DIR, f)
            kapak = os.path.join(KITAP_DIR, ad + ".png")
            kitaplar.append((ad, pdf, kapak))
    return kitaplar

# ================== ARAMA ==================
def filtrele(*_):
    for w in icerik.winfo_children():
        w.destroy()

    aranan = arama.get().lower()
    kitaplar = kitaplari_getir()

    col = 0
    row = 0

    for ad, pdf, kapak in kitaplar:
        if aranan not in ad.lower():
            continue

        kart = tk.Frame(icerik, bg=RENK_KART, padx=10, pady=10)
        kart.grid(row=row, column=col, padx=20, pady=20)

        try:
            if os.path.exists(kapak):
                img = ImageTk.PhotoImage(Image.open(kapak).resize((120,160)))
            else:
                img = None
        except:
            img = None

        btn = tk.Button(
            kart,
            image=img,
            text=ad if not img else "",
            bg=RENK_KART,
            fg=RENK_YAZI,
            command=lambda p=pdf: pdf_ac(p),
            bd=0
        )
        btn.image = img
        btn.pack()

        tk.Label(kart, text=ad, bg=RENK_KART, fg=RENK_YAZI).pack(pady=5)

        col += 1
        if col == 4:
            col = 0
            row += 1

# ================== ARAYÜZ ==================
root = tk.Tk()
root.title("BYK Ders Kitaplığı")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
root.configure(bg=RENK_ARKA)

tk.Label(
    root,
    text="📚 BYK Ders Kitaplığı",
    font=("Segoe UI", 22, "bold"),
    bg=RENK_ARKA,
    fg=RENK_YAZI
).pack(pady=10)

arama = tk.StringVar()
arama.trace_add("write", filtrele)

tk.Entry(
    root,
    textvariable=arama,
    font=("Segoe UI", 14)
).pack(pady=5)

canvas = tk.Canvas(root, bg=RENK_ARKA, highlightthickness=0)
scroll = tk.Scrollbar(root, command=canvas.yview)
icerik = tk.Frame(canvas, bg=RENK_ARKA)

icerik.bind("<Configure>", lambda e:
    canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=icerik, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(fill="both", expand=True)
scroll.pack(side="right", fill="y")

filtrele()

# Son açılan kitabı otomatik açma (isteğe bağlı)
if son_acilan and os.path.exists(son_acilan):
    pdf_ac(son_acilan)

tk.Button(
    root,
    text="🖼 PC Arka Planını Değiştir",
    command=pc_arka_plan
).pack(pady=5)

tk.Button(
    root,
    text="❌ Çıkış",
    command=root.destroy
).pack(pady=10)

root.mainloop()
