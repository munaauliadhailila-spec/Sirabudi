import streamlit as st
import hashlib
import os
from datetime import datetime

# --- 1. CONFIG & THEME (VERSI AUTO-CLEAR & DYNAMIC INTEGRITY) ---
st.set_page_config(page_title="SiraBudi Intelligence", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e3d24; }
    div[data-testid="stMetricValue"] { color: #fbc02d; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #ffffff; }
    .stButton>button, .stFormSubmitButton>button { 
        border-radius: 10px; border: 2px solid #fbc02d; 
        background-color: #2e5a35; color: #fbc02d; 
        font-weight: bold; transition: 0.3s; width: 100%;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover { 
        background-color: #fbc02d; color: #1e3d24; 
    }
    label, .stTextInput label p, .stSelectbox label p, .stTextArea label p, .stFileUploader label p {
        color: #ffffff !important; font-weight: 600 !important;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #2a5233; color: white; border: 1px solid #fbc02d !important;
    }
    [data-testid="stSidebar"] { background-color: #142918; border-right: 2px solid #fbc02d; }
    .file-card {
        background-color: #2a5233; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #fbc02d; margin-bottom: 10px; color: white;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: white; }
    .stTabs [aria-selected="true"] { color: #fbc02d; }
    .alarm-box {
        background-color: #4a1515; border: 1px solid #ff4b4b;
        padding: 10px; border-radius: 8px; color: white; margin-top: 5px; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

DAFTAR_SERVER = ["Server_A", "Server_B", "Server_C"]

def buat_sidik_jari(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

def tambah_log(pesan):
    if "logs" not in st.session_state: st.session_state.logs = []
    st.session_state.logs.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {pesan}")

# --- SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_role' not in st.session_state: st.session_state['user_role'] = None
if 'scan_aktif' not in st.session_state: st.session_state['scan_aktif'] = False
if 'logs' not in st.session_state: st.session_state.logs = []

# --- LOGIN ---
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center; color: #fbc02d;'>⚖️ SIRABUDI INTELLIGENCE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Sistem Integritas Barang Bukti Digital</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("form_masuk"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Akses Sistem", use_container_width=True):
                if user == "admin" and pwd == "admin":
                    st.session_state.logged_in, st.session_state.user_role = True, "admin"
                    st.rerun()
                elif user == "user" and pwd == "user":
                    st.session_state.logged_in, st.session_state.user_role = True, "user"
                    st.rerun()
                else: st.error("Akses Ditolak!")
else:
    # --- HEADER & SIDEBAR ATAS ---
    with st.sidebar:
        st.markdown("<h2 style='color: #fbc02d;'>🛡️ System Guard</h2>", unsafe_allow_html=True)
        role_label = "Jaksa Pratama (ADMIN)" if st.session_state.user_role == "admin" else "Staff Barang Bukti"
        st.success(f"Petugas: **{role_label}**")
        if st.button("🚪 Keluar Sistem", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.scan_aktif = False
            st.rerun()

    st.markdown("<h1 style='color: #fbc02d;'>⚖️ SIRABUDI INTELLIGENCE</h1>", unsafe_allow_html=True)
    
    # =========================================================
    # LOGIKA BARU: HITUNG INTEGRITY SCORE SECARA REAL-TIME
    # =========================================================
    total_file = 0
    file_sehat = 0
    if os.path.exists("Server_A"):
        master_files = [f for f in os.listdir("Server_A") if not f.endswith("_hash.txt") and not f.endswith("_meta.txt") and not f.startswith(".")]
        for fname in master_files:
            for s in DAFTAR_SERVER:
                total_file += 1
                pf = os.path.join(s, fname)
                ph = os.path.join(s, f"{fname}_hash.txt")
                if os.path.exists(pf) and os.path.exists(ph):
                    with open(ph, "r") as f: h_a = f.read().strip()
                    with open(pf, "rb") as f: 
                        if hashlib.sha256(f.read()).hexdigest() == h_a:
                            file_sehat += 1

    skor_integritas = int((file_sehat / total_file) * 100) if total_file > 0 else 100
    status_delta = "Verified" if skor_integritas == 100 else "-TERCEMAR"
    
    # METRICS RENDER
    m1, m2, m3 = st.columns(3)
    m1.metric("Integrity Score", f"{skor_integritas}%", delta=status_delta)
    m2.metric("Nodes Active", "3/3", delta="Synced")
    m3.metric("Encryption", "SHA-256", delta="Active")
    st.divider()

    role = st.session_state.user_role

    if role == "admin":
        tab1, tab2 = st.tabs(["🕵️ LABORATORIUM AUDIT", "🔍 KOMPARASI BUKTI"])

        with tab1:
            st.markdown("<h3 style='color: white;'>Laboratorium Audit & Forensik Digital</h3>", unsafe_allow_html=True)
            if st.button("🔍 Mulai Audit Sinkronisasi Server", use_container_width=True):
                st.session_state.scan_aktif = True
                tambah_log("Admin menjalankan Audit Forensik Global.")
            
            if st.session_state.scan_aktif:
                if os.path.exists("Server_A"):
                    files = [f for f in os.listdir("Server_A") if not f.endswith("_hash.txt") and not f.endswith("_meta.txt") and not f.startswith(".")]
                    for file_name in files:
                        meta_path = os.path.join("Server_A", f"{file_name}_meta.txt")
                        metadata = "Metadata tidak ditemukan."
                        if os.path.exists(meta_path):
                            with open(meta_path, "r") as f: metadata = f.read()

                        st.markdown(f"<div class='file-card'>📂 <b>Barang Bukti:</b> {file_name}<br><small style='color: #fbc02d;'>{metadata}</small></div>", unsafe_allow_html=True)
                        
                        cols = st.columns(3)
                        node_sehat, data_sehat = None, None
                        
                        for s in DAFTAR_SERVER:
                            pf, ph = os.path.join(s, file_name), os.path.join(s, f"{file_name}_hash.txt")
                            if os.path.exists(pf) and os.path.exists(ph):
                                with open(ph, "r") as f: h_a = f.read().strip()
                                with open(pf, "rb") as f: 
                                    dat = f.read()
                                    if hashlib.sha256(dat).hexdigest() == h_a:
                                        node_sehat, data_sehat = s, dat
                                        break
                        
                        for i, s in enumerate(DAFTAR_SERVER):
                            pf, ph = os.path.join(s, file_name), os.path.join(s, f"{file_name}_hash.txt")
                            with cols[i]:
                                if os.path.exists(pf) and os.path.exists(ph):
                                    with open(ph, "r") as f: h_a = f.read().strip()
                                    with open(pf, "rb") as f: dat_now = f.read()
                                    
                                    if hashlib.sha256(dat_now).hexdigest() == h_a: 
                                        st.success(f"✅ {s}: AMAN")
                                    else:
                                        st.error(f"❌ {s}: MANIPULASI!")
                                        waktu_ubah = datetime.fromtimestamp(os.path.getmtime(pf)).strftime('%H:%M:%S (%d-%m-%Y)')
                                        st.toast(f"🚨 ANOMALI: {file_name} di {s} diubah pada {waktu_ubah}!", icon="🚨")
                                        st.markdown(f"<div class='alarm-box'>⚠️ <b>Forensic Alert:</b><br>File diubah pada:<br>{waktu_ubah}</div>", unsafe_allow_html=True)
                                        
                                        if data_sehat and st.button(f"Sembuhkan {s}", key=f"h_{s}_{file_name}"):
                                            with open(pf, "wb") as f: f.write(data_sehat)
                                            tambah_log(f"Admin menyembuhkan manipulasi file di {s}")
                                            st.rerun()
                                else:
                                    st.error(f"❓ {s}: HILANG")
                                    if data_sehat and st.button(f"Pulihkan {s}", key=f"r_{s}_{file_name}"):
                                        with open(pf, "wb") as f: f.write(data_sehat)
                                        tambah_log(f"Admin memulihkan data yang hilang di {s}")
                                        st.rerun()

        with tab2:
            st.markdown("<h3 style='color: white;'>⚖️ Komparasi Identitas Barang Bukti</h3>", unsafe_allow_html=True)
            if os.path.exists("Server_A"):
                files_on_server = [f for f in os.listdir("Server_A") if not f.endswith("_hash.txt") and not f.endswith("_meta.txt") and not f.startswith(".")]
                if files_on_server:
                    col_file1, col_file2 = st.columns(2)
                    with col_file1:
                        st.markdown("<p style='color:white'><b>🏢 File di Server</b></p>", unsafe_allow_html=True)
                        file_lama = st.selectbox("Pilih file yang sudah ada", files_on_server, key="admin_sel")
                        with open(os.path.join("Server_A", f"{file_lama}_hash.txt"), "r") as f:
                            hash_lama = f.read().strip()
                        st.info(f"Hash: `{hash_lama[:20]}...`")

                    with col_file2:
                        st.markdown("<p style='color:white'><b>📥 File Baru (Pembanding)</b></p>", unsafe_allow_html=True)
                        uploaded_baru = st.file_uploader("Upload file untuk dibandingkan", type=["pdf", "jpg", "png"], key="admin_up")

                    if uploaded_baru:
                        bytes_baru = uploaded_baru.getvalue()
                        hash_baru = buat_sidik_jari(bytes_baru)
                        st.divider()
                        
                        if hash_lama == hash_baru:
                            st.success("✅ **IDENTIK (100%)**")
                            st.write("<span style='color:white'>Kedua file memiliki sidik jari digital yang sama persis.</span>", unsafe_allow_html=True)
                            tambah_log("Admin melakukan komparasi data (Hasil: IDENTIK)")
                        else:
                            st.error("⚠️ **TIDAK IDENTIK**")
                            st.write("<span style='color:white'>Peringatan: Berkas pembanding telah dimodifikasi.</span>", unsafe_allow_html=True)
                            tambah_log("Admin melakukan komparasi data (Hasil: TIDAK IDENTIK)")

    else:
        # --- TAB UNTUK STAF ---
        tab_staf_reg, tab_staf_komp = st.tabs(["➕ REGISTRASI BUKTI", "🔍 KOMPARASI BUKTI"])
        
        with tab_staf_reg:
            with st.form("form_registrasi_staf", clear_on_submit=True):
                st.markdown("<h3 style='color: white;'>Registrasi Barang Bukti Baru</h3>", unsafe_allow_html=True)
                col_x, col_y = st.columns(2)
                with col_x:
                    no_perk = st.text_input("Nomor Perkara", placeholder="PDM-001/JKT/04/2026")
                    jaksa = st.text_input("Jaksa Peneliti", placeholder="Nama Jaksa...")
                with col_y:
                    kat = st.selectbox("Tipe Bukti", ["Surat/Dokumen", "Media Elektronik", "Foto Forensik"])
                    ket = st.text_area("Catatan Tambahan", placeholder="Lokasi penemuan...", height=68)

                uploaded_file = st.file_uploader("Upload File Baru", type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx", "txt"])
                submit_button = st.form_submit_button("🛡️ Replikasi ke Server Pusat", use_container_width=True)

                if submit_button:
                    if uploaded_file is None:
                        st.error("⚠️ Gagal! Anda belum memasukkan file barang bukti.")
                    else:
                        bytes_data = uploaded_file.getvalue()
                        h_asli = buat_sidik_jari(bytes_data)
                        meta_content = f"No: {no_perk} | Jaksa: {jaksa} | Tipe: {kat} | Ket: {ket}"
                        
                        for s in DAFTAR_SERVER:
                            if not os.path.exists(s): os.makedirs(s)
                            with open(os.path.join(s, uploaded_file.name), "wb") as f: f.write(bytes_data)
                            with open(os.path.join(s, f"{uploaded_file.name}_hash.txt"), "w") as f_hash: f_hash.write(h_asli)
                            with open(os.path.join(s, f"{uploaded_file.name}_meta.txt"), "w") as f_meta: f_meta.write(meta_content)
                        
                        tambah_log(f"Staf upload & replikasi: {uploaded_file.name}")
                        st.success(f"✅ Berhasil! Data '{uploaded_file.name}' telah diamankan. Form telah dikosongkan.")
                        st.toast("Replikasi Berhasil ke 3 Server!", icon="✅")

        with tab_staf_komp:
            st.markdown("<h3 style='color: white;'>⚖️ Komparasi Identitas Barang Bukti</h3>", unsafe_allow_html=True)
            if os.path.exists("Server_A"):
                files_on_server = [f for f in os.listdir("Server_A") if not f.endswith("_hash.txt") and not f.endswith("_meta.txt") and not f.startswith(".")]
                if files_on_server:
                    col_file1, col_file2 = st.columns(2)
                    with col_file1:
                        st.markdown("<p style='color:white'><b>🏢 File di Server</b></p>", unsafe_allow_html=True)
                        file_lama = st.selectbox("Pilih file yang sudah ada", files_on_server, key="staf_sel")
                        with open(os.path.join("Server_A", f"{file_lama}_hash.txt"), "r") as f:
                            hash_lama = f.read().strip()
                        st.info(f"Hash: `{hash_lama[:20]}...`")

                    with col_file2:
                        st.markdown("<p style='color:white'><b>📥 File Baru (Pembanding)</b></p>", unsafe_allow_html=True)
                        uploaded_baru = st.file_uploader("Upload file untuk dibandingkan", type=["pdf", "jpg", "png"], key="staf_up")

                    if uploaded_baru:
                        bytes_baru = uploaded_baru.getvalue()
                        hash_baru = buat_sidik_jari(bytes_baru)
                        st.divider()
                        
                        if hash_lama == hash_baru:
                            st.success("✅ **IDENTIK (100%)**")
                            st.write("<span style='color:white'>Berkas valid dan belum dimodifikasi. Aman dilanjutkan.</span>", unsafe_allow_html=True)
                            tambah_log("Staf cek komparasi data (Hasil: AMAN)")
                        else:
                            st.error("⚠️ **TIDAK IDENTIK**")
                            st.write("<span style='color:white'>Peringatan: Hash berubah! Jangan serahkan berkas ini.</span>", unsafe_allow_html=True)
                            tambah_log("Staf cek komparasi data (Hasil: ANOMALI/BERBEDA)")

    # --- RENDER LOG DI BAGIAN BAWAH AGAR REAL-TIME ---
    with st.sidebar:
        st.divider()
        st.write("<span style='color:white'>📜 **Logs Terbaru**</span>", unsafe_allow_html=True)
        for log in st.session_state.logs[:6]: 
            st.markdown(f"<small style='color:#cccccc'>{log}</small>", unsafe_allow_html=True)