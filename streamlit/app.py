import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import io
import os
import random
import base64

# --- Import halaman dari modules ---
from modules.panduan_penggunaan import page_panduan_penggunaan
from modules.faq import page_faq
from modules.articles import page_articles

# --- Diubah untuk tflite-runtime ---
try:
    from tflite_runtime.interpreter import Interpreter
    TFLITE_AVAILABLE = True
except ImportError:
    try:
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter
        TFLITE_AVAILABLE = True
    except (ImportError, AttributeError):
        # Jika keduanya gagal, gunakan mode demo
        TFLITE_AVAILABLE = False
        st.warning("⚠️ Peringatan: `tflite-runtime` atau `tensorflow` tidak ditemukan. Aplikasi berjalan dalam mode demo dengan prediksi acak.")


# --- Kelas MinimalTFLiteInterpreter (tetap sama) ---
class MinimalTFLiteInterpreter:
    """Minimal TensorFlow Lite interpreter for when TensorFlow is not available"""
    def __init__(self, model_path):
        self.model_path = model_path
        self.input_height = 224
        self.input_width = 224
        
    def allocate_tensors(self):
        pass
        
    def get_input_details(self):
        return [{'shape': [1, 224, 224, 3]}]
        
    def get_output_details(self):
        return [{'index': 0}]
        
    def set_tensor(self, index, data):
        pass
        
    def invoke(self):
        pass
        
    def get_tensor(self, index):
        fresh_confidence = np.random.uniform(0.6, 0.95)
        non_fresh_confidence = 1.0 - fresh_confidence
        return np.array([[fresh_confidence, non_fresh_confidence]], dtype=np.float32)

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="ReFisher - Klasifikasi Kesegaran Ikan",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS untuk tampilan aplikasi
st.markdown("""
<style>
    /* Global Styles for Main Headers and Subtitles */
    /* .main-header tidak lagi digunakan untuk nama aplikasi, tapi bisa untuk judul bagian lain */
    .main-header {
        font-size: 2.5rem; /* Sedikit dikecilkan karena ada logo besar */
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    /* Prediction Box Styles */
    .prediction-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        color: white;
    }
    .fresh-fish {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .non-fresh-fish {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    /* Info Card Styles */
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }

    /* Metric Card Styles */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }

    /* Footer Styles */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }

    /* Font sizes for main content paragraphs, lists, and general markdown */
    p,
    li,
    div.stMarkdown p, /* General markdown paragraphs */
    .info-card p, .info-card li,
    .stMarkdown ul li, .stMarkdown ol li,
    div[data-testid^="stMarkdownContainer"] p,
    div[data-testid^="stMarkdownContainer"] li,
    div[data-testid^="stMarkdownContainer"] span {
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }

    /* Font sizes for sidebar */
    .stSidebar p, .stSidebar li, .stSidebar .stMarkdown p, .stSidebar .stMarkdown li {
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }

    /* CSS for article images (st.image()) */
    div[data-testid="stImage"] img {
        max-height: 400px !important;
        object-fit: contain !important;
        width: 100% !important;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* CSS for custom HTML article cards */
    .article-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        margin-bottom: 0px !important;
        position: relative;
        z-index: 1;
    }

    .article-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .article-card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }

    .article-card-img {
        width: 80px;
        height: 80px;
        object-fit: cover;
        border-radius: 4px;
        flex-shrink: 0;
    }

    .article-card-title {
        font-size: 1.1em;
        font-weight: bold;
        color: #0B3B73;
        margin: 0;
        flex-grow: 1;
    }

    .article-card-summary {
        font-size: 0.95em;
        color: #555;
        line-height: 1.5;
        margin-top: 5px;
        flex-grow: 1;
    }

    /* CSS for Streamlit button (Baca Artikel) */
    div[data-testid^="stButton"] > button {
        background-color: #0B3B73;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }

    /* Spacing between Streamlit columns */
    div[data-testid^="stHorizontalBlock"] > div[data-testid^="stVerticalBlock"] {
        margin-bottom: 20px;
    }
    
    /* CSS untuk penataan logo utama (jika logo sudah termasuk teks) */
    .app-logo-container {
        text-align: center; /* Untuk menengahkan logo gambar */
        margin-bottom: -20px; /* Tarik logo sedikit ke atas agar lebih dekat dengan jargon */
    }
    
    .app-logo {
        max-width: 250px; /* Atur lebar maksimum logo utama */
        height: auto;
        display: block; /* Agar margin auto bekerja untuk menengahkan */
        margin-left: auto;
        margin-right: auto;
    }

    /* Jargon di bawah logo utama */
    .app-jargon {
        text-align: center;
        font-size: 1.15rem;
        color: #666;
        margin-top: 0px; /* Mengatur jarak dari logo */
        margin-bottom: 3rem; /* Jarak ke konten berikutnya */
    }

    /* Custom CSS for sidebar logo */
    .sidebar-logo {
        width: 150px; /* Lebar logo di sidebar */
        display: block;
        margin: 10px auto 20px auto; /* Margin atas, samping auto (tengah), margin bawah */
    }

</style>
""", unsafe_allow_html=True)

