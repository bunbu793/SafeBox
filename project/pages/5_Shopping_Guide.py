import streamlit as st
import requests
import urllib.parse
import pandas as pd

API_KEY = st.secrets["GEOAPIFY_KEY"]

df = pd.read_csv(
    "https://raw.githubusercontent.com/bunbu793/SafeBox/main/japan_city_code.csv",
    encoding="utf-8"
)

# 列名を正規化（全角→半角、改行・空白除去）
df.columns = df.columns.str.normalize("NFKC").str.replace("\n", "").str.strip()

# 🔹 団体コード順（都道府県順）＋市区町村順に並び替え
df = df.sort_values(
    by=["団体コード"],
    ascending=True
)

df = df.fillna("")

# 🔹 都道府県リスト（団体コード順）
pref_list = df["都道府県名(漢字)"].drop_duplicates().tolist()

# 🔹 市区町村リスト
city_map = {
    pref: [c for c in df[df["都道府県名(漢字)"] == pref]["市区町村名(漢字)"].unique().tolist() if c]
    for pref in pref_list
}

#区リスト
seirei = {
    "札幌市","仙台市","さいたま市","千葉市","横浜市","川崎市","相模原市",
    "新潟市","静岡市","浜松市","名古屋市","京都市","大阪市","堺市",
    "神戸市","岡山市","広島市","北九州市","福岡市","熊本市"
}

ward_map = {
    "札幌市": ["中央区", "北区", "東区", "白石区", "豊平区", "南区", "西区", "厚別区", "手稲区", "清田区"],
    "仙台市": ["青葉区", "宮城野区", "若林区", "太白区", "泉区"],
    "さいたま市": ["西区", "北区", "大宮区", "見沼区", "中央区", "桜区", "浦和区", "南区", "緑区", "岩槻区"],
    "千葉市": ["中央区", "花見川区", "稲毛区", "若葉区", "緑区", "美浜区"],
    "横浜市": ["鶴見区", "神奈川区", "西区", "中区", "南区", "保土ケ谷区", "磯子区", "金沢区", "港北区", "戸塚区", "港南区", "旭区", "緑区", "瀬谷区", "栄区", "泉区", "青葉区", "都筑区"],
    "川崎市": ["川崎区", "幸区", "中原区", "高津区", "多摩区", "宮前区", "麻生区"],
    "相模原市": ["緑区", "中央区", "南区"],
    "新潟市": ["北区", "東区", "中央区", "江南区", "秋葉区", "南区", "西区", "西蒲区"],
    "静岡市": ["葵区", "駿河区", "清水区"],
    "浜松市": ["中央区", "浜名区", "天竜区"],
    "名古屋市": ["千種区", "東区", "北区", "西区", "中村区", "中区", "昭和区", "瑞穂区", "熱田区", "中川区", "港区", "南区", "守山区", "緑区", "名東区", "天白区"],
    "京都市": ["北区", "上京区", "左京区", "中京区", "東山区", "下京区", "南区", "右京区", "伏見区", "山科区", "西京区"],
    "大阪市": ["都島区", "福島区", "此花区", "中央区", "西区", "港区", "大正区", "天王寺区", "浪速区", "西淀川区", "東淀川区", "東成区", "生野区", "旭区", "城東区", "阿倍野区", "住吉区", "東住吉区", "西成区", "淀川区", "鶴見区", "住之江区", "平野区", "北区"],
    "堺市": ["堺区", "中区", "東区", "西区", "南区", "北区", "美原区"],
    "神戸市": ["東灘区", "灘区", "中央区", "兵庫区", "北区", "長田区", "須磨区", "垂水区", "西区"],
    "岡山市": ["北区", "中区", "東区", "南区"],
    "広島市": ["中区", "東区", "南区", "西区", "安佐南区", "安佐北区", "安芸区", "佐伯区"],
    "北九州市": ["門司区", "若松区", "戸畑区", "小倉北区", "小倉南区", "八幡東区", "八幡西区"],
    "福岡市": ["東区", "博多区", "中央区", "南区", "西区", "城南区", "早良区"],
    "熊本市": ["中央区", "東区", "西区", "南区", "北区"]
}

# 東京23区
TOKYO_23 = [
    "千代田区","中央区","港区","新宿区","文京区","台東区","墨田区","江東区",
    "品川区","目黒区","大田区","世田谷区","渋谷区","中野区","杉並区","豊島区",
    "北区","荒川区","板橋区","練馬区","足立区","葛飾区","江戸川区"
]

# =========================
# 日本語住所辞書
# =========================

STRUCT_MAP_ORDERED = [
    ("Dori Avenue", "通"),
    ("Dori", "通"),
    ("Avenue", "通"),
    ("Street", "通り"),
    ("Route", "国道"),
    ("Line", "線"),

    ("1-chome", "1丁目"),
    ("2-chome", "2丁目"),
    ("3-chome", "3丁目"),
    ("4-chome", "4丁目"),
    ("5-chome", "5丁目"),
    ("Route", "号線"),
    ("National Highway", "国道"),
    ("Expressway", "高速"),
    ("Shuto Expressway", "首都高速"),
]

