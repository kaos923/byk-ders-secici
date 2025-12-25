import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os, sys, ctypes, urllib.request, random

# ================== SABİTLER ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KITAP_DIR = os.path.join(BASE_DIR, "kitaplar")
AYAR_DOSYA = os.path.join(BASE_DIR, "ayarlar.txt")
VERSION_DOSYA = os.path.join(BASE_DIR, "version.txt")
ANA_DOSYA = os.path.basename(__file__)

GITHUB_RAW = "https://raw.githubusercontent.com/kaos923/byk-ders-secici/main/"

RENK_ARKA = "#1e1e2e"
RENK_KART = "#313244"
RENK_YAZI = "white"
RENK_BUTON = "#89b4fa"

# ================== AYAR ==================
def ayar_yukle():
    try:
        s = open(AYAR_DOSYA, encoding="utf-8").read().splitlines()
        return s[0], s[1], s[2], s[3]
    except:
        return "?", "?", "1", ""

def ayar_kaydet(sinif, sube, oto, son):
    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        f.write(f"{sinif}\n{sube}\n{oto}\n{son}")

sinif, sube, oto_ac, son_acilan = ayar_yukle()

# ================== PDF ==================
def pdf_ac(yol):
    try:
        ayar_kaydet(sinif, sube, oto_ac, yol)
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
    col = row = 0

    for ad, pdf, kapak in kitaplari_getir():
        if aranan not in ad.lower():
            continue

        kart = tk.Frame(icerik, bg=RENK_KART, padx=10, pady=10)
        kart.grid(row=row, column=col, padx=20, pady=20)

        try:
            img = ImageTk.PhotoImage(Image.open(kapak).resize((120, 160))) if os.path.exists(kapak) else None
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

# ================== GÜNCELLEME ==================
def yerel_surum():
    try:
        return open(VERSION_DOSYA, encoding="utf-8").read().strip()
    except:
        return "0.0"

def guncelle():
    try:
        cache = "?v=" + str(random.randint(1000, 9999))

        yeni = urllib.request.urlopen(
            GITHUB_RAW + "version.txt" + cache,
            timeout=5
        ).read().decode().strip()

        mevcut = yerel_surum()

        if yeni == mevcut:
            messagebox.showinfo("Güncelleme", "Zaten güncel.")
            return

        if not messagebox.askyesno(
            "Güncelleme",
            f"Yeni sürüm: {yeni}\nMevcut: {mevcut}\n\nGüncellensin mi?"
        ):
            return

        kod = urllib.request.urlopen(
            GITHUB_RAW + ANA_DOSYA + cache,
            timeout=10
        ).read().decode("utf-8")

        open(__file__, "w", encoding="utf-8").write(kod)
        open(VERSION_DOSYA, "w", encoding="utf-8").write(yeni)

        messagebox.showinfo("Güncellendi", "Program yeniden başlatılacak.")
        root.destroy()

    except Exception as e:
        messagebox.showerror("Güncelleme Hatası", str(e))

# ================== AYARLAR ==================
def ayarlar_pencere():
    win = tk.Toplevel(root)
    win.title("Ayarlar")
    win.geometry("350x420")
    win.configure(bg=RENK_ARKA)

    kart = tk.Frame(win, bg=RENK_KART, padx=20, pady=20)
    kart.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(kart, text="⚙ Ayarlar", bg=RENK_KART, fg="white",
             font=("Segoe UI", 16, "bold")).pack(pady=10)

    tk.Label(kart, text="Sınıf", bg=RENK_KART, fg="white").pack(anchor="w")
    sinif_e = tk.Entry(kart)
    sinif_e.insert(0, sinif)
    sinif_e.pack(fill="x")

    tk.Label(kart, text="Şube", bg=RENK_KART, fg="white").pack(anchor="w", pady=(10, 0))
    sube_e = tk.Entry(kart)
    sube_e.insert(0, sube)
    sube_e.pack(fill="x")

    oto_var = tk.IntVar(value=int(oto_ac))
    tk.Checkbutton(
        kart,
        text="Son açılan kitabı otomatik aç",
        variable=oto_var,
        bg=RENK_KART,
        fg="white",
        selectcolor=RENK_ARKA
    ).pack(pady=15, anchor="w")

    def kaydet():
        global sinif, sube, oto_ac
        sinif = sinif_e.get()
        sube = sube_e.get()
        oto_ac = str(oto_var.get())
        ayar_kaydet(sinif, sube, oto_ac, son_acilan)
        baslik.config(text=f"📚 BYK Ders Kitaplığı – {sinif}/{sube}")
        win.destroy()

    tk.Button(kart, text="💾 Kaydet", command=kaydet, bg=RENK_BUTON).pack(fill="x", pady=5)
    tk.Button(kart, text="🖼 PC Arka Planı", command=pc_arka_plan).pack(fill="x")
    tk.Button(kart, text="🔄 Güncellemeleri Kontrol Et", command=guncelle,
              bg=RENK_BUTON).pack(fill="x", pady=(10, 0))

# ================== ARAYÜZ ==================
root = tk.Tk()
root.title("BYK Ders Kitaplığı")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
root.configure(bg=RENK_ARKA)

baslik = tk.Label(
    root,
    text=f"📚 BYK Ders Kitaplığı – {sinif}/{sube}",
    font=("Segoe UI", 22, "bold"),
    bg=RENK_ARKA,
    fg=RENK_YAZI
)
baslik.pack(pady=10)

tk.Button(root, text="⚙ Ayarlar", command=ayarlar_pencere,
          bg=RENK_BUTON).pack()

arama = tk.StringVar()
arama.trace_add("write", filtrele)
tk.Entry(root, textvariable=arama, font=("Segoe UI", 14)).pack(pady=5)

canvas = tk.Canvas(root, bg=RENK_ARKA, highlightthickness=0)
scroll = tk.Scrollbar(root, command=canvas.yview)
icerik = tk.Frame(canvas, bg=RENK_ARKA)

icerik.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=icerik, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(fill="both", expand=True)
scroll.pack(side="right", fill="y")

filtrele()

if oto_ac == "1" and son_acilan and os.path.exists(son_acilan):
    pdf_ac(son_acilan)

tk.Button(root, text="❌ Çıkış", command=root.destroy).pack(pady=10)

root.mainloop()
