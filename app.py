# requirements.txt
# streamlit
# pandas
# plotly

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

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
        "dil": "tr",
        "gecmis": [],
        "skorlar": [],
        "oyuncu_adi": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Otomatik tema + manuel ───────────────────────
if st.session_state["tema"] == "🌙 Koyu":
    tema_css = """
    <style>
        .stApp { background-color: #0F172A; }
        h1, h2, h3, h4, h5, h6, p, li, span, div, label { color: #E2E8F0 !important; }
        .stMetric label, .stMetric div { color: #E2E8F0 !important; }
        .stButton>button { background: linear-gradient(135deg, #1A3C6E, #FF6B35); color: white; border: none; border-radius: 12px; font-weight: 600; padding: 0.6em 1.5em; }
        .stButton>button:hover { background: linear-gradient(135deg, #FF6B35, #E5572A); transform: translateY(-2px); }
        .stAlert p { color: #1A202C !important; }
        .stDataFrame { background-color: #1E293B; color: #E2E8F0; }
    </style>
    """
else:
    tema_css = """
    <style>
        .stApp { background-color: #F0F4F8; }
        h1, h2, h3 { color: #1A3C6E; }
        .stButton>button { background: linear-gradient(135deg, #1A3C6E, #2C5282); color: white; border: none; border-radius: 12px; font-weight: 600; padding: 0.6em 1.5em; }
        .stButton>button:hover { background: linear-gradient(135deg, #FF6B35, #E5572A); transform: translateY(-2px); }
        .stAlert p { color: #1A202C !important; }
    </style>
    """
st.markdown(tema_css, unsafe_allow_html=True)

# ── Çoklu dil metinleri ──────────────────────────
DIL = {
    "tr": {
        "menü": ["🏠 Ana Sayfa", "📚 Teori Seçimi", "🎮 Simülasyon", "📊 Karşılaştırma", "📜 Geçmiş & Profil", "🏆 Skor Tablosu", "ℹ️ Hakkında"],
        "tema": "Tema",
        "dil": "Dil",
        "hosgeldin": "Uluslararası İlişkiler Teori Simülatörü",
        "basla": "Hemen Başla",
        "teori_sec": "Teori Seçimi",
        "simulasyon": "Simülasyon",
        "karsilastirma": "Karşılaştırma",
        "hakkinda": "Hakkında",
        "terimler": "Terimler Sözlüğü",
        "profil": "Kişiselleştirilmiş Teori Profilin",
        "rapor_indir": "Raporu İndir",
        "sesli_oku": "Sesli Oku",
        "oyuncu_adi": "Oyuncu Adı"
    },
    "en": {
        "menü": ["🏠 Home", "📚 Theory Selection", "🎮 Simulation", "📊 Comparison", "📜 History & Profile", "🏆 Leaderboard", "ℹ️ About"],
        "tema": "Theme",
        "dil": "Language",
        "hosgeldin": "International Relations Theory Simulator",
        "basla": "Start Now",
        "teori_sec": "Theory Selection",
        "simulasyon": "Simulation",
        "karsilastirma": "Comparison",
        "hakkinda": "About",
        "terimler": "Glossary",
        "profil": "Personalized Theory Profile",
        "rapor_indir": "Download Report",
        "sesli_oku": "Read Aloud",
        "oyuncu_adi": "Player Name"
    }
}
dil = st.session_state["dil"]
metin = DIL[dil]

