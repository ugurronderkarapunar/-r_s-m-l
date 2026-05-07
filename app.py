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
# GLOBAL CSS
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

    /* Aşama göstergesi */
    .asama-bar {
        display: flex;
        gap: 8px;
        margin-bottom: 24px;
    }
    .asama-daire {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 15px;
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
        font-family: 'Source Sans 3', sans-serif;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(26, 60, 110, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B35 0%, #E5572A 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
    }

    /* Seçim kutuları */
    .stRadio [data-baseweb="radio"] {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 6px;
        background: #F7FAFC;
        border: 1px solid #E2E8F0;
    }

    /* Ayırıcı çizgi */
    hr {
        border: none;
        border-top: 2px solid #E2E8F0;
        margin: 24px 0;
    }

    /* Sidebar logo alanı */
    .sidebar-logo {
        padding: 16px;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 16px;
    }
    .sidebar-logo-metin {
        color: #B3C6E0;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Alıntı kutusu */
    .alinti {
        background: #EBF4FF;
        border-left: 4px solid #1A3C6E;
        border-radius: 0 8px 8px 0;
        padding: 16px 20px;
        font-style: italic;
        font-size: 15px;
        color: #2C5282;
        margin: 16px 0;
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
        "ana_aktorler": "Devletler, uluslararası örgütler (BM, Dünya Bankası), çok uluslu şirketler ve sivil toplum kuruluşları.",
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
# SİMÜLASYON KARAR AĞACI VERİSİ
# ─────────────────────────────────────────────
SIMULATION_DATA = {
    1: {
        "baslik": "⚡ Aşama 1: İlk Tepki",
        "durum": "Arkania'nın barajı faaliyete geçti. Beledya'da çiftçiler isyan noktasında. Uluslararası kamuoyunun gözleri bu krize çevrildi. İlk adımını seçiyorsunuz.",
        "secenekler": {
            "realizm": [
                ("Orduyu nehir sınırına konuşlandır; Arkania'ya güç sinyali ver.", "teorik",
                 "🗡️ **Realist hamle:** Güç projeksiyonu karşı tarafı masaya oturtuyor. Arkania savunma pozisyonu alıyor; gerginlik tırmanıyor ama diyalog kapısı kapanmadı."),
                ("BM Su Hukuku Komisyonu'na başvur, uluslararası tahkim iste.", "zit",
                 "🕊️ **Teoriye aykırı:** Uluslararası kurumlara güven realist anlayışla çelişiyor. Süreç uzuyor, Arkania zaman kazanıyor."),
                ("Diplomatik kanal aç; su paylaşım müzakerelerine çağır.", "pragmatik",
                 "🤝 **Pragmatik yaklaşım:** Görüşmeler başladı ancak Arkania somut adım atmakta isteksiz. Zaman kazanılıyor ama sonuç belirsiz."),
            ],
            "liberalizm": [
                ("BM Su Hukuku Komisyonu'na başvur, uluslararası tahkim iste.", "teorik",
                 "🕊️ **Liberal hamle:** Uluslararası toplumun dikkati çekildi. Arabulucu devletler devreye girdi; müzakere süreci resmen başladı."),
                ("Orduyu nehir sınırına konuşlandır; Arkania'ya güç sinyali ver.", "zit",
                 "🗡️ **Teoriye aykırı:** Askeri yığınak liberal değerlerle çelişiyor. Uluslararası kamuoyu Beledya'yı eleştiriyor."),
                ("Diplomatik kanal aç; su paylaşım müzakerelerine çağır.", "pragmatik",
                 "🤝 **Pragmatik yaklaşım:** Görüşmeler başladı, ancak kurumsal destek olmadan süreç yavaş ilerliyor."),
            ],
            "konstrüktivizm": [
                ("İki ülkenin ortak tarihsel su kullanım geleneklerini kamuoyuna duyur; 'nehir komşuluğu' kimliğini vurgula.", "teorik",
                 "🧩 **Konstrüktivist hamle:** Medyada 'komşu halklar' anlatısı yankı uyandırdı. Arkania'da muhalefet seslendi; kimlik çerçevesi yumuşamaya başladı."),
                ("Orduyu nehir sınırına konuşlandır; Arkania'ya güç sinyali ver.", "zit",
                 "🗡️ **Teoriye aykırı:** Güç gösterisi 'düşman kimliği' söylemini pekiştiriyor; toplumsal ayrışma derinleşiyor."),
                ("Diplomatik kanal aç; su paylaşım müzakerelerine çağır.", "pragmatik",
                 "🤝 **Pragmatik yaklaşım:** Diplomatik temas kuruldu ama kimlik dönüşümü sağlanamadı; çözüm yüzeysel kalabilir."),
            ],
            "marksizm": [
                ("Barajı inşa eden Kuzey Avrupa şirketinin ekonomik çıkarlarını ve hükümet bağlantılarını kamuoyuyla paylaş.", "teorik",
                 "⚖️ **Marksist hamle:** Uluslararası kamuoyunda şirket karşıtı ses yükseldi. Yatırımcılar temkinli; Arkania hükümeti iç baskıyla karşılaşıyor."),
                ("BM Su Hukuku Komisyonu'na başvur; uluslararası tahkim iste.", "zit",
                 "🕊️ **Teoriye aykırı:** BM kurumları kapitalist düzenin bir parçası; bu yol gerçek sorunu değil belirtisini çözüyor."),
                ("Diplomatik kanal aç; su paylaşım müzakerelerine çağır.", "pragmatik",
                 "🤝 **Pragmatik yaklaşım:** Görüşme masası kuruldu; ancak ekonomik yapı değişmeden çözüm geçici olacak."),
            ],
        }
    },
    2: {
        "baslik": "🔥 Aşama 2: Kriz Tırmanıyor",
        "durum": "Arkania su akışını daha da kıstı. Beledya'nın tahıl üretimi çöktü. Komşu ülkeler taraf seçmeye başladı. Kritik bir karar noktasındasın.",
        "secenekler": {
            "realizm": [
                ("Bölgesel güç dengesini değiştirmek için Arkania'nın rakip komşusuyla askeri ittifak kur.", "teorik",
                 "🗡️ **Realist hamle:** İttifak kuruldu! Arkania yalnızlaştı. Güç dengesi değişince Arkania müzakereye daha açık hale geldi."),
                ("Uluslararası yardım çağrısında bulun; insani kriz ilan et.", "zit",
                 "🆘 **Teoriye aykırı:** Güçten değil zafiyetten yapılan çağrı realist perspektifle çelişiyor. Arkania taviz verme gereği duymuyor."),
                ("Ekonomik yaptırım tehdidini uluslararası destekle masaya koy.", "pragmatik",
                 "💼 **Pragmatik yaklaşım:** Yaptırım tehdidi Arkania'yı düşündürdü; ancak destek yetersiz kalınca etki sınırlı."),
            ],
            "liberalizm": [
                ("Bölgesel su anlaşmazlıklarını çözen başarılı uluslararası model anlaşmaları öneri olarak sun.", "teorik",
                 "🕊️ **Liberal hamle:** Nil Havzası Girişimi ve Helsinki Kuralları örnek gösterildi. Ortak çerçeve müzakereye ivme kazandırdı."),
                ("Bölgesel güç dengesini değiştirmek için askeri ittifak kur.", "zit",
                 "🗡️ **Teoriye aykırı:** Askeri bloklaşma liberal işbirliği zeminini tahrip ediyor; üçüncü ülkeler çekiniyor."),
                ("Ekonomik yaptırım tehdidini uluslararası destekle masaya koy.", "pragmatik",
                 "💼 **Pragmatik yaklaşım:** Kademeli baskı işe yarıyor; Arkania bazı teknik uzlaşılara açık sinyaller veriyor."),
            ],
            "konstrüktivizm": [
                ("İki ülke halklarını buluşturan ortak kültürel su festivali öner; 'Bereket Nehri Ortak Mirasımız' kampanyası başlat.", "teorik",
                 "🧩 **Konstrüktivist hamle:** Festival fikri viral oldu. Her iki ülkede sivil toplum harekete geçti; 'düşman ülke' söylemi zayıfladı."),
                ("Bölgesel güç dengesini değiştirmek için askeri ittifak kur.", "zit",
                 "🗡️ **Teoriye aykırı:** Askeri bloklaşma toplumlar arası 'biz' ve 'onlar' kimliğini pekiştiriyor; dönüşüm güçleşiyor."),
                ("Ekonomik yaptırım tehdidini uluslararası destekle masaya koy.", "pragmatik",
                 "💼 **Pragmatik yaklaşım:** Ekonomik baskı Arkania'yı yavaşlattı ama kimlik düzeyinde bir değişim yaratmadı."),
            ],
            "marksizm": [
                ("İki ülke işçi sınıfı ve çiftçi örgütlerini sınır ötesi dayanışmaya çağır; elitleri değil halkları muhatap al.", "teorik",
                 "⚖️ **Marksist hamle:** Sınır ötesi dayanışma güçlendi. Her iki hükümet de halktan baskı görüyor; şirketlerin rolü sorgulanmaya başlandı."),
                ("Bölgesel güç dengesini değiştirmek için askeri ittifak kur.", "zit",
                 "🗡️ **Teoriye aykırı:** Devlet-devlet ittifakı sermayenin gücünü sorgulamıyor; sadece egemen çıkarlar öne çıkıyor."),
                ("Ekonomik yaptırım tehdidini uluslararası destekle masaya koy.", "pragmatik",
                 "💼 **Pragmatik yaklaşım:** Yaptırım tehdidi şirketin çıkarlarını etkiliyor; ancak sınıfsal yapı bozulmadı."),
            ],
        }
    },
    3: {
        "baslik": "🌊 Aşama 3: Son Hamle",
        "durum": "Taraflar yoruldu. Uluslararası kamuoyu bir çözüm bekliyor. Bu son hamle, krizin seyrini ve tarihsel mirasını belirleyecek.",
        "secenekler": {
            "realizm": [
                ("Müzakere masasında su akışı garantisi karşılığında Arkania'ya sınır güvencesi ver; ikili anlaşmayı imzala.", "teorik",
                 "🗡️ **Realist hamle:** Güç temelli pazarlık sonuç verdi. Arkania %25 su akışını serbest bıraktı. Kalıcı değil ama mevcut güç dengesi korundu."),
                ("Konuyu BM Güvenlik Konseyi'ne taşı; uluslararası yaptırım karar tasarısı hazırla.", "zit",
                 "🇺🇳 **Teoriye aykırı:** Büyük güçlerin veto refleksi devreye girdi. Karar tasarısı beklendiği etkiyi yaratmadı."),
                ("Su paylaşımını teknik komisyona havale et; 6 ay süre ver.", "pragmatik",
                 "📋 **Pragmatik yaklaşım:** Komisyon çalışmaları başladı; süreç uzuyor ancak şiddet riski azaldı."),
            ],
            "liberalizm": [
                ("BM ve bölgesel örgütlerin garantörlüğünde kapsamlı su paylaşım antlaşması imzala.", "teorik",
                 "🕊️ **Liberal hamle:** Tarihi anlaşma! Kurumsal çerçeve sağlam; her iki taraf da denetim mekanizmalarını kabul etti. Bölgede emsal oluştu."),
                ("Müzakere masasında güç temelli pazarlık yap; karşılıklı taviz al.", "zit",
                 "🗡️ **Teoriye aykırı:** İkili pazarlık kurumsal güvencelerden yoksun; ilk kriz anında bozulabilir."),
                ("Su paylaşımını teknik komisyona havale et; 6 ay süre ver.", "pragmatik",
                 "📋 **Pragmatik yaklaşım:** Teknik çözüm sağlandı; ancak kurumsal meşruiyet eksik kaldı."),
            ],
            "konstrüktivizm": [
                ("İki ülke arasında ortak kimlik vurgulamalı 'Bereket Nehri Barış Beyannamesi'ni kamuoyu önünde imzalat.", "teorik",
                 "🧩 **Konstrüktivist hamle:** Sembolik ama güçlü! Beyanname her iki ülkede kamuoyu nezdinde yeni bir 'komşu kimliği' pekiştirdi. Gelecekteki anlaşmazlıklar için zemin değişti."),
                ("Müzakere masasında güç temelli pazarlık yap.", "zit",
                 "🗡️ **Teoriye aykırı:** Güç temelli çözüm kimlik dönüşümünü geri alıyor; toplumlar arasındaki yumuşama tersine dönebilir."),
                ("Su paylaşımını teknik komisyona havale et.", "pragmatik",
                 "📋 **Pragmatik yaklaşım:** Teknik çözüm sağlandı; ancak kimliksel ayrışma hâlâ var."),
            ],
            "marksizm": [
                ("Barajı işleten şirketi millileştir veya iki ülke devletinin ortak kamu idaresine devret; kârı su kullanıcı köylülere aktar.", "teorik",
                 "⚖️ **Marksist hamle:** Devrimsel adım! Şirketin bölgeden çekilmesi sağlandı. Her iki ülkenin çiftçileri tarihte ilk kez ortak yönetim kurulunda yer aldı."),
                ("BM ve bölgesel örgütlerin garantörlüğünde kapsamlı antlaşma imzala.", "zit",
                 "🕊️ **Teoriye aykırı:** Uluslararası kurumlar kapitalist düzenin içinde; şirketin çıkarlarını koruyacak maddeleri antlaşmaya ekledi."),
                ("Su paylaşımını teknik komisyona havale et.", "pragmatik",
                 "📋 **Pragmatik yaklaşım:** Teknik çözüm sınıfsal ilişkileri değiştirmiyor; kısa vadeli rahatlama sağladı."),
            ],
        }
    }
}

# Seçimlere göre sonuç belirleme
SONUCLAR = {
    3: {
        "baslik": "🏆 Mükemmel Teorik Tutarlılık!",
        "renk": "#22543D",
        "arkaplan": "linear-gradient(135deg, #C6F6D5 0%, #9AE6B4 100%)",
        "metin": "Seçtiğin teorik çerçeveyi baştan sona tutarlı biçimde uyguladın. Akademik çevrelerde bu tür analitik tutarlılık, bir teorinin açıklama gücünü test etmenin en sağlam yoludur.",
        "durum": "✅ Müzakere ile kalıcı anlaşma sağlandı. Tarih seni tutarlı bir vizyon insanı olarak hatırlayacak."
    },
    2: {
        "baslik": "⚖️ Dengeli Pragmatist",
        "renk": "#744210",
        "arkaplan": "linear-gradient(135deg, #FEFCBF 0%, #FAF089 100%)",
        "metin": "Teorik tutarlılıkla pratik zorunluluklar arasında denge kurdun. Gerçek dünya siyasetinde bu yaklaşım yaygındır; teorisyenler buna 'eklektisizm' der.",
        "durum": "⚠️ Statüko korundu ama gerginlik sürüyor. Sonuçlar kısmen olumlu."
    },
    1: {
        "baslik": "🌪️ Kriz Yönetimi Zayıf",
        "renk": "#742A2A",
        "arkaplan": "linear-gradient(135deg, #FED7D7 0%, #FC8181 100%)",
        "metin": "Teoriden sapmalar senaryoyu öngörülemeyen yönlere taşıdı. Uİ teorileri, kriz anlarında bile karar vericilere referans noktası sunar.",
        "durum": "🔴 Gerginlik sürdü; çözüm ertelendi. Sonuçlar belirsiz."
    },
    0: {
        "baslik": "💥 Tam Kaos",
        "renk": "#1A202C",
        "arkaplan": "linear-gradient(135deg, #E2E8F0 0%, #CBD5E0 100%)",
        "metin": "Hiçbir teorik çerçeveye uymayan kararlar aldın. Belki de bunu bilinçli yaptın — bu da bir teorik duruş sayılır: 'saf reelpolitik'.",
        "durum": "☠️ Kriz çözümsüz kaldı. Taraflar yorgun ve öfkeli."
    }
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
# SIDEBAR NAVIGASYON
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:36px">🌍</div>
        <div class="sidebar-logo-metin">Uİ Teori Simülatörü</div>
    </div>
    """, unsafe_allow_html=True)

    menu_secenekleri = [
        "🏠 Ana Sayfa",
        "📚 Teori Seçimi",
        "🎮 Simülasyon (Nehir Krizi)",
        "📊 Karşılaştırma Tablosu",
        "ℹ️ Hakkında"
    ]

    secili_sayfa = st.radio(
        "Menü",
        menu_secenekleri,
        index=menu_secenekleri.index(st.session_state["page"]),
        key="sidebar_menu",
        label_visibility="collapsed"
    )
    st.session_state["page"] = secili_sayfa

    # Seçili teori bilgisi sidebar'da göster
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
        <p>Soyut teorileri gerçek bir kriz senaryosunda test et. 
        Realizm, Liberalizm, Konstrüktivizm ve Marksizm'i oyunlaştırılmış bir deneyimle keşfet.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="adim-kutu">
            <div class="adim-ikon">📚</div>
            <div class="adim-baslik">1. Teorini Seç</div>
            <div class="adim-aciklama">Realizm, Liberalizm, Konstrüktivizm veya Marksizm'den birini seç. Her teorinin varsayımlarını, aktörlerini ve güç tanımını öğren.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="adim-kutu">
            <div class="adim-ikon">🎮</div>
            <div class="adim-baslik">2. Simülasyonu Çalıştır</div>
            <div class="adim-aciklama">Nehir Krizi senaryosunda bir devlet adamı olarak 3 kritik kararı ver. Teorine ne kadar sadık kalabileceksin?</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="adim-kutu">
            <div class="adim-ikon">📊</div>
            <div class="adim-baslik">3. Sonuçları Karşılaştır</div>
            <div class="adim-aciklama">Teorilerin radar grafikleri ve çatışma/işbirliği olasılıklarını görselleştir. Hangi teori senin dünya görüşüne yakın?</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🚀 Hemen Başla", use_container_width=True):
            st.session_state["page"] = "📚 Teori Seçimi"
            st.rerun()

    st.markdown("""
    <div class="kart" style="margin-top:32px;">
        <div class="kart-baslik">Bu Uygulama Hakkında</div>
        <p class="kart-metin">
        Bu simülatör, Uluslararası İlişkiler lisans öğrencilerinin teorik çerçeveleri soyut kavramlar olarak değil, 
        somut karar senaryoları aracılığıyla içselleştirmesini hedefler. Her teori farklı bir 
        "gözlük" sunar: aynı krize bakarken farklı şeyler görürsünüz.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TEORİ SEÇİMİ
# ─────────────────────────────────────────────
def show_theory_selection():
    st.markdown('<h1>📚 Teori Seçimi</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4A5568; font-size:16px;">Simülasyona girmeden önce hangi teorik gözlükle analiz yapacağını seç.</p>', unsafe_allow_html=True)

    col_sol, col_sag = st.columns([1, 1.4])

    with col_sol:
        secenekler = {t["isim"]: tid for tid, t in THEORIES.items()}
        gosterim_listesi = [f"{THEORIES[tid]['ikon']}  {THEORIES[tid]['isim']}" for tid in THEORIES]
        id_listesi = list(THEORIES.keys())

        secim_index = 0
        if st.session_state.get("secilen_teori") in id_listesi:
            secim_index = id_listesi.index(st.session_state["secilen_teori"])

        secim = st.selectbox(
            "🔍 Teori seçin:",
            options=range(len(id_listesi)),
            format_func=lambda i: gosterim_listesi[i],
            index=secim_index
        )
        secilen_id = id_listesi[secim]
        teori = THEORIES[secilen_id]

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎮 Bu Teoriyle Simülasyona Başla", use_container_width=True):
            st.session_state["secilen_teori"] = secilen_id
            # Simülasyon state'ini sıfırla
            st.session_state["sim_asama"] = 0
            st.session_state["sim_puan"] = 0
            st.session_state["sim_rol"] = None
            st.session_state["sim_secimler"] = []
            st.session_state["sim_bitti"] = False
            st.session_state["page"] = "🎮 Simülasyon (Nehir Krizi)"
            st.rerun()

    with col_sag:
        st.markdown(f"""
        <div class="teori-kart">
            <h2>{teori['ikon']} {teori['isim']}</h2>
            <hr style="border-color:rgba(255,255,255,0.2); margin:12px 0;">

            <div class="etiket">Temel Varsayım</div>
            <div class="deger">{teori['temel_varsayim']}</div>

            <div class="etiket">Ana Aktörler</div>
            <div class="deger">{teori['ana_aktorler']}</div>

            <div class="etiket">Güç Tanımı</div>
            <div class="deger">{teori['guc_tanimi']}</div>

            <div class="etiket">Dünya Görüşü</div>
            <div class="deger">{teori['dunya_gorusu']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="alinti">{teori['meshur_soz']}</div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SİMÜLASYON
# ─────────────────────────────────────────────
def show_simulation():
    # Teori seçilmemişse uyar
    if not st.session_state.get("secilen_teori"):
        st.warning("⚠️ Simülasyona başlamadan önce lütfen bir teori seçin.")
        if st.button("📚 Teori Seçimine Git"):
            st.session_state["page"] = "📚 Teori Seçimi"
            st.rerun()
        return

    teori_id = st.session_state["secilen_teori"]
    teori = THEORIES[teori_id]

    st.markdown(f'<h1>🎮 Simülasyon — {teori["ikon"]} {teori["isim"]} Perspektifi</h1>', unsafe_allow_html=True)

    # Senaryo kutusu
    st.markdown("""
    <div class="senaryo-kutu">
        <div class="senaryo-baslik">🌊 Nehir Krizi Senaryosu</div>
        <p style="color:#5D4037; font-size:15px; line-height:1.7; margin:0;">
        <strong>Bereket Nehri</strong>, iki komşu ülke arasında uyuşmazlık konusu. Yukarı kıyıdaş 
        <strong>Arkania</strong>, yeni bir hidroelektrik barajı inşa etti. Aşağı kıyıdaş 
        <strong>Beledya</strong>'nın su akışı <strong>%40 azaldı</strong>, tarım sektörü krizde. 
        Gerginlik tırmanıyor. Sen bir karar verici olarak süreci yöneteceksin.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Rol seçimi
    if st.session_state["sim_asama"] == 0:
        st.markdown("### 🎭 Rolünü Seç")
        rol = st.radio(
            "Hangi tarafı temsil edeceksin?",
            ["🏔️ Arkania (Yukarı Kıyıdaş — Barajı İşleten)", "🌾 Beledya (Aşağı Kıyıdaş — Su Krizi Yaşayan)"],
            key="rol_secim"
        )
        if st.button("✅ Rolü Onayla ve Oyuna Başla", use_container_width=False):
            st.session_state["sim_rol"] = rol
            st.session_state["sim_asama"] = 1
            st.rerun()
        return

    # Bitti mi kontrolü
    if st.session_state["sim_bitti"]:
        show_simulation_result()
        return

    asama_no = st.session_state["sim_asama"]
    if asama_no > 3:
        st.session_state["sim_bitti"] = True
        st.rerun()
        return

    # Aşama ilerleme göstergesi
    col_p1, col_p2, col_p3, _ = st.columns([1, 1, 1, 5])
    for i, col in enumerate([col_p1, col_p2, col_p3], 1):
        with col:
            if i < asama_no:
                renk = "#22543D"
                bg = "#C6F6D5"
                ikon = "✓"
            elif i == asama_no:
                renk = "#FFFFFF"
                bg = "#1A3C6E"
                ikon = str(i)
            else:
                renk = "#A0AEC0"
                bg = "#E2E8F0"
                ikon = str(i)
            st.markdown(f"""
            <div style="background:{bg}; color:{renk}; width:36px; height:36px; border-radius:50%;
                        display:flex; align-items:center; justify-content:center; font-weight:700;
                        font-size:14px; margin:0 auto;">{ikon}</div>
            <div style="text-align:center; font-size:11px; color:#718096; margin-top:4px;">Aşama {i}</div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    asama_veri = SIMULATION_DATA[asama_no]
    st.markdown(f"### {asama_veri['baslik']}")
    st.markdown(f"""
    <div class="kart-turuncu">
        <p style="margin:0; font-size:15px; color:#4A5568; line-height:1.7;">{asama_veri['durum']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='color:#2C5282; font-size:14px;'><strong>Rolün:</strong> {st.session_state['sim_rol']}</p>", unsafe_allow_html=True)

    # Seçenekleri göster
    secenekler = asama_veri["secenekler"][teori_id]
    secim_metinleri = [s[0] for s in secenekler]

    secim = st.radio(
        "Eylemini seç:",
        secim_metinleri,
        key=f"secim_asama_{asama_no}"
    )

    secim_index = secim_metinleri.index(secim)

    if st.button(f"➡️ Kararı Uygula", use_container_width=False):
        secilen_tip = secenekler[secim_index][1]
        secilen_geri = secenekler[secim_index][2]

        if secilen_tip == "teorik":
            st.session_state["sim_puan"] += 1

        st.session_state["sim_secimler"].append({
            "asama": asama_no,
            "secim": secim,
            "tip": secilen_tip,
            "geri_bildirim": secilen_geri
        })

        st.session_state["sim_asama"] += 1

        if st.session_state["sim_asama"] > 3:
            st.session_state["sim_bitti"] = True

        st.rerun()

    # Önceki kararların geri bildirimleri
    if st.session_state["sim_secimler"]:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**📜 Önceki Kararların:**")
        for s in st.session_state["sim_secimler"]:
            st.info(s["geri_bildirim"])


def show_simulation_result():
    """Simülasyon sonuç ekranı"""
    puan = st.session_state["sim_puan"]
    teori_id = st.session_state["secilen_teori"]
    teori = THEORIES[teori_id]
    sonuc = SONUCLAR[puan]

    st.markdown(f"""
    <div class="sonuc-hero">
        <div style="font-size:60px; margin-bottom:12px;">{teori['ikon']}</div>
        <h2>{sonuc['baslik']}</h2>
        <p style="color:#B3C6E0; font-size:17px; max-width:600px; margin:0 auto;">{sonuc['durum']}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="puan-kutu">
            <div style="font-size:13px; color:#718096; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">Teori Uyum Puanı</div>
            <div class="puan-sayi">{puan}/3</div>
            <div style="font-size:14px; color:#4A5568; margin-top:8px;">{teori['isim']} perspektifi</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kart">
            <div class="kart-baslik">📝 Teorik Değerlendirme</div>
            <p class="kart-metin">{sonuc['metin']}</p>
            <br>
            <div class="etiket" style="color:#FF6B35; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:1px;">Teorik Beklenti</div>
            <p class="kart-metin" style="margin-top:6px;">{teori['senaryo_davranis']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Karar özeti
    st.markdown("### 📋 Kararlarının Özeti")
    for s in st.session_state["sim_secimler"]:
        tip_renk = {"teorik": "🟢", "zit": "🔴", "pragmatik": "🟡"}
        tip_metin = {"teorik": "Teoriye Uygun", "zit": "Teoriye Aykırı", "pragmatik": "Pragmatik"}
        st.markdown(f"""
        <div class="kart-turuncu" style="border-left-color: {'#22543D' if s['tip']=='teorik' else '#742A2A' if s['tip']=='zit' else '#D69E2E'}">
            <strong>Aşama {s['asama']}</strong> — {tip_renk[s['tip']]} {tip_metin[s['tip']]}<br>
            <span style="color:#4A5568; font-size:14px;">{s['secim']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        if st.button("🔄 Simülasyonu Sıfırla", use_container_width=True):
            st.session_state["sim_asama"] = 0
            st.session_state["sim_puan"] = 0
            st.session_state["sim_rol"] = None
            st.session_state["sim_secimler"] = []
            st.session_state["sim_bitti"] = False
            st.rerun()
    with col_r2:
        if st.button("📚 Farklı Teori Dene", use_container_width=True):
            st.session_state["secilen_teori"] = None
            st.session_state["sim_asama"] = 0
            st.session_state["sim_puan"] = 0
            st.session_state["sim_rol"] = None
            st.session_state["sim_secimler"] = []
            st.session_state["sim_bitti"] = False
            st.session_state["page"] = "📚 Teori Seçimi"
            st.rerun()

# ─────────────────────────────────────────────
# KARŞILAŞTIRMA TABLOSU
# ─────────────────────────────────────────────
def show_comparison():
    st.markdown('<h1>📊 Teoriler Karşılaştırma Tablosu</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4A5568; font-size:16px;">Dört ana teorinin temel özelliklerini ve nicel karşılaştırmasını keşfet.</p>', unsafe_allow_html=True)

    # DataFrame tablosu
    tablo_data = {
        "Teori": ["Realizm 🗡️", "Liberalizm 🕊️", "Konstrüktivizm 🧩", "Marksizm ⚖️"],
        "Ana Aktör": ["Devlet", "Devlet + Kurumlar + STK", "Toplumlar + Bireyler", "Sınıflar + Şirketler"],
        "Sistem Yapısı": ["Anarşi (değişmez)", "Anarşi (yumuşatılabilir)", "Sosyal inşa", "Kapitalist hiyerarşi"],
        "Çatışma Sebebi": ["Güç açığı / Güvenlik ikilemi", "Kurumsal eksiklik", "Kimlik uyuşmazlığı", "Sınıf ve sömürü"],
        "Barış Yolu": ["Güç dengesi", "Kurumlar + Ticaret", "Kimlik dönüşümü", "Sınıf mücadelesi"],
        "Analiz Düzeyi": ["Devlet / Sistem", "Devlet / Uluslararası", "Birey / Toplum", "Ekonomik yapı"]
    }
    df = pd.DataFrame(tablo_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=200
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🕸️ Radar Grafiği — Teorik Odak Alanları")
        kategoriler = ["Askeri Odak", "Ekonomik Odak", "İşbirliği İmkanı", "Birey Etkisi"]
        renkler = ["#1A3C6E", "#2ECC71", "#FF6B35", "#E74C3C"]

        fig_radar = go.Figure()
        for tid, renk in zip(THEORIES.values(), renkler):
            degerler = [tid["radar"][k] for k in kategoriler]
            degerler_kapali = degerler + [degerler[0]]
            kategoriler_kapali = kategoriler + [kategoriler[0]]

            fig_radar.add_trace(go.Scatterpolar(
                r=degerler_kapali,
                theta=kategoriler_kapali,
                fill='toself',
                name=f"{tid['ikon']} {tid['isim']}",
                line=dict(color=renk, width=2),
                fillcolor=renk,
                opacity=0.2
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=12))
            ),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Source Sans 3'),
            height=420,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Çatışma / İşbirliği Olasılığı")
        teori_isimleri = [f"{t['ikon']} {t['isim']}" for t in THEORIES.values()]
        catisma_degerler = [t["olasilik"]["Çatışma"] for t in THEORIES.values()]
        isbirligi_degerler = [t["olasilik"]["İşbirliği"] for t in THEORIES.values()]

        fig_bar = go.Figure(data=[
            go.Bar(
                name='Çatışma Olasılığı (%)',
                x=teori_isimleri,
                y=catisma_degerler,
                marker_color='#E74C3C',
                marker_line_color='#C0392B',
                marker_line_width=1
            ),
            go.Bar(
                name='İşbirliği Olasılığı (%)',
                x=teori_isimleri,
                y=isbirligi_degerler,
                marker_color='#2ECC71',
                marker_line_color='#27AE60',
                marker_line_width=1
            )
        ])

        fig_bar.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(248,250,252,1)',
            font=dict(family='Source Sans 3'),
            height=420,
            yaxis=dict(title="Olasılık (%)", range=[0, 100], gridcolor='#E2E8F0'),
            xaxis=dict(tickfont=dict(size=11)),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Teori detay expander
    st.markdown("#### 🔍 Teori Detayları")
    secili_detay = st.selectbox(
        "Detayını görmek istediğin teoriyi seç:",
        options=list(THEORIES.keys()),
        format_func=lambda tid: f"{THEORIES[tid]['ikon']}  {THEORIES[tid]['isim']}"
    )
    teori_d = THEORIES[secili_detay]
    with st.expander(f"📖 {teori_d['isim']} — Detaylı Açıklama", expanded=True):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"**Temel Varsayım:** {teori_d['temel_varsayim']}")
            st.markdown(f"**Ana Aktörler:** {teori_d['ana_aktorler']}")
            st.markdown(f"**Güç Tanımı:** {teori_d['guc_tanimi']}")
        with col_d2:
            st.markdown(f"**Dünya Görüşü:** {teori_d['dunya_gorusu']}")
            st.markdown(f"**Kriz Davranışı:** {teori_d['senaryo_davranis']}")
        st.markdown(f"""
        <div class="alinti">{teori_d['meshur_soz']}</div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HAKKINDA
# ─────────────────────────────────────────────
def show_about():
    st.markdown('<h1>ℹ️ Hakkında</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="kart">
            <div class="kart-baslik">🎓 Uygulama Hakkında</div>
            <p class="kart-metin">
            Bu uygulama, <strong>Uluslararası İlişkiler</strong> bölümü lisans ve yüksek lisans öğrencilerine 
            yönelik eğitim amaçlı bir interaktif simülatördür. Amacı; Realizm, Liberalizm, Konstrüktivizm 
            ve Marksizm gibi temel teorik paradigmaları, öğrencilerin aktif karar alma süreçleriyle deneyimlemesini sağlamaktır.
            </p>
            <br>
            <div class="kart-baslik">👥 Hedef Kitle</div>
            <p class="kart-metin">
            Uluslararası İlişkiler, Siyaset Bilimi, Kamu Yönetimi ve Sosyal Bilimler bölümleri öğrencileri; 
            ayrıca teorik çerçeveleri pratik senaryolarda test etmek isteyen araştırmacılar.
            </p>
            <br>
            <div class="kart-baslik">⚠️ Sorumluluk Reddi</div>
            <p class="kart-metin">
            Senaryolar, karakter isimleri (Arkania, Beledya) ve olaylar tamamen kurgusaldır. 
            Herhangi bir ülkeye, etnik gruba veya siyasi tutuma referans vermez. 
            Teorik yorumlar akademik literatürü basitleştirmiş olabilir.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="kart-turuncu">
            <div class="kart-baslik">🛠️ Teknik Bilgi</div>
            <p class="kart-metin">
            <strong>Dil:</strong> Python 3<br><br>
            <strong>Kütüphaneler:</strong><br>
            • Streamlit<br>
            • Pandas<br>
            • Plotly<br><br>
            <strong>Mimari:</strong> Tek dosya (app.py)<br><br>
            <strong>Deployment:</strong> Streamlit Cloud uyumlu
            </p>
        </div>

        <div class="kart" style="margin-top:16px;">
            <div class="kart-baslik">📚 Kaynaklar</div>
            <p class="kart-metin">
            • Waltz, K. (1979). <em>Theory of International Politics</em><br>
            • Keohane, R. (1984). <em>After Hegemony</em><br>
            • Wendt, A. (1999). <em>Social Theory of IR</em><br>
            • Frank, A.G. (1967). <em>Capitalism and Underdevelopment</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding:32px 0 16px 0; color:#A0AEC0; font-size:14px;">
        © 2024 Uİ Teori Simülatörü &nbsp;|&nbsp; Eğitim Amaçlıdır &nbsp;|&nbsp; Açık Kaynak
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ANA ÇALIŞMA BLOĞU — Sayfa yönlendirme
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
