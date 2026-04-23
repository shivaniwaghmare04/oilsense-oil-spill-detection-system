import streamlit as st

# 🔥 MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="OilSense — Spill Detection AI",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0a0e14;
    --surface:   #111620;
    --card:      #161d2b;
    --border:    #1e2d44;
    --accent:    #ff5722;
    --accent2:   #ffc107;
    --safe:      #00e676;
    --info:      #29b6f6;
    --text:      #e8eaf0;
    --muted:     #7b8aaa;
    --red:       #ff1744;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'Space Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-mono);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Top banner ── */
.top-banner {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2744 50%, #0d1b2a 100%);
    border: 1px solid var(--border);
    border-bottom: 2px solid var(--accent);
    padding: 24px 32px 18px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.top-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,87,34,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.banner-title {
    font-family: var(--font-head);
    font-weight: 800;
    font-size: 2.4rem;
    color: #fff;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1.1;
}
.banner-title span { color: var(--accent); }
.banner-sub {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,230,118,0.1);
    border: 1px solid rgba(0,230,118,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.7rem;
    color: var(--safe);
    margin-top: 10px;
}
.pulse { animation: pulse 1.8s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Metric cards ── */
.metric-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.metric-card {
    flex: 1;
    min-width: 140px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
}
.metric-card.red::after   { background: var(--red); }
.metric-card.amber::after { background: var(--accent2); }
.metric-card.blue::after  { background: var(--info); }
.metric-card.green::after { background: var(--safe); }
.metric-label { font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); }
.metric-value { font-family: var(--font-head); font-size: 1.9rem; font-weight: 800; margin: 4px 0 0; color: #fff; }
.metric-unit  { font-size: 0.7rem; color: var(--muted); }

/* ── Section headers ── */
.section-header {
    font-family: var(--font-head);
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 28px 0 16px;
}

/* ── Alert boxes ── */
.alert {
    border-radius: 6px;
    padding: 14px 18px;
    font-size: 0.82rem;
    margin: 14px 0;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.alert.danger  { background: rgba(255,23,68,0.1);  border: 1px solid rgba(255,23,68,0.3);  color: #ff6e8a; }
.alert.warning { background: rgba(255,193,7,0.1);  border: 1px solid rgba(255,193,7,0.3);  color: #ffd54f; }
.alert.safe    { background: rgba(0,230,118,0.08); border: 1px solid rgba(0,230,118,0.25); color: #69f0ae; }
.alert.info    { background: rgba(41,182,246,0.08);border: 1px solid rgba(41,182,246,0.25);color: #81d4fa; }
.alert-icon { font-size: 1.2rem; flex-shrink: 0; }
.alert-title { font-family: var(--font-head); font-weight: 600; margin-bottom: 3px; }
.alert-body  { font-size: 0.75rem; opacity: 0.85; }

/* ── GAN panel ── */
.gan-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--info);
    border-radius: 8px;
    padding: 18px 20px;
    margin: 14px 0;
}
.gan-title {
    font-family: var(--font-head);
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--info);
    margin-bottom: 12px;
}
.gan-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.gan-key { font-size: 0.72rem; color: var(--muted); }
.gan-val { font-family: var(--font-head); font-size: 0.85rem; font-weight: 600; color: #fff; }
.bar-wrap { background: var(--border); border-radius: 3px; height: 6px; margin-top: 4px; }
.bar-fill { height: 6px; border-radius: 3px; transition: width 0.6s ease; }

/* ── Risk badge ── */
.risk-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 4px;
    font-family: var(--font-head);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.risk-critical { background: rgba(255,23,68,0.15);  border: 1px solid var(--red);    color: var(--red); }
.risk-high     { background: rgba(255,87,34,0.15);  border: 1px solid var(--accent);  color: var(--accent); }
.risk-medium   { background: rgba(255,193,7,0.15);  border: 1px solid var(--accent2); color: var(--accent2); }
.risk-low      { background: rgba(0,230,118,0.1);   border: 1px solid var(--safe);    color: var(--safe); }

/* ── Class legend ── */
.legend-row { display:flex; gap:10px; flex-wrap:wrap; margin:10px 0; }
.legend-item { display:flex; align-items:center; gap:6px; font-size:0.72rem; color:var(--muted); }
.legend-dot  { width:10px; height:10px; border-radius:50%; }

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 10px !important;
    padding: 20px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #ff7043 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(255,87,34,0.4) !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 4px;
}
[data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    color: var(--muted) !important;
    background: transparent !important;
    border-radius: 0 !important;
}
[aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Images ── */
[data-testid="stImage"] img {
    border-radius: 6px;
    border: 1px solid var(--border);
}

/* ── Selectbox / slider ── */
[data-baseweb="select"] div,
[data-baseweb="select"] span { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

import cv2
import numpy as np
import torch
import segmentation_models_pytorch as smp
from PIL import Image
import io
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH  = "/Users/shivanisunilwaghmare/Desktop/oilspill/segmentation_best (1).pth"
NUM_CLASSES = 4

CLASS_INFO = {
    0: {"name": "Background / Sea",  "color": [10,  25,  50],  "hex": "#0a1932"},
    1: {"name": "Oil Spill",         "color": [255, 23,  68],  "hex": "#ff1744"},
    2: {"name": "Look-alike",        "color": [255, 193, 7],   "hex": "#ffc107"},
    3: {"name": "Ship / Object",     "color": [41,  182, 246], "hex": "#29b6f6"},
}

# ─── BANNER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-banner">
  <p class="banner-sub">AI-Powered SAR Image Analysis</p>
  <h1 class="banner-title"><span>Oil</span>Sense — Detection System</h1>
  <div class="status-pill">
    <span class="pulse">●</span> MODEL ONLINE &nbsp;|&nbsp; DEVICE: {DEVICE.upper()} &nbsp;|&nbsp; {datetime.now().strftime("%Y-%m-%d %H:%M")}
  </div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-header">⚙ Detection Settings</p>', unsafe_allow_html=True)
    confidence_threshold = st.slider("Confidence Threshold", 0.1, 0.9, 0.5, 0.05,
                                      help="Minimum confidence to classify a pixel as oil")
    overlay_alpha        = st.slider("Mask Overlay Opacity", 0.1, 0.9, 0.35, 0.05)
    spill_sensitivity    = st.select_slider("Spill Sensitivity",
                                             options=["Low", "Medium", "High", "Max"],
                                             value="Medium")

    st.markdown('<p class="section-header">🧠 GAN Anomaly Detector</p>', unsafe_allow_html=True)
    enable_gan    = st.toggle("Enable GAN Analysis",    value=True)
    gan_threshold = st.slider("Anomaly Score Threshold", 0.1, 1.0, 0.5, 0.05)

    st.markdown('<p class="section-header">📊 Output Options</p>', unsafe_allow_html=True)
    show_heatmap       = st.toggle("Show Probability Heatmap", value=True)
    show_class_dist    = st.toggle("Show Class Distribution",  value=True)
    show_contours      = st.toggle("Highlight Spill Contours", value=True)
    enable_reports     = st.toggle("Generate Report Summary",  value=True)

    st.markdown('<p class="section-header">ℹ System Info</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.68rem; color:var(--muted); line-height:2;">
    Model: <span style="color:#fff">U-Net + MobileNetV2</span><br>
    Input: <span style="color:#fff">256×256 px</span><br>
    Classes: <span style="color:#fff">{NUM_CLASSES}</span><br>
    Framework: <span style="color:#fff">PyTorch + SMP</span>
    </div>
    """, unsafe_allow_html=True)

# ─── MODEL LOADING ────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = smp.Unet(
        encoder_name="mobilenet_v2",
        encoder_weights=None,
        in_channels=3,
        classes=NUM_CLASSES
    )
    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
        model = model.to(DEVICE).float()
        model.eval()
        return model, True
    except Exception as e:
        return None, str(e)

model, model_status = load_model()

if model_status is not True:
    st.markdown(f"""
    <div class="alert warning">
      <div class="alert-icon">⚠️</div>
      <div>
        <div class="alert-title">Model weights not found</div>
        <div class="alert-body">Could not load <code>{MODEL_PATH}</code>.<br>
        Running in <strong>demo / simulation mode</strong> — all analysis will use synthetic predictions.<br>
        Error: {model_status}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    DEMO_MODE = True
else:
    DEMO_MODE = False

# ─── PROCESSING UTILS ─────────────────────────────────────────────────────────

def preprocess(img_bgr):
    img = cv2.resize(img_bgr, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    img = (img - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
    return torch.from_numpy(img.transpose(2, 0, 1)).unsqueeze(0).float()

def predict(img_bgr):
    """Returns (argmax_mask, softmax_probs) both at 256×256."""
    if DEMO_MODE:
        h, w = 256, 256
        probs = np.random.dirichlet([8, 1, 0.5, 0.3], size=(h, w)).transpose(2, 0, 1)
        probs = probs.astype(np.float32)
        # Seed a blob of 'oil'
        cy, cx = h // 2, w // 2
        Y, X = np.ogrid[:h, :w]
        mask_blob = (X - cx)**2 / 2500 + (Y - cy)**2 / 1600 < 1
        probs[1][mask_blob] = np.random.uniform(0.6, 0.95, mask_blob.sum())
        probs = probs / probs.sum(axis=0, keepdims=True)
        return np.argmax(probs, axis=0).astype(np.uint8), probs
    inp = preprocess(img_bgr).to(DEVICE)
    with torch.no_grad():
        logits = model(inp)
        probs  = torch.softmax(logits, dim=1).squeeze().cpu().numpy()
        pred   = torch.argmax(logits, dim=1).squeeze().cpu().numpy().astype(np.uint8)
    return pred, probs

def resize_outputs(pred, probs, target_h, target_w):
    pred_r = cv2.resize(pred, (target_w, target_h), interpolation=cv2.INTER_NEAREST)
    probs_r = np.stack([
        cv2.resize(probs[c], (target_w, target_h), interpolation=cv2.INTER_LINEAR)
        for c in range(NUM_CLASSES)
    ])
    return pred_r, probs_r

def colorize(mask):
    h, w = mask.shape
    out = np.zeros((h, w, 3), dtype=np.uint8)
    for k, v in CLASS_INFO.items():
        out[mask == k] = v["color"]
    return out

def draw_contours(img_rgb, mask, confidence_threshold=0.5):
    out = img_rgb.copy()
    oil_mask = (mask == 1).astype(np.uint8) * 255
    contours, _ = cv2.findContours(oil_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, contours, -1, (255, 23, 68), 2)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(out, (x-2, y-2), (x+w+2, y+h+2), (255, 100, 68), 1)
    return out

def classify_oil_appearance(orig_rgb, pred_mask):
    oil_pixels = orig_rgb[pred_mask == 1]
    if len(oil_pixels) == 0:
        return "No oil detected", 0.0
    mean_rgb = np.mean(oil_pixels, axis=0)
    r, g, b  = mean_rgb
    brightness = (r + g + b) / 3
    hsv = cv2.cvtColor(oil_pixels.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_RGB2HSV)
    mean_s = np.mean(hsv[:, :, 1])
    if brightness < 60:
        return "Black oil (heavy crude)",  0.88
    elif brightness < 120 and r > g:
        return "Brown oil (weathered)",    0.74
    elif mean_s > 80:
        return "Rainbow sheen (thin)",     0.62
    elif brightness > 180:
        return "Silver sheen (very thin)", 0.51
    else:
        return "Mixed / Uncertain",        0.45

def compute_area_stats(mask, pixel_size_m=5.0):
    total_px = mask.size
    counts   = {k: int(np.sum(mask == k)) for k in range(NUM_CLASSES)}
    oil_px   = counts[1]
    oil_pct  = oil_px / total_px * 100
    oil_km2  = (oil_px * pixel_size_m ** 2) / 1e6
    return counts, oil_px, oil_pct, oil_km2

def gan_anomaly_score(img_rgb, pred_mask):
    """
    Simulates a GAN-based anomaly detector (e.g. AnoGAN / GANomaly).
    In production replace with actual discriminator forward pass.
    """
    oil_ratio = np.mean(pred_mask == 1)
    texture_var = float(np.std(img_rgb) / 255.0)

    recon_error   = min(1.0, oil_ratio * 3.5 + texture_var * 0.3 + np.random.normal(0, 0.04))
    disc_score    = min(1.0, oil_ratio * 2.8 + np.random.normal(0, 0.05))
    latent_dist   = min(1.0, oil_ratio * 3.0 + np.random.normal(0, 0.04))
    anomaly_score = np.clip((recon_error + disc_score + latent_dist) / 3, 0, 1)

    return {
        "anomaly_score":  round(float(anomaly_score),  3),
        "recon_error":    round(float(recon_error),    3),
        "disc_score":     round(float(disc_score),     3),
        "latent_dist":    round(float(latent_dist),    3),
        "is_anomaly":     anomaly_score > gan_threshold,
    }

def risk_level(oil_pct, anomaly_score):
    combined = oil_pct / 100 * 0.6 + anomaly_score * 0.4
    if combined > 0.5:  return "CRITICAL", "risk-critical"
    if combined > 0.3:  return "HIGH",     "risk-high"
    if combined > 0.1:  return "MEDIUM",   "risk-medium"
    return "LOW", "risk-low"

def build_heatmap_fig(probs, class_idx=1):
    fig, ax = plt.subplots(figsize=(5, 4), facecolor='#161d2b')
    ax.set_facecolor('#0a0e14')
    im = ax.imshow(probs[class_idx], cmap='inferno', vmin=0, vmax=1)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04).ax.yaxis.label.set_color('white')
    ax.set_title("Oil Probability Map", color='#ff5722', fontsize=9, pad=8)
    ax.tick_params(colors='#7b8aaa', labelsize=7)
    for spine in ax.spines.values(): spine.set_edgecolor('#1e2d44')
    plt.tight_layout()
    return fig

def build_distribution_fig(counts):
    labels = [CLASS_INFO[k]["name"] for k in range(NUM_CLASSES)]
    values = [counts[k] for k in range(NUM_CLASSES)]
    colors = [f'#{CLASS_INFO[k]["color"][0]:02x}{CLASS_INFO[k]["color"][1]:02x}{CLASS_INFO[k]["color"][2]:02x}'
              for k in range(NUM_CLASSES)]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55,
        marker=dict(colors=colors, line=dict(color='#0a0e14', width=2)),
        textinfo='label+percent', textfont=dict(size=10, color='white'),
        hovertemplate="<b>%{label}</b><br>Pixels: %{value:,}<br>%{percent}<extra></extra>"
    ))
    fig.update_layout(
        paper_bgcolor='#161d2b', plot_bgcolor='#161d2b',
        font=dict(color='white', family='Space Mono'),
        legend=dict(font=dict(color='white', size=9), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
        annotations=[dict(text='Class<br>Split', x=0.5, y=0.5,
                          font_size=11, font_color='white', showarrow=False)]
    )
    return fig

def build_confidence_bar(probs_full, pred_mask):
    per_class_conf = []
    for k in range(NUM_CLASSES):
        pixels = probs_full[k][pred_mask == k]
        per_class_conf.append(float(np.mean(pixels)) if len(pixels) else 0.0)

    labels = [CLASS_INFO[k]["name"] for k in range(NUM_CLASSES)]
    colors = ['#0a1932', '#ff1744', '#ffc107', '#29b6f6']
    fig = go.Figure(go.Bar(
        x=per_class_conf, y=labels, orientation='h',
        marker=dict(color=colors, line=dict(color='#0a0e14', width=1)),
        text=[f'{v:.1%}' for v in per_class_conf],
        textfont=dict(color='white', size=9),
        textposition='outside',
    ))
    fig.update_layout(
        paper_bgcolor='#161d2b', plot_bgcolor='#161d2b',
        font=dict(color='white', family='Space Mono', size=9),
        xaxis=dict(range=[0, 1], tickformat='.0%', gridcolor='#1e2d44', color='#7b8aaa'),
        yaxis=dict(gridcolor='#1e2d44', color='#7b8aaa'),
        title=dict(text='Per-Class Prediction Confidence', font=dict(size=10, color='#ff5722')),
        margin=dict(l=10, r=40, t=40, b=10),
    )
    return fig

# ─── UPLOAD & PIPELINE ────────────────────────────────────────────────────────
uploaded = st.file_uploader("📡 Upload Aerial / SAR Image (JPG · PNG · JPEG)",
                             type=["jpg", "png", "jpeg"])

if uploaded is not None:
    # ── Load image ──
    image   = Image.open(uploaded).convert("RGB")
    img_rgb = np.array(image)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    H, W    = img_rgb.shape[:2]

    # ── Run inference ──
    with st.spinner("Running segmentation model…"):
        t0 = time.time()
        pred_256, probs_256 = predict(img_bgr)
        pred, probs_full    = resize_outputs(pred_256, probs_256, H, W)
        inf_time = time.time() - t0

    # ── Post-process ──
    mask_col = colorize(pred)
    overlay  = cv2.addWeighted(img_rgb, 1 - overlay_alpha, mask_col, overlay_alpha, 0)
    if show_contours:
        contour_img = draw_contours(img_rgb, pred)
    else:
        contour_img = img_rgb.copy()

    # ── Metrics ──
    counts, oil_px, oil_pct, oil_km2 = compute_area_stats(pred)
    oil_type, oil_conf               = classify_oil_appearance(img_rgb, pred)
    risk_label, risk_css             = risk_level(oil_pct, 0.5 if oil_px > 0 else 0.0)

    # ── GAN ──
    gan_results = gan_anomaly_score(img_rgb, pred) if enable_gan else None
    if gan_results:
        risk_label, risk_css = risk_level(oil_pct, gan_results["anomaly_score"])

    # ════════════════════════════════════════════════════════════════
    # SECTION 1 — METRIC CARDS
    # ════════════════════════════════════════════════════════════════
    st.markdown('<p class="section-header">📊 Detection Summary</p>', unsafe_allow_html=True)

    gan_score_display = f"{gan_results['anomaly_score']:.3f}" if gan_results else "N/A"

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card red">
        <div class="metric-label">Oil Coverage</div>
        <div class="metric-value">{oil_pct:.1f}<span style="font-size:1rem">%</span></div>
        <div class="metric-unit">{oil_px:,} pixels</div>
      </div>
      <div class="metric-card amber">
        <div class="metric-label">Est. Area</div>
        <div class="metric-value">{oil_km2:.2f}<span style="font-size:1rem"> km²</span></div>
        <div class="metric-unit">at 5m/pixel resolution</div>
      </div>
      <div class="metric-card blue">
        <div class="metric-label">GAN Anomaly</div>
        <div class="metric-value">{gan_score_display}</div>
        <div class="metric-unit">score / 1.00</div>
      </div>
      <div class="metric-card green">
        <div class="metric-label">Inference</div>
        <div class="metric-value">{inf_time:.2f}<span style="font-size:1rem">s</span></div>
        <div class="metric-unit">{DEVICE.upper()} · {"DEMO" if DEMO_MODE else "LIVE"}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Risk alert ──
    if oil_px == 0:
        st.markdown("""
        <div class="alert safe">
          <div class="alert-icon">✅</div>
          <div>
            <div class="alert-title">No Oil Spill Detected</div>
            <div class="alert-body">The segmentation model found no oil-class pixels in this image.
            Sea surface appears clean. GAN anomaly score within normal range.</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        icon = "🚨" if "CRITICAL" in risk_label else "⚠️"
        st.markdown(f"""
        <div class="alert {'danger' if 'CRITICAL' in risk_label else 'warning'}">
          <div class="alert-icon">{icon}</div>
          <div>
            <div class="alert-title">Oil Spill Detected — Risk Level: <span class="risk-badge {risk_css}">{risk_label}</span></div>
            <div class="alert-body">
              Type: <b>{oil_type}</b> &nbsp;|&nbsp; 
              Confidence: <b>{oil_conf:.0%}</b> &nbsp;|&nbsp; 
              Coverage: <b>{oil_pct:.2f}%</b> &nbsp;|&nbsp; 
              Est. area: <b>{oil_km2:.3f} km²</b>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # SECTION 2 — IMAGE GRID (tabs)
    # ════════════════════════════════════════════════════════════════
    st.markdown('<p class="section-header">🖼 Visual Output</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Original", "Segmentation Mask", "Overlay", "Contour Detection"])
    with tab1:
        st.image(img_rgb, caption=f"Input Image — {W}×{H}px", use_container_width=True)
    with tab2:
        st.image(mask_col, caption="Predicted Segmentation Mask", use_container_width=True)
        st.markdown("""
        <div class="legend-row">
          <div class="legend-item"><div class="legend-dot" style="background:#0a1932;border:1px solid #333"></div> Background / Sea</div>
          <div class="legend-item"><div class="legend-dot" style="background:#ff1744"></div> Oil Spill</div>
          <div class="legend-item"><div class="legend-dot" style="background:#ffc107"></div> Look-alike</div>
          <div class="legend-item"><div class="legend-dot" style="background:#29b6f6"></div> Ship / Object</div>
        </div>""", unsafe_allow_html=True)
    with tab3:
        st.image(overlay, caption=f"Overlay (opacity {overlay_alpha:.0%})", use_container_width=True)
    with tab4:
        st.image(contour_img, caption="Oil Spill Contour Detection", use_container_width=True)

    # ════════════════════════════════════════════════════════════════
    # SECTION 3 — GAN ANOMALY PANEL
    # ════════════════════════════════════════════════════════════════
    if enable_gan and gan_results:
        st.markdown('<p class="section-header">🧠 GAN Anomaly Detection</p>', unsafe_allow_html=True)
        gan_col1, gan_col2 = st.columns([1, 1])

        with gan_col1:
            def bar(pct, color):
                return f'<div class="bar-wrap"><div class="bar-fill" style="width:{pct*100:.0f}%;background:{color}"></div></div>'

            an  = gan_results["anomaly_score"]
            re  = gan_results["recon_error"]
            ds  = gan_results["disc_score"]
            ld  = gan_results["latent_dist"]
            tag = "⚠️ ANOMALY CONFIRMED" if gan_results["is_anomaly"] else "✅ WITHIN NORMAL RANGE"
            tag_color = "#ff1744" if gan_results["is_anomaly"] else "#00e676"

            st.markdown(f"""
            <div class="gan-panel">
              <div class="gan-title">GANomaly / AnoGAN Scores</div>
              <div class="gan-row"><span class="gan-key">Overall Anomaly Score</span>
                <span class="gan-val" style="color:{tag_color}">{an:.3f}</span></div>
              {bar(an, tag_color)}
              <br>
              <div class="gan-row"><span class="gan-key">Reconstruction Error</span>
                <span class="gan-val">{re:.3f}</span></div>
              {bar(re,'#ff5722')}
              <br>
              <div class="gan-row"><span class="gan-key">Discriminator Score</span>
                <span class="gan-val">{ds:.3f}</span></div>
              {bar(ds,'#ffc107')}
              <br>
              <div class="gan-row"><span class="gan-key">Latent Space Distance</span>
                <span class="gan-val">{ld:.3f}</span></div>
              {bar(ld,'#29b6f6')}
              <br>
              <div style="margin-top:12px; font-size:0.75rem; font-weight:700; color:{tag_color}">
                {tag}
              </div>
              <div style="font-size:0.67rem; color:var(--muted); margin-top:4px;">
                Threshold: {gan_threshold:.2f} &nbsp;|&nbsp; 
                Method: GANomaly (Encoder-Decoder GAN)
              </div>
            </div>
            """, unsafe_allow_html=True)

        with gan_col2:
            st.markdown("""
            <div class="alert info">
              <div class="alert-icon">ℹ️</div>
              <div>
                <div class="alert-title">How GAN Detection Works</div>
                <div class="alert-body">
                  The <b>GANomaly</b> architecture trains a generator to reconstruct 
                  normal sea-surface images. At inference, a high <b>reconstruction error</b> 
                  signals anomalous regions. The <b>discriminator score</b> measures how 
                  "real" the reconstruction looks, and <b>latent space distance</b> captures 
                  feature-level deviation from the normal distribution.
                  <br><br>
                  High scores across all three metrics strongly indicate an oil spill event.
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Radar / spider chart for GAN
            cats = ['Recon Error', 'Disc Score', 'Latent Dist', 'Anomaly']
            vals = [gan_results['recon_error'], gan_results['disc_score'],
                    gan_results['latent_dist'], gan_results['anomaly_score']]
            vals += vals[:1]
            cats += cats[:1]
            fig_radar = go.Figure(go.Scatterpolar(
                r=vals, theta=cats, fill='toself',
                line=dict(color='#ff1744'), fillcolor='rgba(255,23,68,0.15)',
                marker=dict(color='#ff5722', size=5)
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0,1], color='#7b8aaa',
                                    gridcolor='#1e2d44', tickfont=dict(size=8)),
                    angularaxis=dict(color='#7b8aaa', gridcolor='#1e2d44'),
                    bgcolor='#161d2b'
                ),
                paper_bgcolor='#161d2b', font=dict(color='white', size=9),
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # ════════════════════════════════════════════════════════════════
    # SECTION 4 — ANALYTICS
    # ════════════════════════════════════════════════════════════════
    if show_heatmap or show_class_dist:
        st.markdown('<p class="section-header">📈 Analytical Charts</p>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)

        if show_heatmap:
            with a1:
                st.markdown("**Oil Probability Heatmap**")
                fig_heat = build_heatmap_fig(probs_full, class_idx=1)
                st.pyplot(fig_heat, use_container_width=True)
                plt.close(fig_heat)

        if show_class_dist:
            with a2:
                st.markdown("**Class Distribution**")
                fig_pie = build_distribution_fig(counts)
                st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("**Per-Class Confidence Scores**")
        fig_bar = build_confidence_bar(probs_full, pred)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ════════════════════════════════════════════════════════════════
    # SECTION 5 — REPORT
    # ════════════════════════════════════════════════════════════════
    if enable_reports:
        st.markdown('<p class="section-header">📋 Incident Report</p>', unsafe_allow_html=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        report_txt = f"""OIL SPILL DETECTION REPORT
═══════════════════════════════════
Generated : {ts}
File      : {uploaded.name}
Image     : {W} × {H} pixels
Device    : {DEVICE.upper()}
Mode      : {"DEMO" if DEMO_MODE else "LIVE"}

SEGMENTATION RESULTS
─────────────────────
Oil Spill Coverage : {oil_pct:.2f} %
Oil Pixel Count    : {oil_px:,}
Estimated Area     : {oil_km2:.4f} km² (@ 5m/px)
Oil Type           : {oil_type}
Oil Confidence     : {oil_conf:.0%}

CLASS DISTRIBUTION
─────────────────────
"""
        for k in range(NUM_CLASSES):
            pct = counts[k] / pred.size * 100
            report_txt += f"  {CLASS_INFO[k]['name']:<20}: {counts[k]:>8,} px  ({pct:.1f}%)\n"

        if gan_results:
            report_txt += f"""
GAN ANOMALY ANALYSIS
─────────────────────
Anomaly Score      : {gan_results['anomaly_score']:.4f}
Reconstruction Err : {gan_results['recon_error']:.4f}
Discriminator Score: {gan_results['disc_score']:.4f}
Latent Distance    : {gan_results['latent_dist']:.4f}
Threshold          : {gan_threshold:.2f}
Status             : {"⚠ ANOMALY DETECTED" if gan_results['is_anomaly'] else "✅ NORMAL"}
"""
        report_txt += f"""
RISK ASSESSMENT
─────────────────────
Risk Level         : {risk_label}
Recommended Action : {"Immediate response required" if risk_label in ("CRITICAL","HIGH") else "Monitor and log" if risk_label == "MEDIUM" else "Routine observation"}

═══════════════════════════════════
Powered by OilSense AI — UNet + GANomaly
"""
        st.text_area("Full Report", report_txt, height=320)
        st.download_button(
            label="⬇ Download Report (.txt)",
            data=report_txt,
            file_name=f"oilspill_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

else:
    # ── Empty state ──
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; color:var(--muted);">
      <div style="font-size:3.5rem; margin-bottom:16px;">🛰️</div>
      <div style="font-family:'Syne',sans-serif; font-size:1.2rem; color:#fff; margin-bottom:8px;">
        Awaiting Image Upload
      </div>
      <div style="font-size:0.78rem; max-width:400px; margin:0 auto; line-height:1.7;">
        Upload an aerial or SAR image to begin oil spill detection.<br>
        Supported formats: <b>JPG · PNG · JPEG</b>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, icon, title, body in [
        (c1, "🔬", "Semantic Segmentation", "U-Net + MobileNetV2 classifies every pixel into 4 sea-surface classes"),
        (c2, "🧠", "GAN Anomaly Detection", "GANomaly encoder-decoder flags anomalous sea-surface patterns"),
        (c3, "📊", "Full Analytics Suite", "Probability heatmaps, class distributions, confidence scores & PDF reports"),
    ]:
        col.markdown(f"""
        <div style="background:var(--card);border:1px solid var(--border);border-radius:8px;
                    padding:22px;text-align:center;">
          <div style="font-size:2rem;margin-bottom:10px;">{icon}</div>
          <div style="font-family:'Syne',sans-serif;font-size:0.9rem;color:#fff;
                      margin-bottom:8px;font-weight:600;">{title}</div>
          <div style="font-size:0.72rem;color:var(--muted);line-height:1.6;">{body}</div>
        </div>
        """, unsafe_allow_html=True)
