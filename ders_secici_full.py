import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os, sys, subprocess, ctypes, traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KITAP_DIR = os.path.join(BASE_DIR, "kitaplar")
AYAR_DOSYA = os.path.join(BASE_DIR, "ayarlar.txt")

# ================== AYARLAR ==================
def ayar_yukle():
    try:
        s = open(AYAR_DOSYA, encoding="utf-8").read().splitlines()
        return {
            "tema": s[0],
            "bg": s[1],
            "mod": s[2],
            "son": s[3] if len(s) > 3 else ""
        }
    except:
        return {"tema": "dark", "bg": "1", "mod": "ogrenci", "son": ""}

def ayar_kaydet():
    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        f.write("\n".join([
            ayar["tema"],
            ayar["bg"],
            ayar["mod"],
            ayar["son"]
        ]))

ayar = ayar_yukle()

# ================== TEMA ==================
def tema_renk():
    return {
        "bg": "#1e1e2e" if ayar["tema"] == "dark" else "#f5f5f5",
        "kart": "#313244" if ayar["tema"] == "dark" else "#ffffff",
        "fg": "white" if ayar["tema"] == "dark" else "black"
    }

# ================== PDF ==================
def pdf_ac(yol):
    try:
        ayar["son"] = yol
        ayar_kaydet()
        os.startfile(yol)
    except Exception as e:
        messagebox.showerror("PDF", str(e))

# ================== PC ARKA PLAN ==================
def pc_arka_plan():
    dosya = filedialog.askopenfilename(
        filetypes=[("Resim", "*.jpg *.png *.bmp")]
    )
    if dosya:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, dosya, 3)

# ================== KİTAPLARI YÜKLE ==================
def kitaplari_getir():
    kitaplar = []
    if not os.path.exists(KITAP_DIR):
        return kitaplar

    for f in os.listdir(KITAP_DIR):
        if f.lower().endswith(".pdf"):
            ad = os.path.splitext(f)[0]
            kapak = os.path.join(KITAP_DIR, ad + ".png")
            kitaplar.append((ad, os.path.join(KITAP_DIR, f), kapak))
    return kitaplar

# ================== ARAMA ==================
def filtrele(*_):
    for w in icerik.winfo_children():
        w.destroy()

    aranan = arama.get().lower()
    kitaplar = kitaplari_getir()

    for i, (ad, pdf, kapak) in enumerate(kitaplar):
        if aranan not in ad.lower():
            continue

        kart = tk.Frame(icerik, bg=R["kart"], padx=10, pady=10)
        kart.grid(row=i//4, column=i%4, padx=20, pady=20)

        try:
            img = ImageTk.PhotoImage(Image.open(kapak).resize((120,160)))
        except:
            img = None

        btn = tk.Button(
            kart, image=img, text=ad if not img else "",
            bg=R["kart"], fg=R["fg"],
            command=lambda p=pdf: pdf_ac(p)
        )
        btn.image = img
        btn.pack()

        tk.Label(kart, text=ad, bg=R["kart"], fg=R["fg"]).pack()

# ================== ARAYÜZ ==================
root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())

R = tema_renk()
root.configure(bg=R["bg"])

tk.Label(root, text="📚 BYK Ders Kitaplığı",
         font=("Segoe UI", 22, "bold"),
         bg=R["bg"], fg=R["fg"]).pack(pady=10)

arama = tk.StringVar()
arama.trace_add("write", filtrele)

tk.Entry(root, textvariable=arama,
         font=("Segoe UI", 14)).pack(pady=5)

canvas = tk.Canvas(root, bg=R["bg"], highlightthickness=0)
scroll = tk.Scrollbar(root, command=canvas.yview)
icerik = tk.Frame(canvas, bg=R["bg"])

icerik.bind("<Configure>", lambda e:
    canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0,0), window=icerik, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(fill="both", expand=True)
scroll.pack(side="right", fill="y")

filtrele()

if ayar["son"] and os.path.exists(ayar["son"]):
    pdf_ac(ayar["son"])

tk.Button(root, text="🖼 PC Arka Plan",
          command=pc_arka_plan).pack(pady=5)

tk.Button(root, text="🌙 Tema Değiştir",
          command=lambda: (
              ayar.update({"tema": "light" if ayar["tema"]=="dark" else "dark"}),
              ayar_kaydet(),
              os.execl(sys.executable, sys.executable, *sys.argv)
          )).pack(pady=5)

tk.Button(root, text="❌ Çıkış",
          command=root.destroy).pack(pady=10)

root.mainloop()
