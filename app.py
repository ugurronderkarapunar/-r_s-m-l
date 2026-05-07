"""
Drone Spotter MVP - Streamlit + OpenCV
Özellikler:
- Arka/ön kamera seçimi
- Çalışan arka plan yakalama butonu
- Hassasiyet ayarı
- Debug modu (hareket maskesi)
- Anlık fotoğraf çekme
- Karanlık mod
- Drone sayısı görüntüleme
"""

import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import base64

# ---------- Sayfa ayarları ----------
st.set_page_config(page_title="Drone Spotter MVP", layout="centered")

# ---------- Karanlık Mod ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

col_title, col_dark = st.columns([3, 1])
with col_title:
    st.title("🚁 Drone Tespit MVP")
with col_dark:
    dark = st.checkbox("🌙 Karanlık Mod", value=st.session_state.dark_mode)
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark

if st.session_state.dark_mode:
    st.markdown("""
    <style>
    body, .stApp {
        background-color: #1e1e1e !important;
        color: #f0f0f0 !important;
    }
    .stButton>button {
        background-color: #333333;
        color: white;
    }
    .stSlider>div>div>div>div {
        background-color: #444444;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
*Telefonunuzu gökyüzüne doğrultun, kamerayı sabit tutup **Arka Planı Yakala**'ya basın.*  
Hareket eden drone benzeri nesneler yeşil çerçeve ile işaretlenir.
""")

# ---------- Kamera Seçimi ----------
camera_option = st.radio(
    "📷 Kamera Seçimi",
    ["Arka Kamera (environment)", "Ön Kamera (user)"],
    horizontal=True,
    index=0
)
facing_mode = "environment" if "Arka" in camera_option else "user"

# ---------- Hassasiyet ----------
threshold = st.slider("🎚️ Hassasiyet (eşik)", 10, 100, 30)

# ---------- Debug Modu ----------
debug_mode = st.checkbox("🐞 Debug: Hareket maskesini göster")

# ---------- Sesli Uyarı (basit bip) ----------
# Her frame güncellemesinde çalacak, drone sayısı > 0 ise HTML5 audio tetiklenir.
# Daha iyisi için aşağıya bir JavaScript fonksiyonu eklenebilir.
if "play_alert" not in st.session_state:
    st.session_state.play_alert = False

# ---------- Oturum durumu ----------
if "bg_captured" not in st.session_state:
    st.session_state.bg_captured = False
if "capture_trigger" not in st.session_state:
    st.session_state.capture_trigger = False

# ---------- Video İşlemci ----------
class DroneDetector(VideoProcessorBase):
    def __init__(self):
        self.bg_model = None
        self.show_debug = False
        self.last_frame = None
        self.drone_count = 0

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.last_frame = img.copy()

        # Arka plan yakalama tetikleyicisi (session state üzerinden)
        if st.session_state.get("capture_trigger", False):
            self.bg_model = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            st.session_state.capture_trigger = False
            st.session_state.bg_captured = True

        # Debug modunu güncelle
        self.show_debug = debug_mode

        # Arka plan yoksa işlem yapma
        if self.bg_model is None:
            cv2.putText(img, "Arka plan yakalayın", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray, self.bg_model)
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # Morfolojik temizlik
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        # Debug modundaysa maskeyi göster
        if self.show_debug:
            debug_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            cv2.putText(debug_img, "DEBUG: Hareket Maskesi", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            return av.VideoFrame.from_ndarray(debug_img, format="bgr24")

        # Kontur bul
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.drone_count = 0
        h, w = img.shape[:2]

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 500 < area < 15000:
                x, y, cw, ch = cv2.boundingRect(cnt)
                aspect_ratio = cw / ch if ch != 0 else 0
                if 0.5 < aspect_ratio < 2.0 and y < h // 2:
                    label = "DRONE"
                    color = (0, 255, 0)
                    self.drone_count += 1
                else:
                    label = "HAREKET"
                    color = (0, 255, 255)
                cv2.rectangle(img, (x, y), (x + cw, y + ch), color, 2)
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Bilgi yazıları
        cv2.putText(img, f"Drone: {self.drone_count}", (20, 40),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, "Aktif" if self.bg_model else "Bekle...", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Sesli uyarı için flag set et (ana thread’de yakalanacak)
        if self.drone_count > 0:
            st.session_state.play_alert = True
        else:
            st.session_state.play_alert = False

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ---------- Butonlar ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("📸 Arka Planı Yakala"):
        st.session_state.capture_trigger = True
        st.toast("Arka plan yakalanıyor... Lütfen kamerayı sabit tutun.", icon="📸")
with col2:
    if st.button("🧹 Sıfırla"):
        st.session_state.bg_captured = False
        st.session_state.capture_trigger = False
        st.toast("Arka plan sıfırlandı. Kamerayı yeniden başlatın.", icon="🔄")

# ---------- WebRTC Streamer ----------
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

ctx = webrtc_streamer(
    key="drone-spotter",
    video_processor_factory=DroneDetector,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={
        "video": {"facingMode": facing_mode},
        "audio": False
    },
    async_processing=True,
)

# ---------- Sesli Uyarı Gerçekleştir ----------
if st.session_state.get("play_alert", False):
    # Basit bip sesi (her frame'de oynar, hafif rahatsız edebilir)
    # Daha kontrollü için JavaScript ile throttle yapılabilir.
    st.markdown("""
    <audio autoplay>
      <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

# ---------- Anlık Görüntü İndirme ----------
if ctx.video_processor and ctx.video_processor.last_frame is not None:
    img = ctx.video_processor.last_frame
    _, buffer = cv2.imencode('.jpg', img)
    st.download_button(
        label="📥 Anlık Görüntü İndir",
        data=buffer.tobytes(),
        file_name="drone_snapshot.jpg",
        mime="image/jpeg"
    )
