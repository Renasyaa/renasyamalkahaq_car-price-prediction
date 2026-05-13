"""
╔══════════════════════════════════════════════════════════════════════╗
║     CAR PRICE PREDICTION SYSTEM — Streamlit Deployment              ║
║     Simpan sebagai: app.py                                           ║
║     Jalankan: streamlit run app.py                                   ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os

# ──────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Car Price Prediction System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Modern Automotive Dashboard
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* ── Global Reset ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0e1a;
    color: #e8eaf0;
  }

  /* ── Hide default Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 2rem 3rem 2rem; max-width: 1280px; }
  .stDeployButton { display: none; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d1224 0%, #111827 100%);
    border-right: 1px solid rgba(99,102,241,0.25);
  }
  [data-testid="stSidebar"] .stMarkdown h2 {
    color: #818cf8;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    letter-spacing: 0.05em;
  }
  [data-testid="stSidebar"] label {
    color: #a5b4fc !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
  }
  [data-testid="stSidebar"] .stSlider > div > div > div {
    background: #4f46e5;
  }

  /* ── Hero ── */
  .hero-wrapper {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin: 1.5rem 0 2rem 0;
    position: relative;
    overflow: hidden;
  }
  .hero-wrapper::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-wrapper::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(167,139,250,0.15) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.5);
    color: #a5b4fc;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 50px;
    margin-bottom: 1rem;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #f0f4ff;
    line-height: 1.1;
    margin: 0 0 0.8rem 0;
    letter-spacing: -0.02em;
  }
  .hero-title span { color: #818cf8; }
  .hero-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.7;
    max-width: 600px;
    font-weight: 400;
  }

  /* ── Metric Cards ── */
  .metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
  }
  .metric-card {
    background: linear-gradient(145deg, #131929, #1a2035);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
  }
  .metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(99,102,241,0.5);
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
  }
  .metric-card.indigo::before  { background: linear-gradient(90deg, #6366f1, #818cf8); }
  .metric-card.violet::before  { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
  .metric-card.cyan::before    { background: linear-gradient(90deg, #0891b2, #22d3ee); }
  .metric-card.emerald::before { background: linear-gradient(90deg, #059669, #34d399); }
  .metric-icon {
    font-size: 1.6rem;
    margin-bottom: 0.7rem;
    display: block;
  }
  .metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.3rem;
  }
  .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1;
  }
  .metric-sub {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.25rem;
  }

  /* ── Section Titles ── */
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.01em;
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,0.4), transparent);
    margin-left: 0.8rem;
  }

  /* ── Form Panel ── */
  .form-panel {
    background: linear-gradient(145deg, #111827, #1a2035);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 2rem;
  }
  .form-desc {
    color: #64748b;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    padding: 0.9rem 1rem;
    background: rgba(99,102,241,0.06);
    border-left: 3px solid #6366f1;
    border-radius: 0 8px 8px 0;
  }

  /* ── Predict Button ── */
  .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
    margin-top: 0.5rem !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(99,102,241,0.6) !important;
  }
  .stButton > button:active {
    transform: translateY(0px) !important;
  }

  /* ── Result Card ── */
  .result-card {
    background: linear-gradient(135deg, #1e1b4b, #1a2035);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 16px;
    padding: 2.2rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
  }
  .result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
  }
  .result-price-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 0.5rem;
  }
  .result-price {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0f4ff;
    line-height: 1;
    margin-bottom: 0.4rem;
  }
  .result-price sub {
    font-size: 1.2rem;
    color: #818cf8;
    font-weight: 600;
  }
  .result-context {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 0.5rem;
  }
  .spec-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(99,102,241,0.1);
  }
  .spec-key {
    font-size: 0.8rem;
    color: #64748b;
    font-weight: 500;
  }
  .spec-val {
    font-size: 0.85rem;
    color: #c7d2fe;
    font-weight: 600;
  }
  .insight-box {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-top: 1.2rem;
    font-size: 0.85rem;
    color: #6ee7b7;
    line-height: 1.6;
  }

  /* ── Model Info Card ── */
  .model-card {
    background: linear-gradient(145deg, #111827, #131929);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 14px;
    padding: 1.6rem;
  }
  .model-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #818cf8;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 50px;
    margin-bottom: 0.8rem;
    border: 1px solid rgba(99,102,241,0.3);
  }
  .model-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }
  .model-stat-key { font-size: 0.82rem; color: #64748b; }
  .model-stat-val { font-size: 0.88rem; font-weight: 600; color: #a5b4fc; }

  /* ── Footer ── */
  .footer-card {
    background: linear-gradient(135deg, #0d1224, #111827);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin-top: 3rem;
  }
  .footer-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.3rem;
  }
  .footer-detail {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.8;
  }

  /* ── Streamlit component overrides ── */
  .stSelectbox > div > div {
    background: #1a2035 !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
  }
  .stNumberInput > div > div > input,
  .stTextInput > div > div > input {
    background: #1a2035 !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
  }
  div[data-testid="stSlider"] > div > div > div > div {
    background: #6366f1 !important;
  }

  /* Divider */
  hr { border-color: rgba(99,102,241,0.15) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# LOAD MODEL & DATA
# ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load('car_price_model.pkl')
    le    = joblib.load('label_encoder.pkl')
    return model, le

@st.cache_data
def load_metadata():
    with open('model_metadata.json') as f:
        return json.load(f)

try:
    model, le = load_model()
    meta      = load_metadata()
    MODEL_OK  = True
except Exception as e:
    MODEL_OK  = False
    st.error(f" Model tidak ditemukan. Pastikan `car_price_model.pkl`, `label_encoder.pkl`, dan `model_metadata.json` ada di folder yang sama dengan `app.py`.\n\nError: {e}")


# ──────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="
    font-size:1.55rem;
    font-weight:700;
    color:#818cf8;
    margin-bottom:0.3rem;
">
Input Spesifikasi
</div>
""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("Gunakan slider dan dropdown di bawah untuk memasukkan spesifikasi kendaraan yang ingin diprediksi harganya.")
    st.markdown("---")

    engine_size = st.slider(
        " Engine Size (Liter)",
        min_value=1.0, max_value=6.0, value=2.4, step=0.1,
        help="Kapasitas mesin dalam liter"
    )
    horsepower = st.slider(
        " Horsepower (HP)",
        min_value=70, max_value=400, value=150, step=5,
        help="Tenaga mesin dalam satuan Horse Power"
    )
    fuel_capacity = st.slider(
        " Fuel Capacity (Galon)",
        min_value=10.0, max_value=35.0, value=15.0, step=0.5,
        help="Kapasitas tangki bahan bakar"
    )
    fuel_efficiency = st.slider(
        " Fuel Efficiency (MPG)",
        min_value=10, max_value=50, value=27, step=1,
        help="Jarak yang ditempuh per galon bahan bakar"
    )
    vehicle_type = st.selectbox(
        " Vehicle Type",
        options=["Passenger", "Car"],
        help="Jenis kendaraan: Passenger (sedan/city car) atau Car (SUV/pickup)"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#475569; line-height:1.8;'>
    <strong style='color:#818cf8;'>Panduan Input:</strong><br>
    • <b>Sedan/City Car</b>: Engine 1.5–2.5L, 90–160 HP<br>
    • <b>SUV/MPV</b>: Engine 2.5–4.0L, 160–250 HP<br>
    • <b>Pickup/Truck</b>: Engine 3.5–5.5L, 200–350 HP<br>
    • <b>Sport Car</b>: Engine 2.0–4.5L, 200–400 HP
    </div>
    """, unsafe_allow_html=True)

    predict_btn = st.button(" PREDIKSI HARGA", use_container_width=True)