# ── Teori Verisi (8 teori) ───────────────────────
THEORIES = {
    "realizm": {
        "isim": "Realizm", "ikon": "🗡️",
        "varsayim": {"tr": "Devletler güvenlik odaklıdır; uluslararası sistem anarşiktir.", "en": "States are security-focused; international system is anarchic."},
        "aktor": {"tr": "Devletler (egemen ve üniter)", "en": "States (sovereign and unitary)"},
        "guc": {"tr": "Askeri ve ekonomik kapasite", "en": "Military and economic capacity"},
        "dunya": {"tr": "Güç mücadelesi; sıfır toplamlı", "en": "Power struggle; zero-sum"},
        "soz": {"tr": "“Güçlü olan elinden geleni yapar, zayıf olan çekmesi gerekeni çeker.” – Thukydides", "en": "“The strong do what they can and the weak suffer what they must.” – Thucydides"},
        "davranis": {"tr": "Askeri tehdit ve güç dengesi ile sonuç alır.", "en": "Resolves crises through military threats and balance of power."},
        "radar": [9,5,2,1], "olasilik": [78,22]
    },
    "liberalizm": {
        "isim": "Liberalizm", "ikon": "🕊️",
        "varsayim": {"tr": "İşbirliği mümkündür; kurumlar ve ticaret barışı getirir.", "en": "Cooperation is possible; institutions and trade bring peace."},
        "aktor": {"tr": "Devletler + Uluslararası örgütler + STK'lar", "en": "States + International organizations + NGOs"},
        "guc": {"tr": "Yumuşak güç, diplomasi, ekonomik refah", "en": "Soft power, diplomacy, economic prosperity"},
        "dunya": {"tr": "Artı toplamlı oyun; demokratik barış", "en": "Positive-sum game; democratic peace"},
        "soz": {"tr": "“Ebedi Barış, hukukla mümkündür.” – Immanuel Kant", "en": "“Perpetual peace is possible through law.” – Immanuel Kant"},
        "davranis": {"tr": "Uluslararası tahkim ve ortak projelerle kazan‑kazan arar.", "en": "Seeks win-win through international arbitration and joint projects."},
        "radar": [3,8,9,5], "olasilik": [18,82]
    },
    "konstrüktivizm": {
        "isim": "Konstrüktivizm", "ikon": "🧩",
        "varsayim": {"tr": "Uluslararası ilişkiler sosyal olarak inşa edilir; kimlikler ve normlar belirleyicidir.", "en": "IR is socially constructed; identities and norms are determinant."},
        "aktor": {"tr": "Devletler, norm üreticileri, bireyler", "en": "States, norm entrepreneurs, individuals"},
        "guc": {"tr": "Söylem ve kimlik üretme kapasitesi", "en": "Capacity to produce discourse and identity"},
        "dunya": {"tr": "Dost‑düşman kimliği değişkendir", "en": "Friend-enemy identity is fluid"},
        "soz": {"tr": "“Anarşi, devletlerin onu ne hale getirdiğidir.” – Alexander Wendt", "en": "“Anarchy is what states make of it.” – Alexander Wendt"},
        "davranis": {"tr": "Ortak kimlik inşası ve sembolik işbirliği önerir.", "en": "Proposes common identity building and symbolic cooperation."},
        "radar": [2,4,7,9], "olasilik": [30,70]
    },
    "marksizm": {
        "isim": "Marksizm / Bağımlılık", "ikon": "⚖️",
        "varsayim": {"tr": "Kapitalist sistem sömürü ilişkileri yaratır; çatışma sınıfsaldır.", "en": "Capitalist system creates exploitation; conflict is class-based."},
        "aktor": {"tr": "Sınıflar, çok uluslu şirketler", "en": "Classes, multinational corporations"},
        "guc": {"tr": "Üretim araçlarına sahiplik", "en": "Ownership of means of production"},
        "dunya": {"tr": "Merkez‑çevre hiyerarşisi", "en": "Core-periphery hierarchy"},
        "soz": {"tr": "“Az gelişmişlik, az geliştirilmişliktir.” – Andre Gunder Frank", "en": "“Underdevelopment is developed.” – Andre Gunder Frank"},
        "davranis": {"tr": "Şirketleri ifşa eder, ekonomik yapıyı dönüştürmeyi hedefler.", "en": "Exposes corporations, aims to transform economic structure."},
        "radar": [4,10,3,4], "olasilik": [65,35]
    },
    "feminizm": {
        "isim": "Feminizm", "ikon": "♀️",
        "varsayim": {"tr": "Uluslararası ilişkiler cinsiyetçi yapılar üzerine kuruludur.", "en": "IR is built on gendered structures."},
        "aktor": {"tr": "Devletler, toplumsal cinsiyet rolleri", "en": "States, gender roles"},
        "guc": {"tr": "Kapsayıcılık, eşitlik, görünürlük", "en": "Inclusivity, equality, visibility"},
        "dunya": {"tr": "Hiyerarşiler sadece maddi değil, cinsiyet temellidir.", "en": "Hierarchies are not only material but also gender-based."},
        "soz": {"tr": "“Kişisel olan politiktir.” – Carol Hanisch", "en": "“The personal is political.” – Carol Hanisch"},
        "davranis": {"tr": "Kararların kadınlar ve azınlıklar üzerindeki etkisini öne çıkarır.", "en": "Highlights impact on women and minorities."},
        "radar": [1,6,8,7], "olasilik": [25,75]
    },
    "post_kolonyal": {
        "isim": "Post‑kolonyalizm", "ikon": "🌍",
        "varsayim": {"tr": "Batı merkezli bilgi ve sömürgecilik mirası sistemi şekillendirir.", "en": "Western-centric knowledge and colonial legacy shape the system."},
        "aktor": {"tr": "Eski sömürgeler, küresel Güney", "en": "Former colonies, Global South"},
        "guc": {"tr": "Tarihsel anlatıları kontrol etme, kültürel direniş", "en": "Controlling historical narratives, cultural resistance"},
        "dunya": {"tr": "Merkez‑çevre, Batı‑dışı perspektifler", "en": "Core-periphery, non-Western perspectives"},
        "soz": {"tr": "“Avrupa'nın sessize aldığı halklar konuşacak.” – Dipesh Chakrabarty", "en": "“The silenced peoples of Europe will speak.” – Dipesh Chakrabarty"},
        "davranis": {"tr": "Emperyal geçmişi ifşa eder, eşitler arası diyalog arar.", "en": "Exposes imperial past, seeks equal dialogue."},
        "radar": [2,5,9,6], "olasilik": [40,60]
    },
    "yesil_teori": {
        "isim": "Yeşil Teori", "ikon": "🌿",
        "varsayim": {"tr": "Ekolojik sınırlar ve gezegenin sağlığı siyasetin merkezindedir.", "en": "Ecological limits and planetary health are central to politics."},
        "aktor": {"tr": "Ekosistemler, gelecek nesiller, çevreci hareketler", "en": "Ecosystems, future generations, environmental movements"},
        "guc": {"tr": "Sürdürülebilirlik, ekolojik ayak izi kontrolü", "en": "Sustainability, ecological footprint control"},
        "dunya": {"tr": "İnsan‑doğa uyumu; büyüme değil denge", "en": "Human-nature harmony; balance over growth"},
        "soz": {"tr": "“Doğa pazarlık masasında değil, masanın kendisidir.”", "en": "“Nature is not at the bargaining table, it is the table.”"},
        "davranis": {"tr": "Kaynakları koruma, yenilenebilir enerjiye geçiş ön plandadır.", "en": "Prioritizes resource conservation and renewable energy transition."},
        "radar": [0,7,10,5], "olasilik": [10,90]
    },
    "ingiliz_okulu": {
        "isim": "İngiliz Okulu", "ikon": "🏛️",
        "varsayim": {"tr": "Devletler bir 'uluslararası toplum' oluşturur; ortak normlar vardır.", "en": "States form an 'international society' with common norms."},
        "aktor": {"tr": "Devletler topluluğu, uluslararası kurumlar", "en": "Community of states, international institutions"},
        "guc": {"tr": "Meşruiyet, ortak değerler, diplomasi", "en": "Legitimacy, shared values, diplomacy"},
        "dunya": {"tr": "Anarşi ve düzen arasında uluslararası toplum", "en": "International society between anarchy and order"},
        "soz": {"tr": "“Uluslararası toplum, anarşinin içindeki düzendir.” – Hedley Bull", "en": "“International society is order within anarchy.” – Hedley Bull"},
        "davranis": {"tr": "Mevcut normları korur, çok taraflı müzakere ile krizi yönetir.", "en": "Preserves existing norms, manages crises through multilateral negotiation."},
        "radar": [5,5,6,4], "olasilik": [45,55]
    }
}