PREF_MAP = {
    "Hokkaido": "北海道",
    "Aomori": "青森県",
    "Iwate": "岩手県",
    "Miyagi": "宮城県",
    "Akita": "秋田県",
    "Yamagata": "山形県",
    "Fukushima": "福島県",
    "Ibaraki": "茨城県",
    "Tochigi": "栃木県",
    "Gunma": "群馬県",
    "Saitama": "埼玉県",
    "Chiba": "千葉県",
    "Tokyo": "東京都",
    "Kanagawa": "神奈川県",
    "Niigata": "新潟県",
    "Toyama": "富山県",
    "Ishikawa": "石川県",
    "Fukui": "福井県",
    "Yamanashi": "山梨県",
    "Nagano": "長野県",
    "Gifu": "岐阜県",
    "Shizuoka": "静岡県",
    "Aichi": "愛知県",
    "Mie": "三重県",
    "Shiga": "滋賀県",
    "Kyoto": "京都府",
    "Osaka": "大阪府",
    "Hyogo": "兵庫県",
    "Nara": "奈良県",
    "Wakayama": "和歌山県",
    "Tottori": "鳥取県",
    "Shimane": "島根県",
    "Okayama": "岡山県",
    "Hiroshima": "広島県",
    "Yamaguchi": "山口県",
    "Tokushima": "徳島県",
    "Kagawa": "香川県",
    "Ehime": "愛媛県",
    "Kochi": "高知県",
    "Fukuoka": "福岡県",
    "Saga": "佐賀県",
    "Nagasaki": "長崎県",
    "Kumamoto": "熊本県",
    "Oita": "大分県",
    "Miyazaki": "宮崎県",
    "Kagoshima": "鹿児島県",
    "Okinawa": "沖縄県",
}

CITY_MAP = {
    "Nagoya": "名古屋市",
    "Toyota": "豊田市",
    "Okazaki": "岡崎市",
    "Hachioji": "八王子市",
    "Osaka": "大阪市",
}

WARD_MAP = {
    "Nakamura ward": "中村区",
    "Naka ward": "中区",
    "Higashi ward": "東区",
    "Kita ward": "北区",
    "Nishi ward": "西区",
}

NAME_MAP = {
    "Takabata": "高畑",
    "Nagoya Station": "名古屋駅",
    "Kanayama": "金山",
    "Sakae": "栄",
    "Fushimi": "伏見",
    "Ozone": "大曽根",
    "Hachioji": "八王子",
}

# PREF_MAP の下に追加
for jp in df["市区町村名(漢字)"].unique():
    eng = jp.replace("市", "").replace("区", "")
    CITY_MAP[eng] = jp

for city, wards in ward_map.items():
    for w in wards:
        eng = w.replace("区", "")
        WARD_MAP[eng] = w

def to_japanese_address(address: str) -> str:
    for eng, jp in STRUCT_MAP_ORDERED:
        address = address.replace(eng, jp)
    for eng, jp in PREF_MAP.items():
        address = address.replace(eng, jp)
    for eng, jp in CITY_MAP.items():
        address = address.replace(eng, jp)
    for eng, jp in WARD_MAP.items():
        address = address.replace(eng, jp)
    for eng, jp in NAME_MAP.items():
        address = address.replace(eng, jp)
    return address

# =========================
# Geoapify API
# =========================

def geocode(address):
    encoded = urllib.parse.quote(address)
    url = f"https://api.geoapify.com/v1/geocode/search?text={encoded}&apiKey={API_KEY}"
    res = requests.get(url).json()
    features = res.get("features", [])
    if not features:
        return None
    props = features[0]["properties"]
    return props["lat"], props["lon"]

def search_places(category, lat, lng):
    url = (
        "https://api.geoapify.com/v2/places"
        f"?categories={category}"
        f"&filter=circle:{lng},{lat},3000"
        f"&limit=10"
        f"&apiKey={API_KEY}"
    )
    res = requests.get(url).json()
    return res.get("features", [])

# =========================
# UI
# =========================

st.title("🗺️ お店を探す")

pref = st.selectbox("都道府県", pref_list)

# =========================
# 東京都だけ特別処理
# =========================
if pref == "東京都":
    tokyo_cities = [c for c in city_map[pref] if c not in TOKYO_23]

    city_list = ["特別区"] +  tokyo_cities
    city = st.selectbox("市（特別区・多摩地域）", city_list)

    if city == "特別区":
        ward_list = TOKYO_23
    else:
        ward_list = []
    
    ward = st.selectbox("区（ない場合は空欄）", ward_list)
    # 通常の都道府県
    # =========================
else:
    city_list = city_map.get(pref, [])
    city = st.selectbox("市（東京都は市がある）", city_list)

    if city in ward_map:
        ward_list = ward_map[city]
    else:
        ward_list = []

    ward = st.selectbox("区（ない場合は空欄）", ward_list)

place = st.text_input("場所名（例：東京駅、皇居）")

# 空の項目は除外
parts = [pref, city, ward, place]
search_text = " ".join([p for p in parts if p])

category_map = {
    "スーパー": "commercial.supermarket",
    "コンビニ": "commercial.convenience",
    "カフェ": "catering.cafe",
    "ファミレス": "catering.restaurant",
    "ファストフード": "catering.fast_food",
    "ショッピングモール": "commercial.shopping_mall",
}

category_name = st.selectbox("探したい店の種類", list(category_map.keys()))

if place:
    result = geocode(search_text)

    if not result:
        st.error("住所が見つからなかったよ…")
        st.stop()

    lat, lng = result
    st.write(f"📍 緯度: {lat}, 経度: {lng}")

    stores = search_places(category_map[category_name], lat, lng)

    st.subheader(f"🔍 {search_text} の近くの {category_name}")

    if not stores:
        st.error("見つからなかったよ…")
    else:
        unique = {}
        for s in stores:
            props = s["properties"]
            name = props.get("name", "名称不明")
            if name in unique:
                continue
            unique[name] = props

        for name, props in unique.items():
            city = props.get("city", "")
            suburb = props.get("suburb", "")
            district = props.get("district", "")
            street = props.get("street", "")

            raw_address = " ".join([p for p in [city, suburb, district, street] if p])
            address = to_japanese_address(raw_address)

            st.write(f"### {name}")
            st.write(f"📍{address}")