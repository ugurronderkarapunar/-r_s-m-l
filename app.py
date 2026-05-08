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

# ── Session State ────────────────────────────────
def init_state():
    defaults = {
        "page": "🏠 Ana Sayfa",
        "secilen_teori": None,
        "scenario": None,
        "sim_asama": 0,
        "sim_puan": 0,
        "sim_rol": None,
        "sim_secimler": [],
        "sim_bitti": False,
        "tema": "🌞 Açık",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Tema CSS (açık / koyu + mobil iyileştirmeler) ──
if st.session_state["tema"] == "🌙 Koyu":
    tema_css = """
    <style>
        :root {
            --bg: #0F172A;
            --card-bg: #1E293B;
            --text: #E2E8F0;
            --text-secondary: #CBD5E1;
            --primary: #FF6B35;
            --primary-dark: #1A3C6E;
            --border: rgba(255,255,255,0.1);
        }
        .stApp { background-color: var(--bg); }
        h1, h2, h3, h4, h5, h6, p, li, span, div, label { color: var(--text) !important; }
        .stMetric label, .stMetric div { color: var(--text) !important; }
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-dark), var(--primary));
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            padding: 0.6em 1.5em;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--primary), #E5572A);
            transform: translateY(-2px);
        }
        .stAlert p { color: #1A202C !important; }
        .stDataFrame { background-color: var(--card-bg); }
        @media (max-width: 768px) {
            .stButton > button { padding: 0.8em 1.2em; font-size: 16px; }
        }
    </style>
    """
else:
    tema_css = """
    <style>
        :root {
            --bg: #F0F4F8;
            --card-bg: #FFFFFF;
            --text: #1A202C;
            --text-secondary: #4A5568;
            --primary: #FF6B35;
            --primary-dark: #1A3C6E;
            --border: rgba(0,0,0,0.05);
        }
        .stApp { background-color: var(--bg); }
        h1, h2, h3 { color: var(--primary-dark); }
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-dark), #2C5282);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            padding: 0.6em 1.5em;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--primary), #E5572A);
            transform: translateY(-2px);
        }
        .stAlert p { color: #1A202C !important; }
        @media (max-width: 768px) {
            .stButton > button { padding: 0.8em 1.2em; font-size: 16px; }
        }
    </style>
    """
st.markdown(tema_css, unsafe_allow_html=True)

# ── Teori Verisi (4 eski + 4 yeni) ─────────────────
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
    },
    "feminizm": {
        "isim": "Feminizm",
        "ikon": "♀️",
        "varsayim": "Uluslararası ilişkiler cinsiyetçi yapılar üzerine kuruludur; eril bakış hâkimdir.",
        "aktor": "Devletler, toplumsal cinsiyet rolleri, ezilen gruplar",
        "guc": "Kapsayıcılık, eşitlik, görünürlük",
        "dunya": "Hiyerarşiler sadece maddi değil, cinsiyet temellidir.",
        "soz": "“Kişisel olan politiktir.” – Carol Hanisch",
        "davranis": "Kararların kadınlar ve azınlıklar üzerindeki etkisini öne çıkarır, kapsayıcı çözümler arar.",
        "radar": [1, 6, 8, 7],
        "olasilik": [25, 75]
    },
    "post_kolonyal": {
        "isim": "Post‑kolonyalizm",
        "ikon": "🌍",
        "varsayim": "Batı merkezli bilgi ve sömürgecilik mirası uluslararası sistemi şekillendirir.",
        "aktor": "Eski sömürgeler, küresel Güney, yerli halklar",
        "guc": "Tarihsel anlatıları kontrol etme, kültürel direniş",
        "dunya": "Merkez‑çevre, Batı‑dışı perspektifler",
        "soz": "“Avrupa'nın sessize aldığı halklar konuşacak.” – Dipesh Chakrabarty",
        "davranis": "Emperyal geçmişi ifşa eder, eşitler arası diyalog ve tazminat talepleriyle hareket eder.",
        "radar": [2, 5, 9, 6],
        "olasilik": [40, 60]
    },
    "yesil_teori": {
        "isim": "Yeşil Teori",
        "ikon": "🌿",
        "varsayim": "Ekolojik sınırlar ve gezegenin sağlığı siyasetin merkezindedir.",
        "aktor": "Ekosistemler, gelecek nesiller, çevreci hareketler",
        "guc": "Sürdürülebilirlik, ekolojik ayak izi kontrolü",
        "dunya": "İnsan‑doğa uyumu; büyüme değil denge",
        "soz": "“Doğa pazarlık masasında değil, masanın kendisidir.”",
        "davranis": "Kaynakları koruma, yenilenebilir enerjiye geçiş, ekolojik adalet ön plandadır.",
        "radar": [0, 7, 10, 5],
        "olasilik": [10, 90]
    },
    "ingiliz_okulu": {
        "isim": "İngiliz Okulu",
        "ikon": "🏛️",
        "varsayim": "Devletler bir 'uluslararası toplum' oluşturur; ortak normlar ve kurallar sistemi vardır.",
        "aktor": "Devletler topluluğu, uluslararası kurumlar",
        "guc": "Meşruiyet, ortak değerler, diplomasi",
        "dunya": "Anarşi ve düzen arasında; uluslararası toplumun evrimi",
        "soz": "“Uluslararası toplum, anarşinin içindeki düzendir.” – Hedley Bull",
        "davranis": "Mevcut normları korur, çok taraflı müzakere ve uzlaşı ile krizi yönetir.",
        "radar": [5, 5, 6, 4],
        "olasilik": [45, 55]
    }
}