# ── Simülasyon Verisi (iki senaryo, neden açıklamaları ile) ──
SIM_DATA = {
    "Nehir Krizi": {
        "baslik": {"tr": "🌊 Nehir Krizi", "en": "🌊 River Crisis"},
        "senaryo_metni": {"tr": "Arkania baraj yaptı, Beledya susuz kaldı.", "en": "Arkania built a dam, Beledya is deprived of water."},
        "roller": {"tr": ["🏔️ Arkania", "🌾 Beledya"], "en": ["🏔️ Arkania", "🌾 Beledya"]},
        "asamalar": {
            1: {"durum": {"tr": "Arkania barajı yaptı. Beledya'da tarım çöküyor.", "en": "Arkania built dam. Agriculture collapsing in Beledya."},
                "secenekler": {
                    "realizm": [("Orduyu sınıra kaydır", "teorik", "🗡️ Güç gösterisi yaptınız.", "Realizm güç dengesini önemser (Morgenthau, 1948).")],
                    "liberalizm": [("BM'ye başvur", "teorik", "🕊️ Arabulucular devreye girdi.", "Liberalizm kurumlara güvenir (Keohane, 1984).")],
                    "konstrüktivizm": [("Ortak su geleneklerini duyur", "teorik", "🧩 'Komşu halklar' anlatısı yayıldı.", "Konstrüktivizm kimlik inşasını vurgular (Wendt, 1999).")],
                    "marksizm": [("Şirketin çıkarlarını ifşa et", "teorik", "⚖️ Şirket karşıtı tepki oluştu.", "Marksizm sermaye ilişkilerini sorgular (Frank, 1967).")],
                    "feminizm": [("Kadın çiftçilerin mağduriyetini öne çıkar", "teorik", "♀️ Görünürlük sağlandı.", "Feminizm cinsiyetçi yapıları ifşa eder (Enloe, 1989).")],
                    "post_kolonyal": [("Suyun sömürge dönemi paylaşımını hatırlat", "teorik", "🌍 Tarihsel adalet gündemi.", "Post‑kolonyalizm Batı merkezli söylemi yapısöküme uğratır (Chakrabarty, 2000).")],
                    "yesil_teori": [("Nehir ekosisteminin çöküşüne dikkat çek", "teorik", "🌿 Ekolojik hassasiyet öne çıktı.", "Yeşil teori ekolojiyi merkeze alır (Eckersley, 2004).")],
                    "ingiliz_okulu": [("Uluslararası Nehir Hukuku'nu uygula", "teorik", "🏛️ Normlara dayalı adım.", "İngiliz Okulu ortak normları savunur (Bull, 1977).")]
                }
            },
            2: {"durum": {"tr": "Arkania suyu kıstı. Kıtlık başladı.", "en": "Arkania cut water. Famine began."},
                "secenekler": {
                    "realizm": [("Askeri ittifak kur", "teorik", "🗡️ Arkania yalnızlaştı.", "Realizm ittifakları güç dengesi için kullanır (Waltz, 1979).")],
                    "liberalizm": [("Model anlaşma öner", "teorik", "🕊️ Nil Havzası örneği masada.", "Liberalizm başarılı modelleri yayar (Keohane, 1984).")],
                    "konstrüktivizm": [("Ortak festival öner", "teorik", "🧩 Festival viraldi.", "Konstrüktivizm ortak kimlik inşasını teşvik eder (Wendt, 1999).")],
                    "marksizm": [("Sınır ötesi işçi dayanışması", "teorik", "⚖️ Dayanışma güçlendi.", "Marksizm sınıf dayanışmasını esas alır (Marx, 1867).")],
                    "feminizm": [("Kadın kooperatiflerini destekle", "teorik", "♀️ Ekonomik güçlenme.", "Feminizm kadın emeğini görünür kılar (Peterson, 1992).")],
                    "post_kolonyal": [("Güney ülkeleriyle dayanışma", "teorik", "🌍 Küresel Güney birleşiyor.", "Post‑kolonyalizm Güney dayanışmasını savunur (Said, 1978).")],
                    "yesil_teori": [("Ortak ekoloji planı", "teorik", "🌿 Sürdürülebilir adım.", "Yeşil teori ekosistem ortaklığını vurgular (Eckersley, 2004).")],
                    "ingiliz_okulu": [("Uluslararası Konferans düzenle", "teorik", "🏛️ Normatif tartışma başladı.", "İngiliz Okulu çok taraflılığı önemser (Bull, 1977).")]
                }
            },
            3: {"durum": {"tr": "Taraflar yoruldu. Çözüm için son karar.", "en": "Parties exhausted. Final decision."},
                "secenekler": {
                    "realizm": [("İkili anlaşma (güç dengesi)", "teorik", "🗡️ Arkania suyu serbest bıraktı.", "Realizm nihai çözümü güçle dayatır (Mearsheimer, 2001).")],
                    "liberalizm": [("BM garantörlüğünde anlaşma", "teorik", "🕊️ Tarihi anlaşma.", "Liberalizm kurumsal çerçeveyi zorunlu görür (Ikenberry, 2001).")],
                    "konstrüktivizm": [("Barış Beyannamesi imzala", "teorik", "🧩 Yeni komşu kimliği.", "Konstrüktivizm norm değişikliği ile barışı sağlar (Wendt, 1999).")],
                    "marksizm": [("Barajı ortak kamuya devret", "teorik", "⚖️ Şirket çekildi.", "Marksizm üretim araçlarının toplumsallaşmasını hedefler (Lenin, 1917).")],
                    "feminizm": [("Cinsiyet eşitliğini antlaşmaya ekle", "teorik", "♀️ Dönüştürücü adım.", "Feminizm anlaşmalara cinsiyet perspektifi ekler (Tickner, 1992).")],
                    "post_kolonyal": [("Tarihsel özür ve tazminat", "teorik", "🌍 Onarıcı adalet.", "Post‑kolonyalizm geçmişle yüzleşmeyi şart koşar (Fanon, 1961).")],
                    "yesil_teori": [("Nehir ekosistemini koruma altına al", "teorik", "🌿 Doğa kazandı.", "Yeşil teori doğanın haklarını tanır (Eckersley, 2004).")],
                    "ingiliz_okulu": [("Ortak normatif çerçeve anlaşması", "teorik", "🏛️ Toplum inşası.", "İngiliz Okulu normların kurumsallaşmasını savunur (Bull, 1977).")]
                }
            }
        }
    },
    "Ticaret Savaşları": {
        "baslik": {"tr": "💼 Ticaret Savaşları", "en": "💼 Trade Wars"},
        "senaryo_metni": {"tr": "Komşu ülke dampingli ihracat yapıyor, yerli sanayi tehlikede.", "en": "Neighbor country dumps exports, domestic industry at risk."},
        "roller": {"tr": ["🏭 Sanayi Ülkesi", "🌾 Tarım Ülkesi"], "en": ["🏭 Industrial Country", "🌾 Agricultural Country"]},
        "asamalar": {
            1: {"durum": {"tr": "Komşu ülke dampingli ihracat yapıyor.", "en": "Neighbor country dumps exports."},
                "secenekler": {
                    "realizm": [("Yüksek gümrük vergisi koy", "teorik", "🗡️ Korumacı güç gösterisi.", "Realizm ekonomiyi ulusal güvenlik aracı olarak görür (Gilpin, 1987).")],
                    "liberalizm": [("Serbest ticaret anlaşması öner", "teorik", "🕊️ Karşılıklı kazanç.", "Liberalizm serbest ticareti barışın anahtarı sayar (Ricardo, 1817).")],
                    "konstrüktivizm": [("Ticaretin kültürel boyutunu vurgula", "teorik", "🧩 Ortak kimlik inşası.", "Konstrüktivizm ekonomik ilişkilerin sosyal inşasını vurgular (Ruggie, 1982).")],
                    "marksizm": [("Damping yapan çok uluslu şirketleri ifşa et", "teorik", "⚖️ Emekçi dayanışması.", "Marksizm çok uluslu şirketleri sermaye aracı olarak görür (Wallerstein, 1974).")],
                    "feminizm": [("Kadın girişimcilerin zararını öne çıkar", "teorik", "♀️ Toplumsal cinsiyet farkındalığı.", "Feminizm ticaret politikalarında cinsiyet etkisini sorgular (Griffin, 2009).")],
                    "post_kolonyal": [("Kuzey-Güney eşitsizliğini gündeme getir", "teorik", "🌍 Adaletsiz ticaret.", "Post‑kolonyalizm eşitsiz ticaret ilişkilerini ifşa eder (Rodney, 1972).")],
                    "yesil_teori": [("Karbon ayak izi düzenlemesiyle yeşil ticaret öner", "teorik", "🌿 Sürdürülebilir ticaret.", "Yeşil teori ekolojik dengeyi ticarete entegre eder (Daly, 1996).")],
                    "ingiliz_okulu": [("DTÖ kurallarına başvur", "teorik", "🏛️ Normatif çerçeve.", "İngiliz Okulu kurallara dayalı uluslararası toplumu savunur (Bull, 1977).")]
                }
            },
            2: {"durum": {"tr": "Misilleme yapıldı. Sektörler zarar görüyor.", "en": "Retaliation occurred. Sectors damaged."},
                "secenekler": {
                    "realizm": [("Ekonomik yaptırımları artır", "teorik", "🗡️ Güç savaşı.", "Realizm ekonomik yaptırımı stratejik araç sayar (Pape, 1997).")],
                    "liberalizm": [("Uluslararası tahkime başvur", "teorik", "🕊️ Kurumsal çözüm.", "Liberalizm ihtilafların hukuki çözümünü önerir (Keohane, 1984).")],
                    "konstrüktivizm": [("Ortak ticaret kültürü oluşturma çağrısı", "teorik", "🧩 Norm inşası.", "Konstrüktivizm paylaşılan anlamları dönüştürmeyi hedefler (Wendt, 1999).")],
                    "marksizm": [("İşçi sendikalarını sınır ötesi işbirliğine çağır", "teorik", "⚖️ Sınıf dayanışması.", "Marksizm işçi sınıfının uluslararası birliğini savunur (Marx & Engels, 1848).")],
                    "feminizm": [("Kadın istihdamını koruma paketi açıkla", "teorik", "♀️ Eşitlikçi politika.", "Feminizm ekonomik krizlerin kadınları orantısız etkilediğini belirtir (Elson, 1995).")],
                    "post_kolonyal": [("Küresel Güney ticaret bloğu oluştur", "teorik", "🌍 Dayanışma.", "Post‑kolonyalizm alternatif ekonomik yapılar önerir (Amin, 1990).")],
                    "yesil_teori": [("Yeşil dönüşüm fonu öner", "teorik", "🌿 Ortak gelecek.", "Yeşil teori ekonomik dönüşümü ekolojik temelde ele alır (Jackson, 2009).")],
                    "ingiliz_okulu": [("Uluslararası Ticaret Örgütü'ne başvur", "teorik", "🏛️ Normatif çözüm.", "İngiliz Okulu uluslararası toplumun kurallarına vurgu yapar (Bull, 1977).")]
                }
            },
            3: {"durum": {"tr": "Ekonomik daralma derinleşiyor. Halk sokağa döküldü.", "en": "Recession deepens. Public unrest."},
                "secenekler": {
                    "realizm": [("Askeri güçle ticareti zorla", "teorik", "🗡️ Hegemonik çözüm.", "Realizm nihai kertede askeri güce başvurur (Mearsheimer, 2001).")],
                    "liberalizm": [("Kapsamlı serbest ticaret anlaşması imzala", "teorik", "🕊️ Kalıcı barış.", "Liberalizm serbest ticaretin barış getireceğine inanır (Oneal & Russett, 1999).")],
                    "konstrüktivizm": [("Ortak refah kimliği inşa eden anlaşma", "teorik", "🧩 Yeni norm.", "Konstrüktivizm kimlik dönüşümünün işbirliğini kalıcılaştırdığını savunur (Wendt, 1999).")],
                    "marksizm": [("Üretim araçlarını kamulaştır, adil ticaret kooperatifi kur", "teorik", "⚖️ Yapısal dönüşüm.", "Marksizm kapitalist ilişkilerin kökten değişimini öngörür (Marx, 1867).")],
                    "feminizm": [("Cinsiyet bütçelemesi ve kapsayıcı ticaret anlaşması", "teorik", "♀️ Dönüştürücü.", "Feminizm bütçelerin cinsiyete duyarlı olmasını talep eder (Budlender, 2002).")],
                    "post_kolonyal": [("Tarihsel sömürüyü tanıyan tazminat ve yeni ekonomik düzen", "teorik", "🌍 Onarıcı.", "Post‑kolonyalizm yapısal adaletsizliği gidermeyi amaçlar (Fanon, 1961).")],
                    "yesil_teori": [("Yeşil ekonomiye geçiş anlaşması", "teorik", "🌿 Sürdürülebilir.", "Yeşil teori büyüme yerine refahı koyar (Jackson, 2009).")],
                    "ingiliz_okulu": [("Ortak ticaret normları ve etik kurallar sözleşmesi", "teorik", "🏛️ Toplum inşası.", "İngiliz Okulu uluslararası toplumun normatif temellerini güçlendirir (Bull, 1977).")]
                }
            }
        }
    }
}

