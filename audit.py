import hashlib
import os

def buat_sidik_jari(path_file):
    with open(path_file, "rb") as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()

daftar_server = ["Server_A", "Server_B", "Server_C"]
nama_file = "bukti.pdf"

print("🔍 MEMULAI PROSES AUDIT DIGITAL...\n")

for folder in daftar_server:
    path_file = os.path.join(folder, nama_file)
    path_catatan = os.path.join(folder, "catatan_hash.txt")

    # 1. Cek apakah filenya masih ada di folder server
    if os.path.exists(path_file) and os.path.exists(path_catatan):
        # Baca hash asli dari catatan
        with open(path_catatan, "r") as f:
            hash_asli = f.read().strip()
        
        # Hitung ulang hash file yang ada sekarang
        hash_sekarang = buat_sidik_jari(path_file)

        # 2. Bandingkan!
        if hash_asli == hash_sekarang:
            print(f"✅ {folder}: AMAN (Data Identik)")
        else:
            print(f"❌ {folder}: TERDETEKSI MANIPULASI! (Isi file berubah)")
    else:
        print(f"⚠️ {folder}: FILE HILANG ATAU RUSAK!")

print("\n--- AUDIT SELESAI ---")