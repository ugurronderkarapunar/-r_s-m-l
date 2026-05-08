# requirements.txt
# streamlit
# pandas
# plotly

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Sayfa yapılandırması ──────────────────────────
st.set_page_config(
    page_title="Uİ Teori Simülatörü",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS (sadece gerekli düzeltmeler) ──────
st.markdown("""
<style>
    .stApp {
        background-color: #F0F4F8;
    }
    h1, h2, h3 {
        color: #1A3C6E;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1A3C6E, #2C5282);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B35, #E5572A);
        transform: translateY(-2px);
    }
    .stAlert p {
        color: #1A202C !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Teori Verisi ──────────────────────────────────
THEORIES = {
    "realizm": {
        "isim": "Realizm",
        "ikon": "🗡️",
        "varsayim": "Devletler güvenlik odaklıdır; uluslararası sistem anarşiktir.",
        "aktor": "Devletler (egemen ve üniter)",
        "guc": "Askeri ve ekonomik kapasite",
        "dunya": "Güç mücadelesi; sıfır toplamlı",
        "soz": "“Güçlü olan elinden geleni yapar, zayıf olan çekmesi gerekeni çeker.” – Thukydides",
        "davranis": "Askeri tehdit ve güç dengesi ile sonuç alır.",
        "radar": [9, 5, 2, 1],
        "olasilik": [78, 22]
    },
    "liberalizm": {
        "isim": "Liberalizm",
        "ikon": "🕊️",
        "varsayim": "İşbirliği mümkündür; kurumlar ve ticaret barışı getirir.",
        "aktor": "Devletler + Uluslararası örgütler + STK'lar",
        "guc": "Yumuşak güç, diplomasi, ekonomik refah",
        "dunya": "Artı toplamlı oyun; demokratik barış",
        "soz": "“Ebedi Barış, hukukla mümkündür.” – Immanuel Kant",
        "davranis": "Uluslararası tahkim ve ortak projelerle kazan‑kazan arar.",
        "radar": [3, 8, 9, 5],
        "olasilik": [18, 82]
    },
    "konstrüktivizm": {
        "isim": "Konstrüktivizm",
        "ikon": "🧩",
        "varsayim": "Uluslararası ilişkiler sosyal olarak inşa edilir; kimlikler ve normlar belirleyicidir.",
        "aktor": "Devletler, norm üreticileri, bireyler",
        "guc": "Söylem ve kimlik üretme kapasitesi",
        "dunya": "Dost‑düşman kimliği değişkendir",
        "soz": "“Anarşi, devletlerin onu ne hale getirdiğidir.” – Alexander Wendt",
        "davranis": "Ortak kimlik inşası ve sembolik işbirliği önerir.",
        "radar": [2, 4, 7, 9],
        "olasilik": [30, 70]
    },
    "marksizm": {
        "isim": "Marksizm / Bağımlılık",
        "ikon": "⚖️",
        "varsayim": "Kapitalist sistem sömürü ilişkileri yaratır; çatışma sınıfsaldır.",
        "aktor": "Sınıflar, çok uluslu şirketler",
        "guc": "Üretim araçlarına sahiplik",
        "dunya": "Merkez‑çevre hiyerarşisi",
        "soz": "“Az gelişmişlik, az geliştirilmişliktir.” – Andre Gunder Frank",
        "davranis": "Şirketleri ifşa eder, ekonomik yapıyı dönüştürmeyi hedefler.",
        "radar": [4, 10, 3, 4],
        "olasilik": [65, 35]
    }
}

# ── Simülasyon Verisi ─────────────────────────────
SIMULATION_DATA = {
    1: {
        "baslik": "Aşama 1: İlk Tepki",
        "durum": "Arkania barajı yaptı. Beledya'da tarım çöküyor. İlk adımı seçin.",
        "secenekler": {
            "realizm": [
                ("Orduyu sınıra kaydır", "teorik", "🗡️ Realist hamle: Güç gösterisi yaptınız."),
                ("BM'ye başvur", "zit", "🕊️ Teoriye aykırı: Kurumlara güvendiniz."),
                ("Diplomasi başlat", "pragmatik", "🤝 Pragmatik: Müzakere başladı.")
            ],
            "liberalizm": [
                ("BM'ye başvur", "teorik", "🕊️ Liberal hamle: Arabulucular devreye girdi."),
                ("Orduyu kaydır", "zit", "🗡️ Teoriye aykırı: Askeri yığınak liberal değerlerle çelişti."),
                ("Diplomasi başlat", "pragmatik", "🤝 Pragmatik: Görüşmeler yavaş ilerliyor.")
            ],
            "konstrüktivizm": [
                ("Ortak su geleneklerini duyur", "teorik", "🧩 Konstrüktivist: 'Komşu halklar' anlatısı yayıldı."),
                ("Orduyu kaydır", "zit", "🗡️ Teoriye aykırı: Düşman kimliği pekişti."),
                ("Diplomasi başlat", "pragmatik", "🤝 Pragmatik: Temas kuruldu ama kimlik değişmedi.")
            ],
            "marksizm": [
                ("Şirketin çıkarlarını ifşa et", "teorik", "⚖️ Marksist: Kamuoyunda şirket karşıtı ses yükseldi."),
                ("BM'ye başvur", "zit", "🕊️ Teoriye aykırı: BM kapitalist düzenin parçası."),
                ("Diplomasi başlat", "pragmatik", "🤝 Pragmatik: Ekonomik yapı değişmedi.")
            ]
        }
    },
    2: {
        "baslik": "Aşama 2: Kriz Tırmanıyor",
        "durum": "Arkania suyu kıstı. Beledya'da kıtlık başladı. Komşular taraf seçiyor.",
        "secenekler": {
            "realizm": [
                ("Askeri ittifak kur", "teorik", "🗡️ Realist: İttifak Arkania'yı yalnızlaştırdı."),
                ("İnsani yardım çağrısı yap", "zit", "🆘 Teoriye aykırı: Zayıflık algısı oluştu."),
                ("Yaptırım tehdidi", "pragmatik", "💼 Pragmatik: Arkania'yı düşündürdü.")
            ],
            "liberalizm": [
                ("Model anlaşma öner", "teorik", "🕊️ Liberal: Nil Havzası örneği müzakereye ivme kazandırdı."),
                ("Askeri ittifak kur", "zit", "🗡️ Teoriye aykırı: Bloklaşma işbirliğini tahrip etti."),
                ("Yaptırım tehdidi", "pragmatik", "💼 Pragmatik: Arkania teknik uzlaşılara açık.")
            ],
            "konstrüktivizm": [
                ("Ortak festival öner", "teorik", "🧩 Konstrüktivist: Festival fikri viraldi."),
                ("Askeri ittifak kur", "zit", "🗡️ Teoriye aykırı: Toplumlar ayrıştı."),
                ("Yaptırım tehdidi", "pragmatik", "💼 Pragmatik: Baskı yavaşlattı.")
            ],
            "marksizm": [
                ("Sınır ötesi işçi dayanışması çağrısı", "teorik", "⚖️ Marksist: Dayanışma güçlendi."),
                ("Askeri ittifak kur", "zit", "🗡️ Teoriye aykırı: Sermaye sorgulanmadı."),
                ("Yaptırım tehdidi", "pragmatik", "💼 Pragmatik: Şirket etkilendi.")
            ]
        }
    },
    3: {
        "baslik": "Aşama 3: Son Hamle",
        "durum": "Taraflar yoruldu. Çözüm için son karar.",
        "secenekler": {
            "realizm": [
                ("İkili anlaşma (güç dengesi)", "teorik", "🗡️ Realist çözüm: Arkania suyu serbest bıraktı."),
                ("BM Güvenlik Konseyi'ne taşı", "zit", "🇺🇳 Teoriye aykırı: Veto yedi."),
                ("Teknik komisyona havale et", "pragmatik", "📋 Pragmatik: Süreç uzuyor.")
            ],
            "liberalizm": [
                ("BM garantörlüğünde anlaşma imzala", "teorik", "🕊️ Liberal zafer: Tarihi anlaşma."),
                ("Güç temelli pazarlık", "zit", "🗡️ Teoriye aykırı: Kurumsal güvence yok."),
                ("Teknik komisyona havale et", "pragmatik", "📋 Pragmatik: Meşruiyet eksik.")
            ],
            "konstrüktivizm": [
                ("Barış Beyannamesi imzalat", "teorik", "🧩 Konstrüktivist: Yeni komşu kimliği inşa edildi."),
                ("Güç temelli pazarlık", "zit", "🗡️ Teoriye aykırı: Kimlik dönüşümü tersine döndü."),
                ("Teknik komisyona havale et", "pragmatik", "📋 Pragmatik: Ayrışma sürüyor.")
            ],
            "marksizm": [
                ("Barajı ortak kamuya devret", "teorik", "⚖️ Marksist devrim: Şirket çekildi, çiftçiler yönetimde."),
                ("BM anlaşması", "zit", "🕊️ Teoriye aykırı: Şirket çıkarları korundu."),
                ("Teknik komisyona havale et", "pragmatik", "📋 Pragmatik: Sınıfsal yapı değişmedi.")
            ]
        }
    }
}

SONUCLAR = {
    3: "🏆 Mükemmel Teorik Tutarlılık! Kalıcı anlaşma sağlandı.",
    2: "⚖️ Dengeli Pragmatist. Statüko korundu, gerginlik sürüyor.",
    1: "🌪️ Kriz Yönetimi Zayıf. Çözüm ertelendi.",
    0: "💥 Tam Kaos. Kriz çözümsüz kaldı."
}

# ── Session State ─────────────────────────────────
def init_state():
    D = {
        "page": "🏠 Ana Sayfa",
        "secilen_teori": None,
        "sim_asama": 0,
        "sim_puan": 0,
        "sim_rol": None,
        "sim_secimler": [],
        "sim_bitti": False,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Sidebar ───────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Uİ Teori Simülatörü")
    menu = ["🏠 Ana Sayfa", "📚 Teori Seçimi", "🎮 Simülasyon", "📊 Karşılaştırma", "ℹ️ Hakkında"]
    secim = st.radio("Menü", menu, index=menu.index(st.session_state["page"]))
    if secim != st.session_state["page"]:
        st.session_state["page"] = secim
        st.rerun()
    if st.session_state["secilen_teori"]:
        t = THEORIES[st.session_state["secilen_teori"]]
        st.info(f"Seçili: {t['ikon']} {t['isim']}")

# ── Ana Sayfa ─────────────────────────────────────
def show_home():
    st.title("🌍 Uluslararası İlişkiler Teori Simülatörü")
    st.markdown("Gerçek bir kriz senaryosunda **Realizm, Liberalizm, Konstrüktivizm ve Marksizm** teorilerini test edin.")
    col1, col2, col3 = st.columns(3)
    col1.metric("📚", "Teorini Seç", "1. Adım")
    col2.metric("🎮", "Simülasyon", "2. Adım")
    col3.metric("📊", "Karşılaştır", "3. Adım")
    if st.button("🚀 Hemen Başla"):
        st.session_state["page"] = "📚 Teori Seçimi"
        st.rerun()

# ── Teori Seçimi ──────────────────────────────────
def show_theory_selection():
    st.title("📚 Teori Seçimi")
    col1, col2 = st.columns([1, 2])
    with col1:
        tid_list = list(THEORIES.keys())
        sec = st.selectbox("Teori seçin", range(len(tid_list)),
                           format_func=lambda i: f"{THEORIES[tid_list[i]]['ikon']} {THEORIES[tid_list[i]]['isim']}")
        teori = THEORIES[tid_list[sec]]
        if st.button("🎮 Bu Teoriyle Simülasyona Başla"):
            st.session_state["secilen_teori"] = tid_list[sec]
            for k in ["sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
                if k in st.session_state: del st.session_state[k]
            init_state()
            st.session_state["page"] = "🎮 Simülasyon"
            st.rerun()
    with col2:
        st.subheader(f"{teori['ikon']} {teori['isim']}")
        st.markdown(f"**Temel Varsayım:** {teori['varsayim']}")
        st.markdown(f"**Ana Aktörler:** {teori['aktor']}")
        st.markdown(f"**Güç Tanımı:** {teori['guc']}")
        st.markdown(f"**Dünya Görüşü:** {teori['dunya']}")
        st.info(teori['soz'])
        st.caption(f"Kriz Davranışı: {teori['davranis']}")

# ── Simülasyon ────────────────────────────────────
def show_simulation():
    if not st.session_state.get("secilen_teori"):
        st.warning("Önce bir teori seçin.")
        if st.button("Teori Seçimine Git"):
            st.session_state["page"] = "📚 Teori Seçimi"
            st.rerun()
        return
    teori = THEORIES[st.session_state["secilen_teori"]]
    st.title(f"🎮 Simülasyon — {teori['ikon']} {teori['isim']}")

    if st.session_state["sim_asama"] == 0:
        rol = st.radio("Rolünüz:", ["🏔️ Arkania", "🌾 Beledya"])
        if st.button("Oyuna Başla"):
            st.session_state["sim_rol"] = rol
            st.session_state["sim_asama"] = 1
            st.rerun()
        return

    if st.session_state["sim_bitti"]:
        show_result()
        return

    asama = st.session_state["sim_asama"]
    a = SIMULATION_DATA[asama]
    st.subheader(a["baslik"])
    st.write(a["durum"])
    secenekler = a["secenekler"][st.session_state["secilen_teori"]]
    sec_text = [s[0] for s in secenekler]
    secim = st.radio("Eylem:", sec_text, key=f"s{asama}")
    if st.button("Kararı Uygula"):
        sec = secenekler[sec_text.index(secim)]
        if sec[1] == "teorik":
            st.session_state["sim_puan"] += 1
        st.session_state["sim_secimler"].append({"asama": asama, "secim": secim, "tip": sec[1], "feedback": sec[2]})
        st.session_state["sim_asama"] += 1
        if st.session_state["sim_asama"] > 3:
            st.session_state["sim_bitti"] = True
        st.rerun()

    if st.session_state["sim_secimler"]:
        for s in st.session_state["sim_secimler"]:
            st.info(s["feedback"])

def show_result():
    puan = st.session_state["sim_puan"]
    teori = THEORIES[st.session_state["secilen_teori"]]
    sonuc = SONUCLAR[puan]
    st.success(f"## {sonuc}")
    col1, col2 = st.columns(2)
    col1.metric("Teori Uyum Puanı", f"{puan}/3")
    col2.write(f"**Teorik Beklenti:** {teori['davranis']}")

    # 3D grafik
    teorik = sum(1 for s in st.session_state["sim_secimler"] if s["tip"] == "teorik")
    pragmatik = sum(1 for s in st.session_state["sim_secimler"] if s["tip"] == "pragmatik")
    aykiri = 3 - teorik - pragmatik
    fig3 = go.Figure(go.Scatter3d(
        x=[teorik], y=[pragmatik], z=[aykiri],
        mode='markers+text',
        marker=dict(size=15, color='#FF6B35'),
        text=["Senin Kararların"],
        textposition='top center'
    ))
    fig3.update_layout(scene=dict(xaxis_title="Teorik", yaxis_title="Pragmatik", zaxis_title="Aykırı",
                                  xaxis=dict(range=[0,3]), yaxis=dict(range=[0,3]), zaxis=dict(range=[0,3])),
                       height=400, title="Kararlarının 3 Boyutlu Profili")
    st.plotly_chart(fig3, use_container_width=True)

    if st.button("🔄 Sıfırla"):
        for k in ["sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
            if k in st.session_state: del st.session_state[k]
        init_state()
        st.rerun()

# ── Karşılaştırma Tablosu ─────────────────────────
def show_comparison():
    st.title("📊 Teoriler Karşılaştırma")
    # Tablo
    df = pd.DataFrame({
        "Teori": [f"{t['ikon']} {t['isim']}" for t in THEORIES.values()],
        "Aktör": [t['aktor'] for t in THEORIES.values()],
        "Güç": [t['guc'] for t in THEORIES.values()],
        "Dünya Görüşü": [t['dunya'] for t in THEORIES.values()]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Radar
    kategoriler = ["Askeri", "Ekonomi", "İşbirliği", "Birey"]
    fig_radar = go.Figure()
    for tid, t in THEORIES.items():
        fig_radar.add_trace(go.Scatterpolar(
            r=t["radar"] + [t["radar"][0]],
            theta=kategoriler + [kategoriler[0]],
            fill='toself',
            name=f"{t['ikon']} {t['isim']}"
        ))
    fig_radar.update_layout(height=400)
    st.plotly_chart(fig_radar, use_container_width=True)

    # Bar
    fig_bar = go.Figure(data=[
        go.Bar(name="Çatışma", x=list(THEORIES.keys()), y=[t["olasilik"][0] for t in THEORIES.values()]),
        go.Bar(name="İşbirliği", x=list(THEORIES.keys()), y=[t["olasilik"][1] for t in THEORIES.values()])
    ])
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Hakkında ──────────────────────────────────────
def show_about():
    st.title("ℹ️ Hakkında")
    st.markdown("Eğitim amaçlı Uluslararası İlişkiler simülatörüdür.")
    st.markdown("© 2024 Uİ Teori Simülatörü")

# ── Sayfa Yönlendirme ─────────────────────────────
page = st.session_state["page"]
if page == "🏠 Ana Sayfa":
    show_home()
elif page == "📚 Teori Seçimi":
    show_theory_selection()
elif page == "🎮 Simülasyon":
    show_simulation()
elif page == "📊 Karşılaştırma":
    show_comparison()
elif page == "ℹ️ Hakkında":
    show_about()
