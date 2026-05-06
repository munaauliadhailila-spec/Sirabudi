import hashlib
import os
import shutil # Ini library untuk copy file

def buat_sidik_jari(path_file):
    with open(path_file, "rb") as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()

# Konfigurasi
nama_file = "bukti.pdf"
daftar_server = ["Server_A", "Server_B", "Server_C"]

if os.path.exists(nama_file):
    # 1. Hitung Hash Asli
    kode_asli = buat_sidik_jari(nama_file)
    print(f"✅ Berhasil scan bukti asli: {kode_asli[:10]}...")

    # 2. Distribusikan ke semua server
    print("\n--- PROSES DISTRIBUSI KE SERVER ---")
    for folder in daftar_server:
        # Tentukan lokasi tujuan (misal: Server_A/bukti.pdf)
        tujuan = os.path.join(folder, nama_file)
        
        # Copy filenya
        shutil.copy(nama_file, tujuan)
        
        # Simpan juga catatan hash-nya di dalam folder server tersebut
        with open(os.path.join(folder, "catatan_hash.txt"), "w") as f_hash:
            f_hash.write(kode_asli)
            
        print(f"🚀 Bukti berhasil dikirim ke: {folder}")
    
    print("\n[STATUS]: SEMUA SERVER TELAH TER-SYNCHRONIZED")
else:
    print(f"❌ File {nama_file} tidak ditemukan!")