# ── Simülasyon Verisi ─────────────────────────────
# Senaryo 1: Nehir Krizi (mevcut, kısaltılmış)
SIMULATION_DATA_NEHIR = {
    1: {
        "baslik": "Aşama 1: İlk Tepki",
        "durum": "Arkania barajı yaptı. Beledya'da tarım çöküyor.",
        "secenekler": {
            "realizm": [("Orduyu sınıra kaydır", "teorik", "🗡️ Güç gösterisi."), ("BM'ye başvur", "zit", "🕊️ Kurumlara güven."), ("Diplomasi başlat", "pragmatik", "🤝 Müzakere.")],
            "liberalizm": [("BM'ye başvur", "teorik", "🕊️ Arabulucular devreye girdi."), ("Orduyu kaydır", "zit", "🗡️ Askeri yığınak."), ("Diplomasi başlat", "pragmatik", "🤝 Yavaş ilerleme.")],
            "konstrüktivizm": [("Ortak su geleneklerini duyur", "teorik", "🧩 'Komşu halklar' anlatısı."), ("Orduyu kaydır", "zit", "🗡️ Düşman kimliği."), ("Diplomasi başlat", "pragmatik", "🤝 Kimlik değişmedi.")],
            "marksizm": [("Şirketin çıkarlarını ifşa et", "teorik", "⚖️ Şirket karşıtı tepki."), ("BM'ye başvur", "zit", "🕊️ Kapitalist düzen."), ("Diplomasi başlat", "pragmatik", "🤝 Ekonomik yapı değişmedi.")],
            "feminizm": [("Kadın çiftçilerin mağduriyetini öne çıkar", "teorik", "♀️ Görünürlük sağlandı."), ("BM'ye başvur", "zit", "🕊️ Cinsiyet körü."), ("Diplomasi başlat", "pragmatik", "🤝 Yüzeysel.")],
            "post_kolonyal": [("Suyun sömürge dönemi paylaşımını hatırlat", "teorik", "🌍 Tarihsel adalet gündemi."), ("BM'ye başvur", "zit", "🕊️ Batılı mekanizma."), ("Diplomasi başlat", "pragmatik", "🤝 Eşitliksiz.")],
            "yesil_teori": [("Nehir ekosisteminin çöküşüne dikkat çek", "teorik", "🌿 Ekolojik hassasiyet."), ("Orduyu kaydır", "zit", "🗡️ Doğaya aykırı."), ("Diplomasi başlat", "pragmatik", "🤝 Yetersiz.")],
            "ingiliz_okulu": [("Uluslararası Nehir Hukuku'nu uygula", "teorik", "🏛️ Normlara dayalı."), ("Orduyu kaydır", "zit", "🗡️ Toplum dışı."), ("Diplomasi başlat", "pragmatik", "🤝 Norm eksik.")]
        }
    },
    2: {
        "baslik": "Aşama 2: Kriz Tırmanıyor",
        "durum": "Arkania suyu kıstı. Kıtlık başladı.",
        "secenekler": {
            "realizm": [("Askeri ittifak kur", "teorik", "🗡️ Arkania yalnızlaştı."), ("İnsani yardım çağrısı", "zit", "🆘 Zayıflık algısı."), ("Yaptırım tehdidi", "pragmatik", "💼 Arkania'yı düşündürdü.")],
            "liberalizm": [("Model anlaşma öner", "teorik", "🕊️ Nil Havzası örneği."), ("Askeri ittifak kur", "zit", "🗡️ Bloklaşma."), ("Yaptırım tehdidi", "pragmatik", "💼 Arkania uzlaşılara açık.")],
            "konstrüktivizm": [("Ortak festival öner", "teorik", "🧩 Festival viraldi."), ("Askeri ittifak kur", "zit", "🗡️ Toplumlar ayrıştı."), ("Yaptırım tehdidi", "pragmatik", "💼 Baskı yavaşlattı.")],
            "marksizm": [("Sınır ötesi işçi dayanışması", "teorik", "⚖️ Dayanışma güçlendi."), ("Askeri ittifak kur", "zit", "🗡️ Sermaye sorgulanmadı."), ("Yaptırım tehdidi", "pragmatik", "💼 Şirket etkilendi.")],
            "feminizm": [("Kadın kooperatiflerini destekle", "teorik", "♀️ Ekonomik güçlenme."), ("Askeri ittifak kur", "zit", "🗡️ Militarizm."), ("Yaptırım tehdidi", "pragmatik", "💼 Cinsiyet etkisi yok.")],
            "post_kolonyal": [("Güney ülkeleriyle dayanışma kampanyası", "teorik", "🌍 Küresel Güney dayanışması."), ("Askeri ittifak kur", "zit", "🗡️ Batı bloklaşması."), ("Yaptırım tehdidi", "pragmatik", "💼 Neokolonyal.")],
            "yesil_teori": [("Su kıtlığına karşı ortak ekoloji planı", "teorik", "🌿 Sürdürülebilirlik."), ("Askeri ittifak kur", "zit", "🗡️ Ekolojik yıkım."), ("Yaptırım tehdidi", "pragmatik", "💼 Karbon ayak izi.")],
            "ingiliz_okulu": [("Uluslararası Konferans düzenle", "teorik", "🏛️ Toplumsal norm."), ("Askeri ittifak kur", "zit", "🗡️ Norm ihlali."), ("Yaptırım tehdidi", "pragmatik", "💼 Yumuşak baskı.")]
        }
    },
    3: {
        "baslik": "Aşama 3: Son Hamle",
        "durum": "Taraflar yoruldu. Çözüm için son karar.",
        "secenekler": {
            "realizm": [("İkili anlaşma (güç dengesi)", "teorik", "🗡️ Arkania suyu serbest bıraktı."), ("BM Güvenlik Konseyi'ne taşı", "zit", "🇺🇳 Veto yedi."), ("Teknik komisyon", "pragmatik", "📋 Süreç uzuyor.")],
            "liberalizm": [("BM garantörlüğünde anlaşma imzala", "teorik", "🕊️ Tarihi anlaşma."), ("Güç temelli pazarlık", "zit", "🗡️ Kurumsal güvence yok."), ("Teknik komisyon", "pragmatik", "📋 Meşruiyet eksik.")],
            "konstrüktivizm": [("Barış Beyannamesi imzalat", "teorik", "🧩 Yeni komşu kimliği."), ("Güç temelli pazarlık", "zit", "🗡️ Kimlik dönüşümü tersine döndü."), ("Teknik komisyon", "pragmatik", "📋 Ayrışma sürüyor.")],
            "marksizm": [("Barajı ortak kamuya devret", "teorik", "⚖️ Devrimsel adım."), ("BM anlaşması", "zit", "🕊️ Şirket çıkarları korundu."), ("Teknik komisyon", "pragmatik", "📋 Sınıfsal yapı değişmedi.")],
            "feminizm": [("Cinsiyet eşitliğini antlaşmaya ekle", "teorik", "♀️ Dönüştürücü."), ("BM anlaşması", "zit", "🕊️ Eril dil."), ("Teknik komisyon", "pragmatik", "📋 Eksik.")],
            "post_kolonyal": [("Tarihsel adalet için özür ve tazminat talep et", "teorik", "🌍 Onarıcı adalet."), ("BM anlaşması", "zit", "🕊️ Batı formülü."), ("Teknik komisyon", "pragmatik", "📋 Geçmişi es geçer.")],
            "yesil_teori": [("Nehir ekosistemini koruma altına al", "teorik", "🌿 Doğa kazandı."), ("BM anlaşması", "zit", "🕊️ Yeşil boyama."), ("Teknik komisyon", "pragmatik", "📋 Sürdürülemez.")],
            "ingiliz_okulu": [("Ortak normatif çerçeve anlaşması", "teorik", "🏛️ Toplum inşası."), ("Güç temelli pazarlık", "zit", "🗡️ Norm erozyonu."), ("Teknik komisyon", "pragmatik", "📋 Norm eksik.")]
        }
    }
}