# ── Yardımcı fonksiyonlar ────────────────────────
def seslendir(metin):
    """Tarayıcıda metni seslendirir."""
    js = f"""
    <script>
        if (window.speechSynthesis) {{
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance(`{metin}`);
            utterance.lang = '{dil}';
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """
    st.components.v1.html(js, height=0)

def rapor_olustur():
    puan = st.session_state["sim_puan"]
    teori = THEORIES[st.session_state["secilen_teori"]]
    rapor = f"""
    Uİ Teori Simülatörü Raporu
    Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    Teori: {teori['ikon']} {teori['isim']}
    Senaryo: {st.session_state['scenario']}
    Rol: {st.session_state['sim_rol']}
    Teori Uyum Puanı: {puan}/3
    Kararlar:
    """
    for s in st.session_state["sim_secimler"]:
        rapor += f"\n Aşama {s['asama']}: {s['secim']} ({s['tip']})"
    rapor += f"\n\n Sonuç: {SONUCLAR[puan]}"
    return rapor

SONUCLAR = {
    3: "🏆 Mükemmel Teorik Tutarlılık!",
    2: "⚖️ Dengeli Pragmatist.",
    1: "🌪️ Kriz Yönetimi Zayıf.",
    0: "💥 Tam Kaos."
}

# ── Sidebar ───────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Uİ Teori Simülatörü")
    col1, col2 = st.columns(2)
    with col1:
        tema_secenek = st.radio(metin["tema"], ["🌞 Açık", "🌙 Koyu"], index=0 if st.session_state["tema"] == "🌞 Açık" else 1, key="tema_radio")
        if tema_secenek != st.session_state["tema"]:
            st.session_state["tema"] = tema_secenek
            st.rerun()
    with col2:
        dil_secenek = st.radio(metin["dil"], ["tr", "en"], index=0 if st.session_state["dil"] == "tr" else 1, key="dil_radio")
        if dil_secenek != st.session_state["dil"]:
            st.session_state["dil"] = dil_secenek
            st.rerun()

    menu = metin["menü"]
    secim = st.radio("Menü", menu, index=menu.index(st.session_state["page"]) if st.session_state["page"] in menu else 0)
    if secim != st.session_state["page"]:
        st.session_state["page"] = secim
        st.rerun()

    if st.session_state["secilen_teori"]:
        t = THEORIES[st.session_state["secilen_teori"]]
        st.info(f"Seçili: {t['ikon']} {t['isim']}")

