# modules/panduan_penggunaan.py
import streamlit as st
import os
import random
from PIL import Image

def page_panduan_penggunaan():
    st.header("📖 Panduan Penggunaan")
    st.markdown("""
    <div class='info-card'>
        <p>Aplikasi ReFisher dirancang untuk membantu Anda mengidentifikasi kesegaran ikan dengan mudah. Ikuti langkah-langkah di bawah untuk memulai klasifikasi:</p>
        <ul>
            <li><p><strong>Unggah Gambar atau Pilih Contoh:</strong> Anda dapat mengunggah foto ikan Anda sendiri dari perangkat Anda atau menggunakan salah satu contoh gambar ikan yang kami sediakan.</p></li>
            <li><p><strong>Tunggu Proses Analisis:</strong> Setelah gambar diunggah, aplikasi akan secara otomatis menganalisis gambar menggunakan model kecerdasan buatan kami. Proses ini biasanya berlangsung singkat.</p></li>
            <li><p><strong>Lihat Hasil Prediksi:</strong> Anda akan melihat hasil prediksi kesegaran ikan (Segar atau Tidak Segar) beserta tingkat keyakinannya, yang menunjukkan seberapa yakin model dengan prediksinya.</p></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📸 Tips Mengambil Foto Ikan yang Baik")
    st.markdown("""
    <div class='info-card'>
        <p>Untuk hasil klasifikasi yang paling akurat, perhatikan tips berikut saat mengambil foto ikan:</p>
        <ul>
            <li><strong>Fokus pada Mata Ikan:</strong> Mata ikan seringkali menjadi indikator utama kesegaran. Pastikan mata ikan terlihat jelas dan tidak buram dalam foto Anda.</li>
            <li><strong>Pencahayaan Cukup:</strong> Pastikan ikan mendapatkan pencahayaan yang merata dan cukup, hindari bayangan yang bisa menyembunyikan detail penting. Cahaya alami seringkali adalah yang terbaik.</li>
            <li><strong>Ambil dari Jarak Dekat:</strong> Foto *close-up* akan memberikan detail yang lebih kaya kepada model untuk dianalisis. Pastikan seluruh ikan terlihat dalam bingkai, jika memungkinkan.</li>
            <li><strong>Hindari Gambar Buram:</strong> Gambar yang tajam dan tidak buram akan membantu model mengenali fitur-fitur dengan lebih baik. Pastikan kamera Anda stabil.</li>
            <li><strong>Latar Belakang Netral:</strong> Gunakan latar belakang yang bersih dan tidak terlalu ramai agar model fokus pada ikan, bukan pada objek di sekitarnya.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🖼️ Contoh Gambar untuk Dicoba")
    st.markdown("<div class='info-card'><p>Tidak punya gambar ikan? Gunakan contoh gambar berikut untuk mencoba langsung aplikasi:</p></div>", unsafe_allow_html=True)
    
    sample_col1, sample_col2 = st.columns(2)
    # Sesuaikan path ke folder test_sample karena sekarang relatif terhadap root project
    # Atau, jika Anda ingin test_sample juga di dalam modules, sesuaikan path ini:
    # FRESH_DIR, NON_FRESH_DIR = "modules/test_sample/Fresh Fish", "modules/test_sample/Non Fresh Fish"
    # ASUMSI: test_sample masih di root project, jadi path relatifnya perlu diperbaiki
    FRESH_DIR = "test_sample/Fresh Fish"
    NON_FRESH_DIR = "test_sample/Non Fresh Fish"


    def on_sample_click(path):
        try:
            # Perhatikan: path ini harus dari root project jika test_sample ada di root
            full_path = os.path.join(os.getcwd(), path)
            if not os.path.isdir(full_path):
                st.error(f"Direktori tidak ditemukan: '{full_path}'. Pastikan folder 'test_sample' ada dan terisi gambar di root project Anda.")
                return
            files = [f for f in os.listdir(full_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
            if files:
                st.session_state.sample_image_path = os.path.join(full_path, random.choice(files))
                st.session_state.page = "Aplikasi Klasifikasi" # Kembali ke halaman utama setelah memilih contoh
            else:
                st.warning(f"Tidak ada file gambar di: '{full_path}'")
        except Exception as e:
            st.error(f"Gagal memuat gambar contoh: {e}")

    with sample_col1:
        if st.button("🟢 Contoh Ikan Segar", use_container_width=True): on_sample_click(FRESH_DIR)
    with sample_col2:
        if st.button("🔴 Contoh Ikan Tidak Segar", use_container_width=True): on_sample_click(NON_FRESH_DIR)