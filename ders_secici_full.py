def guncelle():
    try:
        with urllib.request.urlopen(GITHUB_RAW + "version.txt", timeout=5) as r:
            yeni_surum = r.read().decode().strip()

        if yeni_surum == MEVCUT_SURUM:
            messagebox.showinfo("Güncelleme", "Zaten en güncel sürüm.")
            return

        if not messagebox.askyesno(
            "Güncelleme Var",
            f"Yeni sürüm: {yeni_surum}\nYeni dosya indirilsin mi?"
        ):
            return

        yeni_dosya = os.path.join(BASE_DIR, "ders_secici_full_new.py")

        with urllib.request.urlopen(GITHUB_RAW + "ders_secici_full.py") as r:
            yeni_kod = r.read().decode("utf-8")

        with open(yeni_dosya, "w", encoding="utf-8") as f:
            f.write(yeni_kod)

        with open(VERSION_DOSYA, "w", encoding="utf-8") as f:
            f.write(yeni_surum)

        messagebox.showinfo(
            "Güncellendi",
            "Yeni sürüm indirildi.\n"
            "ders_secici_full_new.py dosyasını aç."
        )

    except Exception as e:
        messagebox.showerror("Hata", f"Güncelleme başarısız:\n{e}")