class FishFreshnessClassifier:
    def __init__(self, model_path):
        """Inisialisasi model TensorFlow Lite."""
        try:
            if TFLITE_AVAILABLE:
                self.interpreter = Interpreter(model_path=model_path)
            else:
                self.interpreter = MinimalTFLiteInterpreter(model_path)
            
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.input_shape = self.input_details[0]['shape']
            self.input_height = self.input_shape[1]
            self.input_width = self.input_shape[2]
            self.class_labels = ['Fresh Fish', 'Non Fresh Fish']
        except Exception as e:
            st.error(f"Error saat memuat model: {str(e)}")
            self.interpreter = None
    
    def preprocess_image(self, image):
        """Pra-pemrosesan gambar untuk input model."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((self.input_width, self.input_height))
        image_array = np.array(image, dtype=np.float32) / 255.0
        return np.expand_dims(image_array, axis=0)
    
    def predict(self, image):
        """Melakukan prediksi pada gambar."""
        if self.interpreter is None: return None, None
        
        try:
            processed_image = self.preprocess_image(image)
            self.interpreter.set_tensor(self.input_details[0]['index'], processed_image)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            exp_values = np.exp(output_data[0] - np.max(output_data[0]))
            probabilities = exp_values / np.sum(exp_values)
            
            predicted_class_idx = np.argmax(probabilities)
            predicted_class = self.class_labels[predicted_class_idx]
            return predicted_class, probabilities
        except Exception as e:
            st.error(f"Error saat prediksi: {str(e)}")
            return None, None

def create_confidence_chart(probabilities, class_labels):
    """Membuat grafik batang untuk skor keyakinan."""
    fig = go.Figure(data=[go.Bar(
        x=class_labels, y=probabilities,
        marker_color=['#28a745' if prob == max(probabilities) else '#6c757d' for prob in probabilities],
        text=[f'{prob:.2%}' for prob in probabilities], textposition='auto',
    )])
    fig.update_layout(title="Visualisasi Skor Keyakinan", xaxis_title="Kelas", yaxis_title="Keyakinan", yaxis=dict(range=[0, 1]), height=400)
    return fig

# Fungsi untuk mengonversi gambar ke base64 (untuk logo)
def _get_image_as_base64(filepath):
    if not os.path.exists(filepath):
        st.error(f"Error: File logo tidak ditemukan di '{filepath}'. Pastikan file ada di folder yang sama dengan 'streamlit_app.py'.")
        return "" 
    with open(filepath, "rb") as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode("utf-8")


def main(): 
    # Path ke logo utama (ikon + teks) untuk header halaman utama
    main_logo_path = 'Logo.png'
    main_logo_base64 = _get_image_as_base64(main_logo_path)

    # Path ke logo sidebar (hanya teks)
    sidebar_logo_path = 'Logo-Name.png'
    sidebar_logo_base64 = _get_image_as_base64(sidebar_logo_path)
    
    @st.cache_resource
    def load_model(): return FishFreshnessClassifier("model.tflite")
    classifier = load_model()

    if "sample_image_path" not in st.session_state: st.session_state.sample_image_path = None
    if "page" not in st.session_state: st.session_state.page = "Aplikasi Klasifikasi"
    if "selected_article" not in st.session_state: st.session_state.selected_article = None 

    with st.sidebar:
        # Menampilkan logo teks di sidebar
        if sidebar_logo_base64:
            st.markdown(f'<img src="data:image/png;base64,{sidebar_logo_base64}" class="sidebar-logo">', unsafe_allow_html=True)
        else:
            st.title("ReFisher") # Fallback jika logo tidak ditemukan
        
        st.header("📋 Navigasi")
        # Tombol navigasi untuk halaman
        if st.button("🏡 Aplikasi Klasifikasi", use_container_width=True):
            st.session_state.page = "Aplikasi Klasifikasi"
            st.session_state.selected_article = None
        if st.button("📖 Panduan Penggunaan", use_container_width=True):
            st.session_state.page = "Panduan Penggunaan"
            st.session_state.selected_article = None
        if st.button("❓ FAQ", use_container_width=True):
            st.session_state.page = "FAQ"
            st.session_state.selected_article = None
        if st.button("📰 Artikel", use_container_width=True):
            st.session_state.page = "Artikel"
            st.session_state.selected_article = None

        st.markdown("---")
        st.markdown("<div class='info-card'><h4>Informasi Model</h4><p><strong>Sumber Data:</strong> Roboflow Universe</p><p><strong>Kelas:</strong> Fresh & Non Fresh</p><p><strong>Model:</strong> TensorFlow Lite</p></div>", unsafe_allow_html=True)
        # Pindahkan "Tentang Aplikasi ReFisher" ke sidebar
        st.markdown("---")
        with st.expander("ℹ️ Tentang Aplikasi ReFisher"):
            st.markdown(
                """
                Aplikasi ini menggunakan **Computer Vision** dan **Deep Learning** untuk mengklasifikasikan kesegaran ikan berdasarkan analisis citra.
                - **Backend**: Python, Streamlit
                - **Machine Learning**: TensorFlow Lite
                - **Dataset**: Roboflow Universe (Fresh and Non-Fresh Fish)
                """
            )
        st.markdown("---")
        # Checkbox show_details dipindahkan ke halaman utama
        if st.session_state.page == "Aplikasi Klasifikasi":
            show_details = st.checkbox("Tampilkan detail teknis", value=True)
            show_confidence = st.checkbox("Tampilkan grafik keyakinan", value=True)
            if 'show_details' not in st.session_state: st.session_state.show_details = True
            if 'show_confidence' not in st.session_state: st.session_state.show_confidence = True
            st.session_state.show_details = show_details
            st.session_state.show_confidence = show_confidence
            
    # Logika untuk menampilkan halaman yang berbeda
    if st.session_state.page == "Aplikasi Klasifikasi":
        page_klasifikasi_utama(classifier, main_logo_path, main_logo_base64)
    elif st.session_state.page == "Panduan Penggunaan":
        page_panduan_penggunaan()
    elif st.session_state.page == "FAQ":
        page_faq()
    elif st.session_state.page == "Artikel":
        page_articles()

    # Footer Section
    st.markdown("---") 
    st.markdown(
        """
        <div class="footer">
            © 2025 Refisher. All rights reserved.<br>
            Segarnya Ikan, Amannya Sajian Anda.
        </div>
        """,
        unsafe_allow_html=True
    )

# Fungsi untuk halaman utama aplikasi klasifikasi
def page_klasifikasi_utama(classifier, logo_path, logo_base64):
    # --- Pindahkan bagian header ke sini ---
    st.markdown(f"""
    <div class="app-logo-container">
        <img src="data:image/png;base64,{logo_base64}" class="app-logo" width="250">
    </div>
    <p class="app-jargon">Segarnya Ikan, Amannya Sajian Anda.</p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    # --- Akhir bagian header yang dipindahkan ---

    col1, col2 = st.columns([1, 1])
    image, caption = None, ""
    
    with col1:
        st.header("📤 Unggah Gambar untuk Analisis")
        st.info("💡 Anda juga bisa menemukan contoh gambar di halaman 'Panduan Penggunaan' di sidebar.")
        uploaded_file = st.file_uploader("Pilih gambar ikan (.png, .jpg, .jpeg)", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image, caption = Image.open(uploaded_file), "Gambar yang diunggah"
            st.session_state.sample_image_path = None
        elif st.session_state.sample_image_path:
            try:
                image, caption = Image.open(st.session_state.sample_image_path), f"Contoh: {os.path.basename(st.session_state.sample_image_path)}"
            except Exception as e:
                st.error(f"Gagal membuka gambar contoh: {e}")
                st.session_state.sample_image_path = None

        if image:
            st.image(image, caption=caption, use_container_width=True)
            st.subheader("🎨 Sesuaikan Kualitas Gambar")
            st.info("Gunakan slider ini untuk meningkatkan visibilitas detail ikan sebelum analisis.")
            enhance_contrast = st.slider("Kontras", 0.5, 2.0, 1.0, 0.1)
            enhance_brightness = st.slider("Kecerahan", 0.5, 2.0, 1.0, 0.1)
            
            if abs(enhance_contrast - 1.0) > 0.01 or abs(enhance_brightness - 1.0) > 0.01:
                enhanced_image = ImageEnhance.Contrast(image).enhance(enhance_contrast)
                enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(enhance_brightness)
                image = enhanced_image
                st.image(image, caption="Gambar setelah peningkatan kualitas", use_container_width=True)
    
    with col2:
        st.header("🤖 Hasil Analisis Kesegaran Ikan")
        if image:
            with st.spinner("🔄 Menganalisis gambar ikan..."):
                predicted_class, probabilities = classifier.predict(image)
            
            if predicted_class and probabilities is not None:
                confidence = max(probabilities)
                result_class = "fresh-fish" if predicted_class == "Fresh Fish" else "non-fresh-fish"
                result_icon = "🟢" if predicted_class == "Fresh Fish" else "🔴"
                recommendation = "Ikan terdeteksi dalam kondisi segar dan **layak konsumsi**." if predicted_class == "Fresh Fish" else "Ikan terdeteksi dalam kondisi **tidak segar** dan tidak layak konsumsi."
                
                st.markdown(f'<div class="prediction-box {result_class}"><h2>{result_icon} {predicted_class}</h2><h3>Keyakinan: {confidence:.2%}</h3><p>{recommendation}</p></div>', unsafe_allow_html=True)
                
                if st.session_state.get('show_details', True): 
                    st.subheader("📈 Detail Skor Keyakinan")
                    m_col1, m_col2 = st.columns(2)
                    m_col1.metric("Keyakinan Ikan Segar", f"{probabilities[0]:.2%}")
                    m_col2.metric("Keyakinan Ikan Tidak Segar", f"{probabilities[1]:.2%}")
                
                if st.session_state.get('show_confidence', True):
                    st.plotly_chart(create_confidence_chart(probabilities, classifier.class_labels), use_container_width=True)
                
            else:
                st.error("❌ Gagal melakukan prediksi. Pastikan gambar yang diunggah adalah gambar ikan yang jelas dan tidak buram.")
        else:
            st.info("📷 Silakan unggah gambar ikan atau pilih dari contoh di halaman Panduan Penggunaan untuk memulai klasifikasi.")


if __name__ == "__main__":
    main()