# 🚗 Car Price Prediction System
**Final Project — Matakuliah Sains Data**  
Metode: CRISP-DM | Model: Linear Regression | Framework: Streamlit

---

## 📁 Struktur Folder Project

```
car-price-prediction/
│
├── app.py                    ← Aplikasi web Streamlit (UTAMA)
├── car_price_model.pkl       ← Model Linear Regression (download dari Colab)
├── label_encoder.pkl         ← Label encoder untuk Vehicle_type (download dari Colab)
├── model_metadata.json       ← Metadata dan metrik model (download dari Colab)
├── requirements.txt          ← Daftar library yang dibutuhkan
├── README.md                 ← Panduan ini
│
└── assets/                   ← (Opsional) Gambar/logo tambahan
```

---

## 🔄 Alur Workflow Deployment

```
Google Colab                     VS Code / Local          Streamlit Cloud
──────────────                   ─────────────────        ───────────────
1. Analisis EDA        ──→       4. Copy file .pkl   ──→  7. Push ke GitHub
2. Training Model                5. Buat app.py           8. Connect repo
3. Simpan .pkl files  ──→       6. Test local            9. Deploy online
                       download
```

---

## 🚀 Langkah 1: Persiapan di Google Colab

1. Buka [Google Colab](https://colab.research.google.com)
2. Upload file `Final_Project_Car_Price_Prediction_COLAB.py` sebagai notebook baru
   - Atau copy-paste isi file tersebut ke cell-cell di Colab
3. Upload file `Car_sales.xls` ke Colab:
   ```python
   from google.colab import files
   uploaded = files.upload()  # Pilih Car_sales.xls
   ```
4. Jalankan semua cell secara berurutan dari atas ke bawah
5. Di cell terakhir (Save Model), tiga file akan otomatis terdownload:
   - `car_price_model.pkl`
   - `label_encoder.pkl`
   - `model_metadata.json`

---

## 💻 Langkah 2: Setup Lokal di VS Code

### 2.1 Buat folder project
```bash
mkdir car-price-prediction
cd car-price-prediction
```

### 2.2 Pindahkan semua file ke folder ini
```
car-price-prediction/
├── app.py                  ← dari file yang disediakan
├── car_price_model.pkl     ← hasil download dari Colab
├── label_encoder.pkl       ← hasil download dari Colab
├── model_metadata.json     ← hasil download dari Colab
└── requirements.txt        ← dari file yang disediakan
```

### 2.3 Buat Virtual Environment (disarankan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.4 Install semua library
```bash
pip install -r requirements.txt
```

---

## ▶️ Langkah 3: Jalankan Aplikasi Streamlit

```bash
streamlit run app.py
```

Setelah perintah dijalankan, buka browser dan akses:
```
http://localhost:8501
```

Untuk menghentikan server: tekan `Ctrl + C` di terminal.

---

## 🌐 Langkah 4: Deployment ke Streamlit Community Cloud (Online)

### 4.1 Buat akun GitHub
Daftar di [github.com](https://github.com) jika belum punya akun.

### 4.2 Buat repository baru
1. Klik tombol **"New"** di GitHub
2. Nama repository: `car-price-prediction`
3. Set **Public**
4. Klik **"Create repository"**

### 4.3 Upload file ke GitHub
**Cara 1 — Via Web GitHub (mudah):**
1. Buka repository yang baru dibuat
2. Klik **"Add file"** → **"Upload files"**
3. Drag & drop semua file:
   - `app.py`
   - `car_price_model.pkl`
   - `label_encoder.pkl`
   - `model_metadata.json`
   - `requirements.txt`
4. Klik **"Commit changes"**

**Cara 2 — Via Git (lebih profesional):**
```bash
cd car-price-prediction
git init
git add .
git commit -m "Initial commit: Car Price Prediction System"
git branch -M main
git remote add origin https://github.com/USERNAME/car-price-prediction.git
git push -u origin main
```

### 4.4 Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih:
   - **Repository**: `USERNAME/car-price-prediction`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Klik **"Deploy!"**
6. Tunggu 2–5 menit hingga proses selesai
7. Aplikasi Anda akan live di:
   ```
   https://USERNAME-car-price-prediction-app-XXXXXX.streamlit.app
   ```

---

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` |
| Model tidak ditemukan | Pastikan `.pkl` ada di folder yang sama dengan `app.py` |
| Port 8501 sudah dipakai | Jalankan `streamlit run app.py --server.port 8502` |
| Streamlit Cloud error | Cek `requirements.txt`, pastikan semua versi kompatibel |
| File .pkl terlalu besar | Compress dengan `joblib.dump(model, 'model.pkl', compress=3)` |

---

## 📊 Informasi Model

| Komponen | Detail |
|----------|--------|
| Algoritma | Linear Regression (scikit-learn) |
| Fitur Input | Engine Size, Horsepower, Fuel Capacity, Fuel Efficiency, Vehicle Type |
| Target Output | Harga Mobil (dalam ribuan USD) |
| Pembagian Data | 80% Training / 20% Testing |
| Evaluasi | RMSE & R² Score |

---

## 👤 Informasi Mahasiswa

> **GANTI INFORMASI INI** di bagian footer pada file `app.py` (baris terakhir)

```python
# Cari bagian ini di app.py dan sesuaikan:
NAMA        LENGKAP ANDA         ← Ganti dengan nama Anda
NPM : 12345678XX                 ← Ganti dengan NPM Anda
Universitas Anda                 ← Ganti dengan nama universitas
Final Project · 2026             ← Sesuaikan tahun
```

---

*Final Project Matakuliah Sains Data · CRISP-DM Methodology*
