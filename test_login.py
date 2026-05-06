import streamlit as st

# 1. Cek apakah sudah login atau belum
if 'sudah_login' not in st.session_state:
    st.session_state['sudah_login'] = False

# 2. Tampilan kalau BELUM login
if st.session_state['sudah_login'] == False:
    st.title("Halaman Login")
    user = st.text_input("Nama")
    if st.button("Masuk"):
        if user == "della":
            st.session_state['sudah_login'] = True
            st.rerun()
        else:
            st.error("Namanya salah!")

# 3. Tampilan kalau SUDAH login
else:
    st.title("Selamat Datang di SiraBudi!")
    st.write("Sekarang kamu sudah masuk ke dalam sistem.")
    if st.button("Keluar"):
        st.session_state['sudah_login'] = False
        st.rerun()