# ── Sayfa: Ana Sayfa ─────────────────────────────
def show_home():
    st.title(f"🌍 {metin['hosgeldin']}")
    st.markdown(f"**8 teori, 2 senaryo, sesli anlatım, profil analizi ve çok daha fazlası!**")
    col1, col2, col3 = st.columns(3)
    col1.metric("📚", metin["teori_sec"], "1. Adım")
    col2.metric("🎮", metin["simulasyon"], "2. Adım")
    col3.metric("📊", metin["karsilastirma"], "3. Adım")
    if st.button(f"🚀 {metin['basla']}"):
        st.session_state["page"] = metin["menü"][1]
        st.rerun()

    with st.expander(f"📖 {metin['terimler']}"):
        terimler = {
            "Anarşi": {"tr": "Uluslararası sistemde üstün bir otoritenin bulunmaması.", "en": "Absence of a supreme authority in the international system."},
            "Güvenlik İkilemi": {"tr": "Bir devletin güvenlik adına attığı adımların diğerlerini tehdit edip silahlanmaya yol açması.", "en": "A state's security actions threatening others, leading to an arms race."}
        }
        for t, ac in terimler.items():
            st.markdown(f"**{t}**: {ac[dil]}")

# ── Sayfa: Teori Seçimi ──────────────────────────
def show_theory_selection():
    st.title(f"📚 {metin['teori_sec']}")
    col1, col2 = st.columns([1, 2])
    with col1:
        tid_list = list(THEORIES.keys())
        sec = st.selectbox("Teori seçin", range(len(tid_list)),
                           format_func=lambda i: f"{THEORIES[tid_list[i]]['ikon']} {THEORIES[tid_list[i]]['isim']}")
        teori = THEORIES[tid_list[sec]]
        if st.button("🎮 Simülasyona Başla"):
            st.session_state["secilen_teori"] = tid_list[sec]
            for k in ["scenario", "sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
                if k in st.session_state: del st.session_state[k]
            init_state()
            st.session_state["page"] = metin["menü"][2]
            st.rerun()
    with col2:
        st.subheader(f"{teori['ikon']} {teori['isim']}")
        st.markdown(f"**Temel Varsayım:** {teori['varsayim'][dil]}")
        st.markdown(f"**Ana Aktörler:** {teori['aktor'][dil]}")
        st.markdown(f"**Güç Tanımı:** {teori['guc'][dil]}")
        st.markdown(f"**Dünya Görüşü:** {teori['dunya'][dil]}")
        st.info(teori['soz'][dil])
        st.caption(f"Kriz Davranışı: {teori['davranis'][dil]}")

# ── Sayfa: Simülasyon ────────────────────────────
def show_simulation():
    if not st.session_state.get("secilen_teori"):
        st.warning("Önce bir teori seçin.")
        if st.button("Teori Seçimine Git"):
            st.session_state["page"] = metin["menü"][1]
            st.rerun()
        return

    teori = THEORIES[st.session_state["secilen_teori"]]
    st.title(f"🎮 {metin['simulasyon']} — {teori['ikon']} {teori['isim']}")

    if st.session_state.get("scenario") is None:
        senaryo_secenek = list(SIM_DATA.keys())
        sec = st.radio("Senaryo seçin", senaryo_secenek, format_func=lambda x: SIM_DATA[x]["baslik"][dil])
        if st.button("Senaryoyu Onayla"):
            st.session_state["scenario"] = sec
            st.rerun()
        return

    senaryo = SIM_DATA[st.session_state["scenario"]]
    tid = st.session_state["secilen_teori"]
    if st.session_state["sim_asama"] == 0:
        rol = st.radio("Rolünüz:", senaryo["roller"][dil])
        if st.button("Oyuna Başla"):
            st.session_state["sim_rol"] = rol
            st.session_state["sim_asama"] = 1
            st.rerun()
        return

    if st.session_state["sim_bitti"]:
        show_result()
        return

    asama = st.session_state["sim_asama"]
    a = senaryo["asamalar"][asama]
    st.subheader(f"Aşama {asama}/3")
    st.write(a["durum"][dil])
    if st.button(metin["sesli_oku"]):
        seslendir(a["durum"][dil])

    if tid not in a["secenekler"]: tid = "realizm"
    secenekler = a["secenekler"][tid]
    sec_text = [s[0] for s in secenekler]
    secim = st.radio("Eylem:", sec_text, key=f"s{asama}")
    sec = secenekler[sec_text.index(secim)]
    st.info(f"**Teorik Neden:** {sec[3]}")

    if st.button("Kararı Uygula"):
        if sec[1] == "teorik": st.session_state["sim_puan"] += 1
        st.session_state["sim_secimler"].append({"asama": asama, "secim": sec[0], "tip": sec[1], "feedback": sec[2]})
        st.session_state["sim_asama"] += 1
        if st.session_state["sim_asama"] > 3:
            st.session_state["sim_bitti"] = True
            st.session_state["gecmis"].append({
                "tarih": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "teori": teori['isim'],
                "senaryo": st.session_state["scenario"],
                "puan": st.session_state["sim_puan"],
                "secimler": st.session_state["sim_secimler"].copy()
            })
        st.rerun()

    if st.session_state["sim_secimler"]:
        for s in st.session_state["sim_secimler"]:
            st.write(s["feedback"])

def show_result():
    puan = st.session_state["sim_puan"]
    teori = THEORIES[st.session_state["secilen_teori"]]
    sonuc = SONUCLAR[puan]
    st.success(f"## {sonuc}")
    col1, col2 = st.columns(2)
    col1.metric("Teori Uyum Puanı", f"{puan}/3")
    col2.write(f"**Teorik Beklenti:** {teori['davranis'][dil]}")
    # 3D grafik
    teorik = sum(1 for s in st.session_state["sim_secimler"] if s["tip"] == "teorik")
    pragmatik = sum(1 for s in st.session_state["sim_secimler"] if s["tip"] == "pragmatik")
    aykiri = 3 - teorik - pragmatik
    fig3 = go.Figure(go.Scatter3d(x=[teorik], y=[pragmatik], z=[aykiri], mode='markers+text', marker=dict(size=15, color='#FF6B35'), text=["Senin Kararların"]))
    fig3.update_layout(scene=dict(xaxis_title="Teorik", yaxis_title="Pragmatik", zaxis_title="Aykırı", xaxis=dict(range=[0,3]), yaxis=dict(range=[0,3]), zaxis=dict(range=[0,3])), height=400)
    st.plotly_chart(fig3, use_container_width=True)
    # Rapor indir
    rapor = rapor_olustur()
    st.download_button(metin["rapor_indir"], rapor, f"rapor_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
    if st.button("🔄 Sıfırla"):
        for k in ["scenario", "sim_asama", "sim_puan", "sim_rol", "sim_secimler", "sim_bitti"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

# ── Sayfa: Karşılaştırma ─────────────────────────
def show_comparison():
    st.title(f"📊 {metin['karsilastirma']}")
    df = pd.DataFrame({ "Teori": [f"{t['ikon']} {t['isim']}" for t in THEORIES.values()], "Aktör": [t['aktor'][dil] for t in THEORIES.values()], "Güç": [t['guc'][dil] for t in THEORIES.values()] })
    st.dataframe(df, use_container_width=True, hide_index=True)

    kategoriler = ["Askeri", "Ekonomi", "İşbirliği", "Birey"]
    fig_radar = go.Figure()
    for tid, t in THEORIES.items():
        fig_radar.add_trace(go.Scatterpolar(r=t["radar"]+[t["radar"][0]], theta=kategoriler+[kategoriler[0]], fill='toself', name=f"{t['ikon']} {t['isim']}"))
    fig_radar.update_layout(height=400)
    st.plotly_chart(fig_radar, use_container_width=True)

    fig_bar = go.Figure(data=[
        go.Bar(name="Çatışma", x=list(THEORIES.keys()), y=[t["olasilik"][0] for t in THEORIES.values()]),
        go.Bar(name="İşbirliği", x=list(THEORIES.keys()), y=[t["olasilik"][1] for t in THEORIES.values()])
    ])
    st.plotly_chart(fig_bar, use_container_width=True)

    # 3D Scatter
    st.subheader("🌐 3D Teori Konumlandırması")
    fig_3d = go.Figure()
    for tid, t in THEORIES.items():
        fig_3d.add_trace(go.Scatter3d(x=[t["radar"][0]], y=[t["radar"][1]], z=[t["radar"][2]], mode='markers+text', marker=dict(size=t["radar"][3]*5, color=t["radar"][3], colorscale='Viridis'), text=f"{t['ikon']} {t['isim']}"))
    fig_3d.update_layout(scene=dict(xaxis_title="Askeri", yaxis_title="Ekonomi", zaxis_title="İşbirliği"), height=500)
    st.plotly_chart(fig_3d, use_container_width=True)

# ── Sayfa: Geçmiş & Profil ───────────────────────
def show_history():
    st.title("📜 Geçmiş & Profil")
    st.subheader(metin["oyuncu_adi"])
    ad = st.text_input("Adınız", st.session_state["oyuncu_adi"])
    if ad != st.session_state["oyuncu_adi"]:
        st.session_state["oyuncu_adi"] = ad
    if st.session_state["gecmis"]:
        df = pd.DataFrame(st.session_state["gecmis"])
        st.dataframe(df)
        # Profil
        if st.session_state["oyuncu_adi"]:
            teoriler = [g["teori"] for g in st.session_state["gecmis"]]
            profil = {t: teoriler.count(t) for t in set(teoriler)}
            st.subheader(metin["profil"])
            fig = go.Figure(go.Bar(x=list(profil.keys()), y=list(profil.values())))
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"{metin['oyuncu_adi']}: {st.session_state['oyuncu_adi']}, Toplam oyun: {len(st.session_state['gecmis'])}")
    else:
        st.info("Henüz simülasyon oynanmadı.")

# ── Sayfa: Skor Tablosu ──────────────────────────
def show_leaderboard():
    st.title("🏆 Skor Tablosu")
    if st.session_state["oyuncu_adi"] and st.session_state["sim_bitti"]:
        st.session_state["skorlar"].append({"isim": st.session_state["oyuncu_adi"], "puan": st.session_state["sim_puan"], "tarih": datetime.now().strftime('%Y-%m-%d %H:%M')})
    if st.session_state["skorlar"]:
        df = pd.DataFrame(st.session_state["skorlar"]).sort_values("puan", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Henüz skor yok.")

# ── Sayfa: Hakkında ──────────────────────────────
def show_about():
    st.title(f"ℹ️ {metin['hakkinda']}")
    st.markdown("Eğitim amaçlı Uluslararası İlişkiler simülatörü. 8 teori, 2 senaryo, ses, profil, skor tablosu içerir.")

# ── Sayfa Yönlendirme ────────────────────────────
page = st.session_state["page"]
if page == metin["menü"][0]: show_home()
elif page == metin["menü"][1]: show_theory_selection()
elif page == metin["menü"][2]: show_simulation()
elif page == metin["menü"][3]: show_comparison()
elif page == metin["menü"][4]: show_history()
elif page == metin["menü"][5]: show_leaderboard()
elif page == metin["menü"][6]: show_about()
