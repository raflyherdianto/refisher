<div align="center">
  <img src="https://i.imgur.com/auG5p6C.png" alt="Laskar AI Logo" width="200"/>
  <h1><b>Project Capstone LaskarAI</b></h1>
  <p><i>Sebuah inisiatif untuk masa depan AI Indonesia yang lebih cerah!</i></p>
</div>

**Laskar AI** adalah program beasiswa bergengsi, sebuah inisiatif dari **Lintasarta** yang berkolaborasi dengan **Dicoding** dan **NVIDIA**. Program ini dirancang khusus untuk mencetak talenta-talenta digital terbaik Indonesia yang tidak hanya mampu mengadopsi, tetapi juga mengembangkan teknologi AI untuk menciptakan solusi inovatif demi menyongsong **Indonesia Emas 2045**.

Program ini memberikan pelatihan intensif di bidang _Machine Learning_ & _Data Science_ sebagai fondasi utama pengembangan AI. Melalui program **AI Nation**, Lintasarta menunjukkan komitmennya dalam membangun ekosistem digital yang kuat. Sebagai perusahaan ICT _total solution_ dengan pengalaman lebih dari 36 tahun, Lintasarta secara konsisten berkontribusi dalam meningkatkan literasi dan keterampilan teknologi generasi muda Indonesia.

**Disponsori dan Didukung oleh:**

| | | |
| :---: | :---: | :---: |
| <img src="https://i.imgur.com/Af8lVk5.png" alt="Lintasarta Logo" width="150"> | <img src="https://i.imgur.com/HYG4mYW.png" alt="Dicoding Logo" width="150"> | <img src="https://i.imgur.com/B6Ash0H.png" alt="NVIDIA Logo" width="120"> |
| **Lintasarta** | **Dicoding** | **NVIDIA** |

---

# 🐟 ReFisher: Deteksi Kesegaran Ikan dengan AI

Selamat datang di **ReFisher**! ✨ Proyek ini memanfaatkan kekuatan _Deep Learning_ untuk mengklasifikasi kesegaran ikan berdasarkan citra. Model yang kami kembangkan dapat membedakan antara ikan segar dan tidak segar, sebuah langkah awal yang menjanjikan untuk otomatisasi kontrol kualitas di industri perikanan.

## 👥 Anggota Tim

Proyek ini adalah hasil kolaborasi dari talenta-talenta berbakat dari berbagai universitas di Indonesia:

| Anggota Tim | ID | Universitas |
| :--- | :---: | :---: |
| **Eldy Eﬀendi** | `A288YBF142` | <img src="https://i.imgur.com/Acvbhyx.png" alt="Universitas Pamulang" width="50"> <br> Universitas Pamulang |
| **Ahmad Kholish Fauzan Shobiry**| `A006YBF028` | <img src="https://i.imgur.com/5jzhjFI.png" alt="Universitas Brawijaya" width="50"> <br> Universitas Brawijaya |
| **Mochammad Raﬂy Herdianto** | `A131YBF282` | <img src="https://i.imgur.com/soJPlVs.png" alt="Politeknik Negeri Malang" width="50"> <br> Politeknik Negeri Malang |
| **Nurindra Rusmana** | `A013XBM383` | <img src="https://i.imgur.com/JwHbAqL.png" alt="Universitas Terbuka" width="50"> <br> Universitas Terbuka |

## ✨ Fitur Utama

* **Klasifikasi Biner**: Model dapat membedakan antara 2 kelas: `fresh` (segar) dan `non-fresh fish` (tidak segar).
* **Arsitektur CNN**: Dibangun menggunakan arsitektur _Convolutional Neural Network_ (CNN) sederhana namun efektif dengan TensorFlow/Keras.
* **Akurasi Tinggi**: Model mencapai akurasi yang baik pada data validasi dan data uji, menunjukkan kemampuannya untuk generalisasi.
* **Siap Pakai**: Model diekspor ke berbagai format (`.tflite`, dan `TFJS`) untuk kemudahan implementasi di berbagai platform.
* **Kolaborasi Terbuka**: Proyek ini dikelola dengan Git dan terbuka untuk kontribusi.

## 🚀 Aplikasi Streamlit

Kami telah mengembangkan aplikasi web interaktif menggunakan **Streamlit** untuk mendemonstrasikan kemampuan model kami secara langsung.

* **Akses Aplikasi**: [**refisher.streamlit.app**](https://refisher.streamlit.app/)
* **Branch Pengembangan**: Lihat kode aplikasi di branch [**development**](https://github.com/raflyherdianto/refisher/tree/development).

## 🛠️ Struktur Branch & Model

Proyek ini mengeksplorasi beberapa arsitektur model yang dikembangkan secara paralel di *branch* yang berbeda:

| Branch | Model yang Dikembangkan | Deskripsi |
| :---: | :---: | :--- |
| [**`Eldy`**](https://github.com/raflyherdianto/refisher/tree/eldy) | **MobileNetV2** | Model yang ringan dan efisien, cocok untuk perangkat mobile. |
| [**`Kholish`**](https://github.com/raflyherdianto/refisher/tree/kholish)| **VGG16** | Arsitektur klasik yang dikenal dengan kedalaman dan performanya. |
| [**`Nuri`**](https://github.com/raflyherdianto/refisher/tree/nuri) | **Custom CNN** | Model CNN yang dibangun dari awal untuk tugas spesifik ini. |
| [**`Rafly`**](https://github.com/raflyherdianto/refisher/tree/rafly) | **ResNet50V2** | Model dengan koneksi residual untuk mengatasi masalah *vanishing gradient*. |

## 📊 Dataset

Dataset yang digunakan dibagi menjadi tiga bagian untuk memastikan proses pelatihan dan evaluasi yang solid:

* **Data Latih (Train)**: Terdiri dari 3007 gambar.
* **Data Validasi (Validation)**: Terdiri dari 859 gambar.
* **Data Uji (Test)**: Terdiri dari 426 gambar.

Semua gambar di-preprocess dengan normalisasi (skala 1./255) sebelum dimasukkan ke dalam model.

## 📈 Pelatihan & Evaluasi (Contoh dari Branch `Nuri`)

Setiap model dilatih secara terpisah. Sebagai contoh, berikut adalah hasil dari model CNN kustom:

Model dilatih selama maksimal 20 *epoch* dengan *callback* `EarlyStopping` yang memonitor `val_accuracy`.

| Metrik | Nilai |
| --- | --- |
| **Akurasi Latih** | ~94.88% |
| **Akurasi Validasi**| ~93.83% |
| **Akurasi Uji** | **~92.96%** |
| **Loss Uji** | ~0.2372 |

_Sumber: Hasil evaluasi dari file nurind.ipynb di branch Nuri._

**Grafik Akurasi dan Loss per Epoch:**
![Grafik Hasil Training](https://i.imgur.com/rDJ1fwm.png)

## 📦 Aset Model

Folder `model_development` di setiap *branch* berisi aset yang relevan, termasuk:

1.  **Notebook `.ipynb`**: Berisi seluruh proses dari pemuatan data hingga pelatihan.
2.  **`model.tflite`**: Model dalam format TensorFlow Lite.
3.  **`tfjs_model/`**: Model dalam format TensorFlow.js.

Anda dapat meng-clone repositori ini dan menjelajahi setiap *branch* untuk melihat implementasi model yang berbeda.