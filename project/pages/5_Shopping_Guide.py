import streamlit as st
import requests
import urllib.parse
import pandas as pd
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/bunbu793/SafeBox/main/japan_city_code.csv",
    encoding="utf-8"
)

# 列名を正規化（全角・半角・改行・空白を除去）
df.columns = df.columns.str.normalize("NFKC").str.strip()

# 正しい列名を確認
st.write(df.columns)

# 並び替え
df = df.sort_values(by=["都道府県名", "市区町村名(漢字)"], ascending=True)

df.columns = df.columns.str.normalize("NFKC").str.strip()
df = df.fillna("")


API_KEY = st.secrets["GEOAPIFY_KEY"]

#県
pref_list = sorted(df["都道府県名\n(漢字)"].unique())

#市区町村
city_map = {
    pref: sorted(df[df["都道府県名\n(漢字)"] == pref]["市区町村名\n(漢字)"].unique())
    for pref in pref_list
}

#区リスト
seirei = {
    "札幌市","仙台市","さいたま市","千葉市","横浜市","川崎市","相模原市",
    "新潟市","静岡市","浜松市","名古屋市","京都市","大阪市","堺市",
    "神戸市","岡山市","広島市","北九州市","福岡市","熊本市"
}

ward_map = {city: [] for city in seirei}

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
]

PREF_MAP = {
    "Tokyo": "東京都",
    "Aichi": "愛知県",
    "Osaka": "大阪府",
    "Gifu": "岐阜県",
    "Mie": "三重県",
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

city_list = city_map.get(pref, [])
city = st.selectbox("市（東京都は市がある）", city_list)

# 市がある場合は ward_map[市]、ない場合は ward_map[都道府県]
if city:
    ward_list = ward_map.get(city, [])
else:
    ward_list = ward_map.get(pref, [])

ward = st.selectbox("区（ない場合は空欄）", ward_list)

place = st.text_input("場所名（例：イオン、セブンイレブン）")

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