# Senaryo 2: Ticaret Savaşları (yeni)
SIMULATION_DATA_TICARET = {
    1: {
        "baslik": "Aşama 1: Gerilim Tırmanıyor",
        "durum": "Ülkeniz, komşu ülkenin dampingli ihracatı nedeniyle yerli sanayisini korumak için gümrük vergisi artırmayı düşünüyor.",
        "secenekler": {
            "realizm": [("Yüksek gümrük vergisi koy", "teorik", "🗡️ Korumacı güç gösterisi."), ("Serbest ticaret anlaşması öner", "zit", "🕊️ Realist çıkar çatışması."), ("Misilleme tehdidi", "pragmatik", "💼 Karşı tarafı düşündürür.")],
            "liberalizm": [("Serbest ticaret anlaşması öner", "teorik", "🕊️ Karşılıklı kazanç."), ("Yüksek gümrük vergisi koy", "zit", "🗡️ İşbirliğini baltalar."), ("Misilleme tehdidi", "pragmatik", "💼 Geçici baskı.")],
            "konstrüktivizm": [("Ticaretin kültürel boyutunu vurgula", "teorik", "🧩 Ortak kimlik."), ("Yüksek gümrük vergisi koy", "zit", "🗡️ Düşman imajı."), ("Misilleme tehdidi", "pragmatik", "💼 Söylem eksik.")],
            "marksizm": [("Damping yapan çok uluslu şirketleri ifşa et", "teorik", "⚖️ Emekçi dayanışması."), ("Serbest ticaret anlaşması", "zit", "🕊️ Kapitalist çözüm."), ("Misilleme tehdidi", "pragmatik", "💼 Sınıfsal değil.")],
            "feminizm": [("Kadın girişimcilerin zararını öne çıkar", "teorik", "♀️ Toplumsal cinsiyet farkındalığı."), ("Yüksek gümrük vergisi koy", "zit", "🗡️ Cinsiyet körü."), ("Misilleme tehdidi", "pragmatik", "💼 Eşitliksiz.")],
            "post_kolonyal": [("Kuzey-Güney eşitsizliğini gündeme getir", "teorik", "🌍 Adaletsiz ticaret."), ("Serbest ticaret anlaşması", "zit", "🕊️ Bağımlılık."), ("Misilleme tehdidi", "pragmatik", "💼 Geçici.")],
            "yesil_teori": [("Karbon ayak izi düzenlemesiyle yeşil ticaret öner", "teorik", "🌿 Sürdürülebilir ticaret."), ("Yüksek gümrük vergisi koy", "zit", "🗡️ Doğaya zarar."), ("Misilleme tehdidi", "pragmatik", "💼 Yeşil değil.")],
            "ingiliz_okulu": [("DTÖ kurallarına başvur", "teorik", "🏛️ Normatif çerçeve."), ("Yüksek gümrük vergisi koy", "zit", "🗡️ Kuralları ihlal."), ("Misilleme tehdidi", "pragmatik", "💼 Norm dışı.")]
        }
    },
    2: {
        "baslik": "Aşama 2: Karşı Hamle",
        "durum": "Komşu ülke misilleme yaptı. Sektörler zarar görüyor.",
        "secenekler": {
            "realizm": [("Ekonomik yaptırımları artır", "teorik", "🗡️ Güç savaşı."), ("Uluslararası tahkime başvur", "zit", "🕊️ Realist çelişki."), ("Müzakere masası kur", "pragmatik", "💼 Denge arayışı.")],
            "liberalizm": [("Uluslararası tahkime başvur", "teorik", "🕊️ Kurumsal çözüm."), ("Yaptırımları artır", "zit", "🗡️ İşbirliğini öldürür."), ("Müzakere masası kur", "pragmatik", "💼 Yavaş ilerleme.")],
            "konstrüktivizm": [("Ortak ticaret kültürü oluşturma çağrısı", "teorik", "🧩 Norm inşası."), ("Yaptırımları artır", "zit", "🗡️ Düşmanlık."), ("Müzakere masası kur", "pragmatik", "💼 Söylem eksik.")],
            "marksizm": [("İşçi sendikalarını sınır ötesi işbirliğine çağır", "teorik", "⚖️ Sınıf dayanışması."), ("Yaptırımları artır", "zit", "🗡️ Sermaye kazanır."), ("Müzakere masası kur", "pragmatik", "💼 Sınıfsal değil.")],
            "feminizm": [("Kadın istihdamını koruma paketi açıkla", "teorik", "♀️ Eşitlikçi politika."), ("Yaptırımları artır", "zit", "🗡️ Kadınları etkiler."), ("Müzakere masası kur", "pragmatik", "💼 Eksik.")],
            "post_kolonyal": [("Küresel Güney ticaret bloğu oluştur", "teorik", "🌍 Dayanışma."), ("Yaptırımları artır", "zit", "🗡️ Merkez-çevre."), ("Müzakere masası kur", "pragmatik", "💼 Eşitsiz.")],
            "yesil_teori": [("Yeşil dönüşüm fonu öner", "teorik", "🌿 Ortak gelecek."), ("Yaptırımları artır", "zit", "🗡️ Ekolojik kriz."), ("Müzakere masası kur", "pragmatik", "💼 Dönüşümsüz.")],
            "ingiliz_okulu": [("Uluslararası Ticaret Örgütü'ne başvur", "teorik", "🏛️ Normatif çözüm."), ("Yaptırımları artır", "zit", "🗡️ Toplum dışı."), ("Müzakere masası kur", "pragmatik", "💼 Normlar zayıf.")]
        }
    },
    3: {
        "baslik": "Aşama 3: Nihai Karar",
        "durum": "Ekonomik daralma derinleşiyor. Halk sokağa döküldü.",
        "secenekler": {
            "realizm": [("Askeri güçle ticareti zorla", "teorik", "🗡️ Hegemonik çözüm."), ("DTÖ kararına uy", "zit", "🏛️ Egemenlik kaybı."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Geçici.")],
            "liberalizm": [("Kapsamlı serbest ticaret anlaşması imzala", "teorik", "🕊️ Kalıcı barış."), ("Askeri güç kullan", "zit", "🗡️ Liberalizme aykırı."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 İkinci en iyi.")],
            "konstrüktivizm": [("Ortak refah kimliği inşa eden anlaşma", "teorik", "🧩 Yeni norm."), ("Askeri güç kullan", "zit", "🗡️ Kimlik tahribi."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Yüzeysel.")],
            "marksizm": [("Üretim araçlarını kamulaştır ve adil ticaret kooperatifi kur", "teorik", "⚖️ Yapısal dönüşüm."), ("DTÖ kararına uy", "zit", "🕊️ Kapitalist sistem."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Geçici.")],
            "feminizm": [("Cinsiyet bütçelemesi ve kapsayıcı ticaret", "teorik", "♀️ Dönüştürücü."), ("Askeri güç kullan", "zit", "🗡️ Militarist."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Eksik.")],
            "post_kolonyal": [("Tarihsel sömürüyü tanıyan tazminat ve yeni düzen", "teorik", "🌍 Onarıcı."), ("DTÖ kararına uy", "zit", "🕊️ Batı merkezli."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Eşitsiz.")],
            "yesil_teori": [("Yeşil ekonomiye geçiş anlaşması", "teorik", "🌿 Sürdürülebilir."), ("Askeri güç kullan", "zit", "🗡️ Ekolojik yıkım."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Yetersiz.")],
            "ingiliz_okulu": [("Ortak ticaret normları ve etik kurallar sözleşmesi", "teorik", "🏛️ Toplum inşası."), ("Askeri güç kullan", "zit", "🗡️ Norm dışı."), ("Yumuşatılmış anlaşma", "pragmatik", "💼 Norm zayıf.")]
        }
    }
}

SONUCLAR = {
    3: "🏆 Mükemmel Teorik Tutarlılık! Kalıcı anlaşma sağlandı.",
    2: "⚖️ Dengeli Pragmatist. Statüko korundu, gerginlik sürüyor.",
    1: "🌪️ Kriz Yönetimi Zayıf. Çözüm ertelendi.",
    0: "💥 Tam Kaos. Kriz çözümsüz kaldı."
}

# ── Terim Sözlüğü (expander) ──────────────────────
GLOSSARY = {
    "Anarşi": "Uluslararası sistemde üstün bir otoritenin bulunmaması.",
    "Güvenlik İkilemi": "Bir devletin güvenlik adına attığı adımların diğerlerini tehdit edip silahlanmaya yol açması.",
    "Yumuşak Güç": "Askeri güç yerine kültür, değerler ve diplomasi ile etki kurma.",
    "Sıfır Toplamlı Oyun": "Birinin kazancının diğerinin kaybı olduğu durum.",
    "Artı Toplamlı Oyun": "İşbirliği ile herkesin kazanabileceği durum.",
    "Demokratik Barış": "Demokratik devletlerin birbirleriyle savaşma ihtimalinin düşük olduğu teorisi.",
    "Kimlik İnşası": "Konstrüktivizmde devlet kimliklerinin etkileşimlerle oluşması.",
    "Merkez-Çevre": "Marksist bağımlılık teorisinde gelişmiş ülkelerin (merkez) az gelişmişleri (çevre) sömürmesi.",
    "Norm Girişimcisi": "Yeni uluslararası normların oluşmasını sağlayan aktörler.",
    "Toplumsal Cinsiyet": "Feminist teoride rollerin ve beklentilerin inşa edildiği alan.",
}

# ── Sidebar (tema, menü, seçili teori) ──────────
with st.sidebar:
    st.markdown("## 🌍 Uİ Teori Simülatörü")
    tema_secenek = st.radio("Tema", ["🌞 Açık", "🌙 Koyu"], index=0 if st.session_state["tema"] == "🌞 Açık" else 1)
    if tema_secenek != st.session_state["tema"]:
        st.session_state["tema"] = tema_secenek
        st.rerun()

    menu = ["🏠 Ana Sayfa", "📚 Teori Seçimi", "🎮 Simülasyon", "📊 Karşılaştırma", "ℹ️ Hakkında"]
    secim = st.radio("Menü", menu, index=menu.index(st.session_state["page"]))
    if secim != st.session_state["page"]:
        st.session_state["page"] = secim
        st.rerun()

    if st.session_state["secilen_teori"]:
        t = THEORIES[st.session_state["secilen_teori"]]
        st.info(f"Seçili: {t['ikon']} {t['isim']}")

# ── Ana Sayfa + Terim Sözlüğü ────────────────────
def show_home():
    st.title("🌍 Uluslararası İlişkiler Teori Simülatörü")
    st.markdown("Gerçek bir kriz senaryosunda **çok sayıda teoriyi** test edin. Yeni teoriler eklendi: Feminizm, Post‑kolonyalizm, Yeşil Teori, İngiliz Okulu.")
    col1, col2, col3 = st.columns(3)
    col1.metric("📚", "Teorini Seç", "1. Adım")
    col2.metric("🎮", "Simülasyon", "2. Adım")
    col3.metric("📊", "Karşılaştır", "3. Adım")
    if st.button("🚀 Hemen Başla"):
        st.session_state["page"] = "📚 Teori Seçimi"
        st.rerun()

    with st.expander("📖 Terimler Sözlüğü"):
        for terim, aciklama in GLOSSARY.items():
            st.markdown(f"**{terim}**: {aciklama}")

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
            for k in ["scenario", "sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
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

# ── Simülasyon (senaryo seçimi eklendi) ──────────
def show_simulation():
    if not st.session_state.get("secilen_teori"):
        st.warning("Önce bir teori seçin.")
        if st.button("Teori Seçimine Git"):
            st.session_state["page"] = "📚 Teori Seçimi"
            st.rerun()
        return

    teori = THEORIES[st.session_state["secilen_teori"]]
    st.title(f"🎮 Simülasyon — {teori['ikon']} {teori['isim']}")

    # Senaryo seçimi
    if st.session_state.get("scenario") is None:
        senaryo = st.radio("Senaryo seçin", ["🌊 Nehir Krizi", "💼 Ticaret Savaşları"])
        if st.button("Senaryoyu Onayla"):
            st.session_state["scenario"] = senaryo
            st.rerun()
        return

    # Senaryo verisini seç
    if st.session_state["scenario"] == "🌊 Nehir Krizi":
        data = SIMULATION_DATA_NEHIR
    else:
        data = SIMULATION_DATA_TICARET

    # Rol seçimi
    if st.session_state["sim_asama"] == 0:
        if st.session_state["scenario"] == "🌊 Nehir Krizi":
            rol_secenek = ["🏔️ Arkania", "🌾 Beledya"]
        else:
            rol_secenek = ["🏭 Sanayi Ülkesi", "🌾 Tarım Ülkesi"]
        rol = st.radio("Rolünüz:", rol_secenek)
        if st.button("Oyuna Başla"):
            st.session_state["sim_rol"] = rol
            st.session_state["sim_asama"] = 1
            st.rerun()
        return

    if st.session_state["sim_bitti"]:
        show_result()
        return

    asama = st.session_state["sim_asama"]
    a = data[asama]
    st.subheader(a["baslik"])
    st.write(a["durum"])

    # Seçenekleri al, eğer teori ID yoksa "realizm" varsay
    tid = st.session_state["secilen_teori"]
    if tid not in a["secenekler"]:
        tid = "realizm"  # fallback
    secenekler = a["secenekler"][tid]
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
        for k in ["scenario", "sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
            if k in st.session_state: del st.session_state[k]
        init_state()
        st.rerun()

# ── Karşılaştırma Sayfası (3D scatter eklendi) ──
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

    # Radar grafik
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

    # Bar grafik
    fig_bar = go.Figure(data=[
        go.Bar(name="Çatışma", x=list(THEORIES.keys()), y=[t["olasilik"][0] for t in THEORIES.values()]),
        go.Bar(name="İşbirliği", x=list(THEORIES.keys()), y=[t["olasilik"][1] for t in THEORIES.values()])
    ])
    st.plotly_chart(fig_bar, use_container_width=True)

    # 3D scatter (Yeni)
    st.subheader("🌐 Teorilerin 3 Boyutlu Konumlandırması")
    fig_3d_all = go.Figure()
    for tid, t in THEORIES.items():
        fig_3d_all.add_trace(go.Scatter3d(
            x=[t["radar"][0]],  # Askeri
            y=[t["radar"][1]],  # Ekonomi
            z=[t["radar"][2]],  # İşbirliği
            mode='markers+text',
            marker=dict(size=t["radar"][3]*5, color=t["radar"][3], colorscale='Viridis', showscale=True),
            text=f"{t['ikon']} {t['isim']}",
            textposition='top center',
            name=t["isim"]
        ))
    fig_3d_all.update_layout(
        scene=dict(xaxis_title="Askeri Odak", yaxis_title="Ekonomik Odak", zaxis_title="İşbirliği İmkanı"),
        height=500
    )
    st.plotly_chart(fig_3d_all, use_container_width=True)

# ── Hakkında ──────────────────────────────────────
def show_about():
    st.title("ℹ️ Hakkında")
    st.markdown("Eğitim amaçlı Uluslararası İlişkiler simülatörüdür. Yeni teoriler ve senaryolar eklendi.")
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
