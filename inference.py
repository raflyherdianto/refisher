import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('best_vgg_model.keras')
    return model

model = load_model()

class_names = ['Fresh', 'Tidak Fresh']

# Set UI
st.title("Klasifikasi Gambar Mata Ikan")
st.write("Upload gambar mata ikan (format .jpg/.jpeg/.png) untuk diklasifikasikan:")

uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Gambar yang Diupload', use_container_width=True)

    # Preprocessing gambar untuk inference
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0  # Normalisasi sesuai dengan train_datagen
    img_array = np.expand_dims(img_array, axis=0) # Tambah batch dimensi

    # Prediksi
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    predicted_class = class_names[predicted_class_index]
    confidence = prediction[0][predicted_class_index]

    # Hasil
    st.markdown("### Hasil Prediksi:")
    st.write(f"**Kelas:** {predicted_class}")
    st.write(f"**Kepercayaan:** {confidence:.2%}")