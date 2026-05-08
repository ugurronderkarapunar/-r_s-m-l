# requirements.txt
# streamlit
# pandas
# plotly

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# SAYFA YAPILANDIRMASI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Uİ Teori Simülatörü",
    page_icon="🌍",
    layout="wide"
)

# ─────────────────────────────────────────────
# GLOBAL CSS (st.info metinlerini koyulaştırmak için ekleme yapıldı)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Sans+3:wght@300;400;600&display=swap');

    :root {
        --lacivert: #1A3C6E;
        --acik-lacivert: #2C5282;
        --turuncu: #FF6B35;
        --arka-plan: #F0F4F8;
        --kart-bg: #FFFFFF;
        --metin: #1A202C;
        --metin-ikincil: #4A5568;
    }

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
    }

    .stApp {
        background-color: var(--arka-plan);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A3C6E 0%, #0D2147 100%);
        border-right: 3px solid #FF6B35;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #E2E8F0 !important;
        font-size: 15px !important;
        font-weight: 400;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        background: transparent;
    }

    /* Başlıklar */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: var(--lacivert);
    }

    /* Kart bileşeni */
    .kart {
        background: var(--kart-bg);
        border-radius: 12px;
        padding: 28px;
        box-shadow: 0 4px 20px rgba(26, 60, 110, 0.10);
        border-left: 5px solid var(--lacivert);
        margin-bottom: 20px;
    }

    .kart-turuncu {
        background: var(--kart-bg);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(255, 107, 53, 0.12);
        border-left: 5px solid var(--turuncu);
        margin-bottom: 16px;
    }

    .kart-baslik {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 800;
        color: var(--lacivert);
        margin-bottom: 12px;
    }

    .kart-metin {
        font-size: 15px;
        color: var(--metin-ikincil);
        line-height: 1.7;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #1A3C6E 0%, #2C5282 50%, #1A3C6E 100%);
        border-radius: 16px;
        padding: 48px 40px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: "🌍";
        font-size: 160px;
        position: absolute;
        right: 40px;
        top: -20px;
        opacity: 0.12;
    }
    .hero h1 {
        color: #FFFFFF !important;
        font-size: 42px;
        margin-bottom: 12px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .hero p {
        color: #B3C6E0;
        font-size: 18px;
        line-height: 1.6;
        max-width: 600px;
    }

    /* Adım kutuları */
    .adim-kutu {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(26, 60, 110, 0.08);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .adim-kutu:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(26, 60, 110, 0.15);
    }
    .adim-ikon {
        font-size: 40px;
        margin-bottom: 12px;
    }
    .adim-baslik {
        font-family: 'Playfair Display', serif;
        font-size: 17px;
        font-weight: 700;
        color: var(--lacivert);
        margin-bottom: 8px;
    }
    .adim-aciklama {
        font-size: 14px;
        color: var(--metin-ikincil);
        line-height: 1.5;
    }

    /* Teori kartı */
    .teori-kart {
        background: linear-gradient(135deg, #1A3C6E 0%, #2C5282 100%);
        border-radius: 14px;
        padding: 28px;
        color: white;
        box-shadow: 0 6px 24px rgba(26, 60, 110, 0.25);
    }
    .teori-kart h2 {
        color: white !important;
        font-size: 28px;
        margin-bottom: 6px;
    }
    .teori-kart .etiket {
        font-size: 13px;
        font-weight: 600;
        color: #FF6B35;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .teori-kart .deger {
        font-size: 15px;
        color: #B3C6E0;
        line-height: 1.6;
        margin-bottom: 16px;
    }

    /* Senaryo kutusu */
    .senaryo-kutu {
        background: linear-gradient(135deg, #FFF3EE 0%, #FFE8DC 100%);
        border-radius: 12px;
        padding: 24px;
        border-left: 5px solid #FF6B35;
        margin-bottom: 24px;
    }
    .senaryo-baslik {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        color: #C05621;
        margin-bottom: 10px;
    }

    /* Sonuç ekranı */
    .sonuc-hero {
        background: linear-gradient(135deg, #1A3C6E 0%, #2C5282 100%);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        color: white;
        margin-bottom: 24px;
    }
    .sonuc-hero h2 {
        color: white !important;
        font-size: 32px;
    }

    /* Puan göstergesi */
    .puan-kutu {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(26, 60, 110, 0.1);
        border-top: 4px solid #FF6B35;
    }
    .puan-sayi {
        font-family: 'Playfair Display', serif;
        font-size: 56px;
        font-weight: 800;
        color: #FF6B35;
        line-height: 1;
    }

    /* Genel buton */
    .stButton > button {
        background: linear-gradient(135deg, #1A3C6E 0%, #2C5282 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B35 0%, #E5572A 100%);
        transform: translateY(-2px);
    }

    /* Alıntı kutusu */
    .alinti {
        background: #EBF4FF;
        border-left: 4px solid #1A3C6E;
        padding: 16px 20px;
        font-style: italic;
        color: #2C5282;
        margin: 16px 0;
    }

    /* st.info kutusundaki metinlerin okunabilir olması için */
    .stAlert p, .stAlert div {
        color: #1A202C !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TEORİ VERİSİ
# ─────────────────────────────────────────────
THEORIES = {
    "realizm": {
        "id": "realizm",
        "isim": "Realizm",
        "ikon": "🗡️",
        "temel_varsayim": "Devletler, güvenlik ve hayatta kalma güdüsüyle hareket eden üniter rasyonel aktörlerdir. Uluslararası sistem anarşiktir; üst bir otorite yoktur.",
        "ana_aktorler": "Devletler (tek ve egemen aktörler). Uluslararası kurumlar yalnızca güçlü devletlerin araçlarıdır.",
        "dunya_gorusu": "Dünya bir güç mücadelesi arenasıdır. Kalıcı barış bir yanılsamadır; güç dengesi geçici istikrarı sağlar.",
        "guc_tanimi": "Askeri ve ekonomik kapasite. 'Güç' maddi ve ölçülebilir bir kaynaktır; diplomatik manevra bu gücün uzantısıdır.",
        "meshur_soz": "\"Güçlü olan elinden geleni yapar, zayıf olan çekmesi gerekeni çeker.\" — Thukydides",
        "senaryo_davranis": "Gerginliği avantaja çevirmek için baskı uygular, ittifak arar, askeri seçenekleri masada tutar. Müzakere ancak güçten gelirse anlamlıdır.",
        "radar": {"Askeri Odak": 9, "Ekonomik Odak": 5, "İşbirliği İmkanı": 2, "Birey Etkisi": 1},
        "olasilik": {"Çatışma": 78, "İşbirliği": 22}
    },
    "liberalizm": {
        "id": "liberalizm",
        "isim": "Liberalizm",
        "ikon": "🕊️",
        "temel_varsayim": "Devletler işbirliği yapabilir ve karşılıklı çıkar, uluslararası kurumlar ve demokratik normlar aracılığıyla barış inşa edilebilir.",
        "ana_aktorler": "Devletler, uluslararası örgütler, çok uluslu şirketler ve sivil toplum kuruluşları.",
        "dunya_gorusu": "Anarşi yumuşatılabilir. Kurumlar, ticaret bağımlılığı ve demokrasinin yayılması kalıcı barış zeminini hazırlar.",
        "guc_tanimi": "Kurumsal etki, ekonomik entegrasyon ve meşruiyet. 'Soft power' kaynakları en az askeri kapasite kadar belirleyicidir.",
        "meshur_soz": "\"Ebedi Barış, devletlerin anayasal cumhuriyetler olduğu ve hukuka saygı gösterdiği bir düzenle mümkündür.\" — Immanuel Kant",
        "senaryo_davranis": "Uluslararası tahkim mekanizmalarına başvurur, çok taraflı müzakere masası kurar ve ortak çıkarlara dayalı ikili anlaşma arar.",
        "radar": {"Askeri Odak": 3, "Ekonomik Odak": 8, "İşbirliği İmkanı": 9, "Birey Etkisi": 5},
        "olasilik": {"Çatışma": 18, "İşbirliği": 82}
    },
    "konstrüktivizm": {
        "id": "konstrüktivizm",
        "isim": "Konstrüktivizm",
        "ikon": "🧩",
        "temel_varsayim": "Uluslararası ilişkilerin yapısı maddi değil, sosyal olarak inşa edilmiştir. Kimlikler, normlar ve fikirler devlet davranışını belirler.",
        "ana_aktorler": "Devletler, normlar üretici uluslararası topluluklar, sivil aktörler ve önemli bireyler (liderler, entelektüeller).",
        "dunya_gorusu": "Anarşi 'kendi kendine' var olmaz; devletler ona anlam yükler. Kimlikler değişirse davranışlar da değişir.",
        "guc_tanimi": "Söylem, kimlik ve meşruiyet üretme kapasitesi. Kim olduğunuz ne yapabileceğinizi belirler.",
        "meshur_soz": "\"Anarşi, devletlerin onu ne hale getirdiğidir.\" — Alexander Wendt",
        "senaryo_davranis": "Karşılıklı 'düşman kimliği' çerçevesini yeniden tanımlamaya çalışır, ortak tarih ve kader anlatısı inşa eder, sembolik jestler önerir.",
        "radar": {"Askeri Odak": 2, "Ekonomik Odak": 4, "İşbirliği İmkanı": 7, "Birey Etkisi": 9},
        "olasilik": {"Çatışma": 30, "İşbirliği": 70}
    },
    "marksizm": {
        "id": "marksizm",
        "isim": "Marksizm / Bağımlılık Teorisi",
        "ikon": "⚖️",
        "temel_varsayim": "Uluslararası sistem, kapitalist ekonomik yapı tarafından şekillendirilir. Küresel Kuzey ile Güney arasındaki sömürü ilişkileri her çatışmanın asıl nedenidir.",
        "ana_aktorler": "Sınıflar, çok uluslu şirketler, emperyalist devletler ve çevre ülkelerin komprador elitleri.",
        "dunya_gorusu": "Dünya, merkez-çevre hiyerarşisi üzerine kuruludur. Çatışma ekonomik sömürünün bir yansımasıdır; devletler sermayenin araçlarıdır.",
        "guc_tanimi": "Üretim ilişkilerindeki konum. Sermaye birikimi ve ekonomik kontrol gücün gerçek kaynağıdır.",
        "meshur_soz": "\"Az gelişmişlik, az geliştirilmişliktir; doğal bir durum değil, tarihsel bir sürecin ürünüdür.\" — Andre Gunder Frank",
        "senaryo_davranis": "Ekonomik çıkarlar ve sınıf çatışması çerçevesinde analiz eder; baraj şirketlerinin uluslararası sermaye ile bağlantısını sorgular ve direniş önerir.",
        "radar": {"Askeri Odak": 4, "Ekonomik Odak": 10, "İşbirliği İmkanı": 3, "Birey Etkisi": 4},
        "olasilik": {"Çatışma": 65, "İşbirliği": 35}
    }
}

# ─────────────────────────────────────────────
# SİMÜLASYON VERİSİ
# ─────────────────────────────────────────────
SIMULATION_DATA = {
    1: {
        "baslik": "⚡ Aşama 1: İlk Tepki",
        "durum": "Arkania'nın barajı faaliyete geçti. Beledya'da çiftçiler isyan noktasında.",
        "secenekler": {
            "realizm": [
                ("Orduyu nehir sınırına konuşlandır; Arkania'ya güç sinyali ver.", "teorik",
                 "🗡️ Realist hamle: Güç projeksiyonu karşı tarafı masaya oturtuyor."),
                ("BM Su Hukuku Komisyonu'na başvur, uluslararası tahkim iste.", "zit",
                 "🕊️ Teoriye aykırı: Uluslararası kurumlara güven realist anlayışla çelişiyor."),
                ("Diplomatik kanal aç; su paylaşım müzakerelerine çağır.", "pragmatik",
                 "🤝 Pragmatik yaklaşım: Görüşmeler başladı ancak sonuç belirsiz.")
            ],
            "liberalizm": [
                ("BM Su Hukuku Komisyonu'na başvur, uluslararası tahkim iste.", "teorik",
                 "🕊️ Liberal hamle: Uluslararası toplum dikkati çekildi."),
                ("Orduyu nehir sınırına konuşlandır; Arkania'ya güç sinyali ver.", "zit",
                 "🗡️ Teoriye aykırı: Askeri yığınak liberal değerlerle çelişiyor."),
                ("Diplomatik kanal aç; su paylaşım müzakerelerine çağır.", "pragmatik",
                 "🤝 Pragmatik yaklaşım: Görüşmeler başladı, kurumsal destek olmadan yavaş.")
            ],
            "konstrüktivizm": [
                ("İki ülkenin ortak tarihsel su geleneklerini kamuoyuna duyur.", "teorik",
                 "🧩 Konstrüktivist hamle: Medyada 'komşu halklar' anlatısı yankı uyandırdı."),
                ("Orduyu nehir sınırına konuşlandır.", "zit",
                 "🗡️ Teoriye aykırı: Güç gösterisi 'düşman kimliği' söylemini pekiştiriyor."),
                ("Diplomatik kanal aç.", "pragmatik",
                 "🤝 Pragmatik yaklaşım: Diplomatik temas kuruldu ama kimlik dönüşümü sağlanamadı.")
            ],
            "marksizm": [
                ("Barajı inşa eden şirketin ekonomik çıkarlarını kamuoyuyla paylaş.", "teorik",
                 "⚖️ Marksist hamle: Şirket karşıtı ses yükseldi."),
                ("BM Su Hukuku Komisyonu'na başvur.", "zit",
                 "🕊️ Teoriye aykırı: BM kurumları kapitalist düzenin bir parçası."),
                ("Diplomatik kanal aç.", "pragmatik",
                 "🤝 Pragmatik: Görüşme masası kuruldu; ekonomik yapı değişmeden çözüm geçici.")
            ]
        }
    },
    2: {
        "baslik": "🔥 Aşama 2: Kriz Tırmanıyor",
        "durum": "Arkania su akışını kıstı. Beledya'nın tahıl üretimi çöktü. Komşu ülkeler taraf seçiyor.",
        "secenekler": {
            "realizm": [
                ("Bölgesel güç dengesini değiştirmek için askeri ittifak kur.", "teorik",
                 "🗡️ Realist hamle: İttifak kuruldu! Arkania yalnızlaştı."),
                ("Uluslararası yardım çağrısı yap.", "zit",
                 "🆘 Teoriye aykırı: Zafiyetten yapılan çağrı Arkania'yı etkilemedi."),
                ("Ekonomik yaptırım tehdidini masaya koy.", "pragmatik",
                 "💼 Pragmatik: Arkania'yı düşündürdü, etki sınırlı.")
            ],
            "liberalizm": [
                ("Başarılı uluslararası model anlaşmaları öner.", "teorik",
                 "🕊️ Liberal hamle: Nil Havzası örneği müzakereye ivme kazandırdı."),
                ("Askeri ittifak kur.", "zit",
                 "🗡️ Teoriye aykırı: Askeri bloklaşma işbirliği zeminini tahrip etti."),
                ("Ekonomik yaptırım tehdidi.", "pragmatik",
                 "💼 Pragmatik: Arkania bazı teknik uzlaşılara açık sinyal verdi.")
            ],
            "konstrüktivizm": [
                ("Ortak su festivali öner.", "teorik",
                 "🧩 Konstrüktivist hamle: Festival fikri viral oldu, sivil toplum harekete geçti."),
                ("Askeri ittifak kur.", "zit",
                 "🗡️ Teoriye aykırı: Askeri bloklaşma toplumları ayrıştırdı."),
                ("Ekonomik yaptırım tehdidi.", "pragmatik",
                 "💼 Pragmatik: Ekonomik baskı Arkania'yı yavaşlattı.")
            ],
            "marksizm": [
                ("İşçi ve çiftçi örgütlerini sınır ötesi dayanışmaya çağır.", "teorik",
                 "⚖️ Marksist hamle: Sınır ötesi dayanışma güçlendi."),
                ("Askeri ittifak kur.", "zit",
                 "🗡️ Teoriye aykırı: Devlet-devlet ittifakı sermayenin gücünü sorgulamıyor."),
                ("Ekonomik yaptırım tehdidi.", "pragmatik",
                 "💼 Pragmatik: Şirketin çıkarlarını etkiledi, sınıfsal yapı bozulmadı.")
            ]
        }
    },
    3: {
        "baslik": "🌊 Aşama 3: Son Hamle",
        "durum": "Taraflar yoruldu. Uluslararası kamuoyu bir çözüm bekliyor.",
        "secenekler": {
            "realizm": [
                ("Su akışı garantisi karşılığında ikili anlaşma imzala.", "teorik",
                 "🗡️ Realist çözüm: Arkania %25 su akışını serbest bıraktı."),
                ("Konuyu BM Güvenlik Konseyi'ne taşı.", "zit",
                 "🇺🇳 Teoriye aykırı: Büyük güçlerin vetosuyla karşılaştı."),
                ("Su paylaşımını teknik komisyona havale et.", "pragmatik",
                 "📋 Pragmatik: Komisyon çalışmaları başladı, süreç uzuyor.")
            ],
            "liberalizm": [
                ("BM garantörlüğünde kapsamlı antlaşma imzala.", "teorik",
                 "🕊️ Liberal zafer: Tarihi anlaşma sağlandı."),
                ("Müzakere masasında güç temelli pazarlık yap.", "zit",
                 "🗡️ Teoriye aykırı: Kurumsal güvenceden yoksun anlaşma."),
                ("Teknik komisyona havale et.", "pragmatik",
                 "📋 Pragmatik: Teknik çözüm sağlandı, meşruiyet eksik.")
            ],
            "konstrüktivizm": [
                ("'Bereket Nehri Barış Beyannamesi'ni imzalat.", "teorik",
                 "🧩 Konstrüktivist zirve: Yeni komşu kimliği pekişti."),
                ("Güç temelli pazarlık yap.", "zit",
                 "🗡️ Teoriye aykırı: Kimlik dönüşümü geri alındı."),
                ("Teknik komisyona havale et.", "pragmatik",
                 "📋 Pragmatik: Teknik çözüm, kimliksel ayrışma sürüyor.")
            ],
            "marksizm": [
                ("Barajı millileştir veya ortak kamu idaresine devret.", "teorik",
                 "⚖️ Marksist devrim: Şirket bölgeden çekildi, çiftçiler yönetimde."),
                ("BM garantörlüğünde antlaşma imzala.", "zit",
                 "🕊️ Teoriye aykırı: Antlaşma şirketin çıkarlarını korudu."),
                ("Teknik komisyona havale et.", "pragmatik",
                 "📋 Pragmatik: Sınıfsal ilişkiler değişmedi.")
            ]
        }
    }
}

SONUCLAR = {
    3: {"baslik": "🏆 Mükemmel Teorik Tutarlılık!", "metin": "Teorik çerçeveyi tavizsiz uyguladın.", "durum": "✅ Kalıcı anlaşma sağlandı."},
    2: {"baslik": "⚖️ Dengeli Pragmatist", "metin": "Teori ile pratiği dengeledin.", "durum": "⚠️ Statüko korundu, gerginlik sürüyor."},
    1: {"baslik": "🌪️ Kriz Yönetimi Zayıf", "metin": "Teoriden sapmalar belirsizliğe yol açtı.", "durum": "🔴 Gerginlik sürdü, çözüm ertelendi."},
    0: {"baslik": "💥 Tam Kaos", "metin": "Hiçbir teoriye uymayan kararlar.", "durum": "☠️ Kriz çözümsüz kaldı."}
}

# ─────────────────────────────────────────────
# SESSION STATE BAŞLATMA
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "🏠 Ana Sayfa",
        "secilen_teori": None,
        "sim_asama": 0,
        "sim_puan": 0,
        "sim_rol": None,
        "sim_secimler": [],
        "sim_bitti": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:36px">🌍</div>
        <div class="sidebar-logo-metin">Uİ Teori Simülatörü</div>
    </div>
    """, unsafe_allow_html=True)

    menu_secenekleri = ["🏠 Ana Sayfa", "📚 Teori Seçimi", "🎮 Simülasyon (Nehir Krizi)", "📊 Karşılaştırma Tablosu", "ℹ️ Hakkında"]
    secili_sayfa = st.radio("Menü", menu_secenekleri, index=menu_secenekleri.index(st.session_state["page"]), label_visibility="collapsed")
    st.session_state["page"] = secili_sayfa

    if st.session_state["secilen_teori"]:
        t = THEORIES[st.session_state["secilen_teori"]]
        st.markdown(f"""
        <div style="margin-top:24px; background:rgba(255,107,53,0.15); border-radius:8px; padding:12px; border:1px solid rgba(255,107,53,0.3);">
            <div style="font-size:11px; color:#FF6B35; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Seçili Teori</div>
            <div style="color:#E2E8F0; font-weight:600;">{t['ikon']} {t['isim']}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ANA SAYFA
# ─────────────────────────────────────────────
def show_home():
    st.markdown("""
    <div class="hero">
        <h1>Uluslararası İlişkiler Teori Simülatörü</h1>
        <p>Soyut teorileri gerçek bir kriz senaryosunda test et.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="adim-kutu"><div class="adim-ikon">📚</div><div class="adim-baslik">1. Teorini Seç</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="adim-kutu"><div class="adim-ikon">🎮</div><div class="adim-baslik">2. Simülasyonu Çalıştır</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="adim-kutu"><div class="adim-ikon">📊</div><div class="adim-baslik">3. Sonuçları Karşılaştır</div></div>', unsafe_allow_html=True)

    if st.button("🚀 Hemen Başla"):
        st.session_state["page"] = "📚 Teori Seçimi"
        st.rerun()

# ─────────────────────────────────────────────
# TEORİ SEÇİMİ
# ─────────────────────────────────────────────
def show_theory_selection():
    st.markdown('<h1>📚 Teori Seçimi</h1>', unsafe_allow_html=True)
    col_sol, col_sag = st.columns([1, 1.4])
    with col_sol:
        id_listesi = list(THEORIES.keys())
        gosterim = [f"{THEORIES[tid]['ikon']}  {THEORIES[tid]['isim']}" for tid in id_listesi]
        secim = st.selectbox("🔍 Teori seçin:", range(len(id_listesi)), format_func=lambda i: gosterim[i])
        secilen_id = id_listesi[secim]
        teori = THEORIES[secilen_id]
        if st.button("🎮 Simülasyona Başla"):
            st.session_state["secilen_teori"] = secilen_id
            for k in ["sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
                if k in st.session_state: del st.session_state[k]
            init_state()
            st.session_state["page"] = "🎮 Simülasyon (Nehir Krizi)"
            st.rerun()
    with col_sag:
        st.markdown(f"""
        <div class="teori-kart">
            <h2>{teori['ikon']} {teori['isim']}</h2>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div class="etiket">Temel Varsayım</div><div class="deger">{teori['temel_varsayim']}</div>
            <div class="etiket">Ana Aktörler</div><div class="deger">{teori['ana_aktorler']}</div>
            <div class="etiket">Güç Tanımı</div><div class="deger">{teori['guc_tanimi']}</div>
            <div class="etiket">Dünya Görüşü</div><div class="deger">{teori['dunya_gorusu']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="alinti">{teori["meshur_soz"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SİMÜLASYON
# ─────────────────────────────────────────────
def show_simulation():
    if not st.session_state.get("secilen_teori"):
        st.warning("⚠️ Lütfen önce bir teori seçin.")
        if st.button("Teori Seçimine Git"):
            st.session_state["page"] = "📚 Teori Seçimi"
            st.rerun()
        return

    teori = THEORIES[st.session_state["secilen_teori"]]
    st.markdown(f'<h1>🎮 Simülasyon — {teori["ikon"]} {teori["isim"]}</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="senaryo-kutu">
        <div class="senaryo-baslik">🌊 Nehir Krizi Senaryosu</div>
        <p style="color:#5D4037;">Bereket Nehri krizi: Arkania baraj yaptı, Beledya susuz kaldı.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["sim_asama"] == 0:
        rol = st.radio("Rol seç:", ["🏔️ Arkania", "🌾 Beledya"])
        if st.button("Oyuna Başla"):
            st.session_state["sim_rol"] = rol
            st.session_state["sim_asama"] = 1
            st.rerun()
        return

    if st.session_state["sim_bitti"]:
        show_simulation_result()
        return

    asama = st.session_state["sim_asama"]
    asama_veri = SIMULATION_DATA[asama]
    st.markdown(f"### {asama_veri['baslik']}")
    st.markdown(f'<div class="kart-turuncu"><p>{asama_veri["durum"]}</p></div>', unsafe_allow_html=True)

    secenekler = asama_veri["secenekler"][st.session_state["secilen_teori"]]
    secim_metin = [s[0] for s in secenekler]
    secim = st.radio("Eyleminiz:", secim_metin, key=f"sec_{asama}")

    if st.button("Kararı Uygula"):
        secilen = secenekler[secim_metin.index(secim)]
        if secilen[1] == "teorik":
            st.session_state["sim_puan"] += 1
        st.session_state["sim_secimler"].append({"asama": asama, "secim": secim, "tip": secilen[1], "geri_bildirim": secilen[2]})
        st.session_state["sim_asama"] += 1
        if st.session_state["sim_asama"] > 3:
            st.session_state["sim_bitti"] = True
        st.rerun()

    if st.session_state["sim_secimler"]:
        for s in st.session_state["sim_secimler"]:
            st.info(s["geri_bildirim"])

def show_simulation_result():
    puan = st.session_state["sim_puan"]
    teori = THEORIES[st.session_state["secilen_teori"]]
    sonuc = SONUCLAR[puan]

    st.markdown(f"""
    <div class="sonuc-hero">
        <div style="font-size:60px;">{teori['ikon']}</div>
        <h2>{sonuc['baslik']}</h2>
        <p>{sonuc['durum']}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f'<div class="puan-kutu"><div class="puan-sayi">{puan}/3</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kart"><p>{sonuc["metin"]}</p><p><strong>Teorik Beklenti:</strong> {teori["senaryo_davranis"]}</p></div>', unsafe_allow_html=True)

    # 3D Grafik
    teorik = sum(1 for s in st.session_state["sim_secimler"] if s["tip"] == "teorik")
    pragmatik = sum(1 for s in st.session_state["sim_secimler"] if s["tip"] == "pragmatik")
    aykiri = 3 - teorik - pragmatik

    fig_3d = go.Figure(go.Scatter3d(
        x=[teorik], y=[pragmatik], z=[aykiri],
        mode='markers+text',
        marker=dict(size=12, color='#FF6B35'),
        text=["Senin Kararların"],
        textposition='top center'
    ))
    fig_3d.update_layout(
        scene=dict(xaxis_title="Teorik", yaxis_title="Pragmatik", zaxis_title="Aykırı",
                   xaxis=dict(range=[0,3]), yaxis=dict(range=[0,3]), zaxis=dict(range=[0,3])),
        height=400, title="Kararlarının 3 Boyutlu Profili"
    )
    st.plotly_chart(fig_3d, use_container_width=True)

    if st.button("🔄 Sıfırla"):
        for k in ["sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
            if k in st.session_state: del st.session_state[k]
        init_state()
        st.rerun()

# ─────────────────────────────────────────────
# KARŞILAŞTIRMA
# ─────────────────────────────────────────────
def show_comparison():
    st.markdown('<h1>📊 Karşılaştırma Tablosu</h1>', unsafe_allow_html=True)
    df = pd.DataFrame({
        "Teori": ["Realizm 🗡️", "Liberalizm 🕊️", "Konstrüktivizm 🧩", "Marksizm ⚖️"],
        "Aktör": ["Devlet", "Devlet + Kurumlar", "Toplumlar", "Sınıflar"],
        "Barış Yolu": ["Güç dengesi", "Kurumlar", "Kimlik dönüşümü", "Sınıf mücadelesi"]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_radar = go.Figure()
        for tid in THEORIES:
            t = THEORIES[tid]
            fig_radar.add_trace(go.Scatterpolar(
                r=[t["radar"]["Askeri Odak"], t["radar"]["Ekonomik Odak"], t["radar"]["İşbirliği İmkanı"], t["radar"]["Birey Etkisi"]],
                theta=["Askeri", "Ekonomi", "İşbirliği", "Birey"],
                fill='toself', name=f'{t["ikon"]} {t["isim"]}'
            ))
        fig_radar.update_layout(height=400)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        fig_bar = go.Figure(data=[
            go.Bar(name='Çatışma', x=list(THEORIES.keys()), y=[t["olasilik"]["Çatışma"] for t in THEORIES.values()]),
            go.Bar(name='İşbirliği', x=list(THEORIES.keys()), y=[t["olasilik"]["İşbirliği"] for t in THEORIES.values()])
        ])
        st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# HAKKINDA
# ─────────────────────────────────────────────
def show_about():
    st.markdown('<h1>ℹ️ Hakkında</h1>', unsafe_allow_html=True)
    st.markdown('<div class="kart"><p>Eğitim amaçlı Uluslararası İlişkiler simülatörü.</p></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; color:#A0AEC0;">© 2024 Uİ Teori Simülatörü</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# YÖNLENDİRME
# ─────────────────────────────────────────────
page = st.session_state["page"]
if page == "🏠 Ana Sayfa":
    show_home()
elif page == "📚 Teori Seçimi":
    show_theory_selection()
elif page == "🎮 Simülasyon (Nehir Krizi)":
    show_simulation()
elif page == "📊 Karşılaştırma Tablosu":
    show_comparison()
elif page == "ℹ️ Hakkında":
    show_about()
