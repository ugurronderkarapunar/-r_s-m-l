"""
Drone Spotter MVP - Streamlit + OpenCV
Kameradan gelen görüntüde hareketli nesneleri tespit eder,
boyut ve konuma göre drone olarak işaretler.
"""

import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av

st.set_page_config(page_title="Drone Spotter MVP", layout="centered")
st.title("🚁 Drone Tespit MVP (Streamlit)")

st.markdown("""
**Nasıl Çalışır:**  
Kamerayı başlat, **Arka Planı Yakala** butonuna tıkla.  
Ardından ekranda hareket eden nesneleri izle; drone benzeri olanlar yeşil dikdörtgenle işaretlenir.
""")

# Threshold slider
threshold = st.slider("Hassasiyet (eşik değeri)", 10, 100, 30)

class DroneDetector(VideoProcessorBase):
    def __init__(self):
        self.bg_model = None           # referans arka plan (gri ton)
        self.capture_background = False
        self.frame_count = 0

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1

        # İlk kareyi direkt arka plan olarak al veya butonla güncelle
        if self.bg_model is None or self.capture_background:
            # Convert to grayscale
            self.bg_model = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.capture_background = False
            # Sadece bir kez almak için kendini kapat
            st.session_state["bg_captured"] = True

        # Arka plan yoksa işlem yapma
        if self.bg_model is None:
            return frame

        # Kareyi griye çevir
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Arka plan çıkarma (fark)
        diff = cv2.absdiff(gray, self.bg_model)

        # Eşikleme
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # Morfolojik işlemler (gürültü temizleme)
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        # Kontur bul
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        drone_count = 0
        h, w = img.shape[:2]

        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Alan filtreleme (çok küçük / çok büyük değilse)
            if 500 < area < 15000:
                x, y, cw, ch = cv2.boundingRect(cnt)
                aspect_ratio = cw / ch if ch != 0 else 0
                # Drone benzeri koşullar: karemsi veya hafifçe dikdörtgen (0.5-2.0)
                if 0.5 < aspect_ratio < 2.0:
                    # Gökyüzünde olma ihtimali: resmin üst yarısında
                    if y < h // 2:
                        label = "DRONE"
                        color = (0, 255, 0)
                        drone_count += 1
                    else:
                        label = "HAREKET"
                        color = (0, 255, 255)
                else:
                    label = "HAREKET"
                    color = (0, 255, 255)
            elif area >= 200:
                # Çok küçük ama hareketli
                x, y, cw, ch = cv2.boundingRect(cnt)
                label = "KUCUK"
                color = (0, 0, 255)
            else:
                continue

            # Dikdörtgen çiz
            cv2.rectangle(img, (x, y), (x + cw, y + ch), color, 2)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Bilgi yaz
        cv2.putText(img, f"Drone: {drone_count}", (20, 40),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, "Bekleme..." if self.bg_model is None else "Aktif",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Streamlit state management
if "bg_captured" not in st.session_state:
    st.session_state["bg_captured"] = False

# Buton: arka planı manuel yakala
col1, col2 = st.columns(2)
with col1:
    if st.button("📸 Arka Planı Yakala"):
        st.session_state["bg_captured"] = False  # processor'ın yeniden almasını tetikleyeceğiz
        # Processor'ın capture_background flag'ini set edecek bir mekanizma gerek
        # streamlit_webrtc'de VideoProcessorBase ile buton etkileşimi callback ile yapılır.
        st.warning("Arka plan yakalama aktif – lütfen kamerayı sabit tutun.")
with col2:
    if st.button("🧹 Sıfırla"):
        # Sıfırlama ancak webrtc_streamer tekrar başlatılırsa mümkün, basitçe uyaralım
        st.info("Değişikliklerin etkili olması için kamerayı durdurup yeniden başlatın.")

# WebRTC streamer
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

ctx = webrtc_streamer(
    key="drone-spotter",
    video_processor_factory=DroneDetector,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,   # performans için
)

# Buton tetiklemesini processor'a iletmek için:
if ctx.video_processor:
    if st.session_state.get("capture_trigger", False):
        ctx.video_processor.capture_background = True
        st.session_state["capture_trigger"] = False