# ──────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────────────────────────────

# ── HERO ──
st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge"> Sains Data · Linear Regression · CRISP-DM</div>
  <h1 class="hero-title">Car Price<br><span>Prediction System</span></h1>
  <p class="hero-sub">
    Sistem prediksi harga mobil untuk membantu perusahaan otomotif menentukan spesifikasi dan harga kendaraan yang kompetitif sesuai tren pasar.
  </p>
</div>
""", unsafe_allow_html=True)


# ── DASHBOARD METRICS ──
st.markdown('<div class="section-title"> Dashboard Insight Pasar</div>', unsafe_allow_html=True)

if MODEL_OK:
    avg_price    = meta.get('avg_price', 27.39)
    total_data   = meta.get('total_data', 155)
    top_car      = meta.get('top_car', 'Ford F-Series')
    top_sales    = meta.get('top_sales', 540.6)
    r2_val       = meta.get('r2_score', 0.71)
else:
    avg_price, total_data, top_car, top_sales, r2_val = 27.39, 155, 'Ford F-Series', 540.6, 0.71

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card indigo">
    <span class="metric-icon"> </span>
    <div class="metric-label">Mobil Paling Laris</div>
    <div class="metric-value" style="font-size:1.2rem;">{top_car}</div>
    <div class="metric-sub">{top_sales:,.1f}K unit terjual</div>
  </div>
  <div class="metric-card violet">
    <span class="metric-icon"> </span>
    <div class="metric-label">Rata-rata Harga Pasar</div>
    <div class="metric-value">${avg_price:.1f}K</div>
    <div class="metric-sub">≈ ${avg_price*1000:,.0f} USD</div>
  </div>
  <div class="metric-card cyan">
    <span class="metric-icon"> </span>
    <div class="metric-label">Total Data Kendaraan</div>
    <div class="metric-value">{total_data}</div>
    <div class="metric-sub">model kendaraan unik</div>
  </div>
  <div class="metric-card emerald">
    <span class="metric-icon"> </span>
    <div class="metric-label">Akurasi Model (R²)</div>
    <div class="metric-value">{r2_val*100:.1f}%</div>
    <div class="metric-sub">variansi harga dijelaskan</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── PREDICTION SECTION ──
st.markdown('<div class="section-title"> Prediksi Harga Kendaraan</div>', unsafe_allow_html=True)

col_form, col_result = st.columns([1.05, 1], gap="large")

with col_form:
    st.markdown("""
    <div class="form-panel">
      <div class="form-desc">
        Masukkan spesifikasi kendaraan menggunakan <strong>panel sidebar (kiri)</strong> untuk memperkirakan
        harga pasar kendaraan. Sesuaikan nilai Engine Size, Horsepower, Fuel Capacity,
        Fuel Efficiency, dan jenis kendaraan, kemudian tekan tombol <strong>Prediksi Harga</strong>.
      </div>
    """, unsafe_allow_html=True)

    st.markdown("**Spesifikasi yang akan diprediksi:**")

    c1, c2 = st.columns(2)
    with c1:
        st.metric(" Engine Size",    f"{engine_size:.1f} L")
        st.metric(" Fuel Capacity",  f"{fuel_capacity:.1f} Galon")
    with c2:
        st.metric(" Horsepower",     f"{horsepower} HP")
        st.metric(" Fuel Efficiency",f"{fuel_efficiency} MPG")

    st.metric(" Vehicle Type", vehicle_type)
    st.markdown("</div>", unsafe_allow_html=True)


with col_result:
    if predict_btn and MODEL_OK:
        # Encode vehicle type
        v_encoded = 1 if vehicle_type == "Passenger" else 0

        input_df = pd.DataFrame({
            'Engine_size':    [engine_size],
            'Horsepower':     [float(horsepower)],
            'Fuel_capacity':  [fuel_capacity],
            'Fuel_efficiency':[float(fuel_efficiency)],
            'Vehicle_type':   [v_encoded]
        })

        predicted_price = model.predict(input_df)[0]
        predicted_usd   = predicted_price * 1000
        predicted_idr   = predicted_usd * 17500          # ← konversi ke Rupiah (kurs tetap Rp17.500/USD)

        # Generate insight
        if predicted_price < 15:
            segment = "Budget / Economy"
            insight = "Kendaraan ini berada di segmen ekonomi. Cocok untuk pasar konsumen muda dan pengguna perkotaan yang mencari nilai terbaik dengan harga terjangkau."
            seg_color = "#34d399"
        elif predicted_price < 30:
            segment = "Mid-Range / Family"
            insight = "Segmen mid-range adalah yang paling laris di pasar. Kendaraan ini bersaing langsung dengan Toyota Camry dan Honda Accord — dua model terlaris secara konsisten."
            seg_color = "#60a5fa"
        elif predicted_price < 50:
            segment = "Premium / Upper-Mid"
            insight = "Segmen premium menawarkan margin profitabilitas lebih tinggi. Konsumen di segmen ini mengutamakan performa dan kenyamanan dibanding harga semata."
            seg_color = "#a78bfa"
        else:
            segment = "Luxury / High-End"
            insight = "Kendaraan mewah memiliki pasar yang lebih kecil namun menguntungkan. Strategi pemasaran harus menekankan eksklusivitas, teknologi, dan brand prestige."
            seg_color = "#f59e0b"

        st.markdown(f"""
        <div class="result-card">
          <div class="result-price-label">⬆ Estimasi Harga Pasar Kendaraan</div>

          <div class="result-price">
            Rp{predicted_idr:,.0f}
          </div>
          <div style="font-size:1.35rem; color:#94a3b8; font-weight:500; margin:0.3rem 0;">
            ≈ <strong style="color:#c7d2fe;">${predicted_usd:,.0f}</strong> USD
          </div>
          <div style="font-size:0.75rem; color:#475569; margin-top:0.2rem; letter-spacing:0.05em;">
            Kurs: Rp17.500 / USD
          </div>

          <hr style="margin:1rem 0!important;">

          <div style="margin-bottom:0.8rem;">
            <span class="model-badge" style="background:rgba({seg_color[1:]},0.15); color:{seg_color}; border-color:{seg_color}40;">
              {segment}
            </span>
          </div>

          <div class="spec-row">
            <span class="spec-key">Engine Size</span>
            <span class="spec-val">{engine_size:.1f} L</span>
          </div>
          <div class="spec-row">
            <span class="spec-key">Horsepower</span>
            <span class="spec-val">{horsepower} HP</span>
          </div>
          <div class="spec-row">
            <span class="spec-key">Fuel Capacity</span>
            <span class="spec-val">{fuel_capacity:.1f} Galon</span>
          </div>
          <div class="spec-row">
            <span class="spec-key">Fuel Efficiency</span>
            <span class="spec-val">{fuel_efficiency} MPG</span>
          </div>
          <div class="spec-row" style="border-bottom:none;">
            <span class="spec-key">Vehicle Type</span>
            <span class="spec-val">{vehicle_type}</span>
          </div>

          <div class="insight-box">
            <strong>Market Insight:</strong><br>{insight}
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif predict_btn and not MODEL_OK:
        st.error("Model tidak tersedia. Pastikan file .pkl sudah ada.")
    else:
        st.markdown("""
        <div style="
          background: linear-gradient(145deg, #111827, #1a2035);
          border: 2px dashed rgba(99,102,241,0.25);
          border-radius: 16px;
          padding: 3rem 2rem;
          text-align: center;
          color: #475569;
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        ">
          <div style="font-size: 3.5rem; margin-bottom: 1rem; opacity: 0.5;">🚗</div>
          <div style="font-size: 1rem; font-weight: 600; color: #64748b; margin-bottom: 0.5rem;">
            Siap Memprediksi
          </div>
          <div style="font-size: 0.82rem; color: #64748b; line-height: 1.6; max-width: 250px;">
            Atur spesifikasi kendaraan di sidebar kiri, lalu tekan
            <strong style="color:#818cf8;">Prediksi Harga</strong> untuk melihat estimasi harga pasar.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── MODEL INFO & EVALUATION ──
st.markdown('<div class="section-title"> Tentang Model & Evaluasi</div>', unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)

if MODEL_OK:
    rmse_val = meta.get('rmse', 9.5)
    r2_pct   = meta.get('r2_score', 0.71) * 100
    n_train  = meta.get('n_training', 123)
    n_test   = meta.get('n_testing', 32)
else:
    rmse_val, r2_pct, n_train, n_test = 9.5, 71, 123, 32

with col_m1:
    st.markdown(f"""
    <div class="model-card">
      <div class="model-badge">Algoritma</div>
      <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800; color:#e2e8f0; margin-bottom:0.8rem;">
        Linear Regression
      </div>
      <div class="model-stat">
        <span class="model-stat-key">Training Data</span>
        <span class="model-stat-val">{n_train} sampel (80%)</span>
      </div>
      <div class="model-stat">
        <span class="model-stat-key">Testing Data</span>
        <span class="model-stat-val">{n_test} sampel (20%)</span>
      </div>
      <div class="model-stat">
        <span class="model-stat-key">Dataset</span>
        <span class="model-stat-val">Car Sales (.xls)</span>
      </div>
      <div class="model-stat" style="border:none;">
        <span class="model-stat-key">Framework</span>
        <span class="model-stat-val">scikit-learn</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="model-card">
      <div class="model-badge">Metrik Evaluasi</div>
      <div style="text-align:center; padding:0.5rem 0 1rem 0;">
        <div style="font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800; color:#6ee7b7;">{r2_pct:.1f}%</div>
        <div style="font-size:0.75rem; color:#64748b; letter-spacing:0.08em;">R² SCORE</div>
      </div>
      <div class="model-stat">
        <span class="model-stat-key">RMSE</span>
        <span class="model-stat-val">${rmse_val:.3f}K</span>
      </div>
      <div class="model-stat" style="border:none;">
        <span class="model-stat-key">Rata-rata Error</span>
        <span class="model-stat-val">≈ ${rmse_val*1000:,.0f} USD</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div class="model-card">
      <div class="model-badge">Fitur Prediktor</div>
      <div style="margin-top:0.5rem;">
        {''.join([
          f'<div class="model-stat"><span class="model-stat-key">✦ {f}</span></div>'
          for f in ['Engine Size (L)', 'Horsepower (HP)', 'Fuel Capacity (Gal)', 'Fuel Efficiency (MPG)', 'Vehicle Type']
        ])}
        <div class="model-stat" style="border:none; margin-top:0.5rem;">
          <span class="model-stat-key">Target</span>
          <span class="model-stat-val">Price (USD×1000)</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ──
st.markdown("""
<div class="footer-card">
  <div style="font-size:1.5rem; margin-bottom:0.8rem;">🚗</div>
  <div class="footer-name">Renasya Malkahaq</div>
  <div class="footer-detail">
    NPM : 237006007<br>
    Program Studi Informatika · Universitas Siliwangi<br>
    Final Project Mata kuliah Sains Data · 2026
  </div>
  <div style="margin-top:1.2rem; font-size:0.72rem; color:#334155; letter-spacing:0.08em;">
    BUILT WITH PYTHON · SCIKIT-LEARN · STREAMLIT · CRISP-DM METHODOLOGY
  </div>
</div>
""", unsafe_allow_html=True)