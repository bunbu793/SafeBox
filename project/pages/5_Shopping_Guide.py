import streamlit as st
import requests
import urllib.parse
import pandas as pd
import math
import json
from supabase import create_client

# =========================
# 距離計算
# =========================
def calc_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat/2)**2 
        + math.cos(math.radians(lat1)) 
        * math.cos(math.radians(lat2)) 
        * math.sin(dlon/2)**2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# =========================
# APIキー
# =========================
API_KEY = st.secrets["GEOAPIFY_KEY"]

# =========================
# Supabase
# =========================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# =========================
# 市区町村データ
# =========================
df = pd.read_csv(
    "https://raw.githubusercontent.com/bunbu793/SafeBox/main/japan_city_code.csv",
    encoding="utf-8"
)

df.columns = df.columns.str.normalize("NFKC").str.replace("\n", "").str.strip()
df = df.sort_values(by=["団体コード"], ascending=True).fillna("")

pref_list = df["都道府県名(漢字)"].drop_duplicates().tolist()

city_map = {
    pref: [c for c in df[df["都道府県名(漢字)"] == pref]["市区町村名(漢字)"].unique().tolist() if c]
    for pref in pref_list
}

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
        f"&details=store"
        f"&apiKey={API_KEY}"
    )
    res = requests.get(url).json()
    return res.get("features", [])

# =========================
# UI
# =========================
st.title("SafeBox Manager - Shopping Guide")

if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

family_code = st.session_state["family_code"]
st.success(f"ログイン中：{family_code}")

# =========================
# チェックリスト連動
# =========================
response = supabase.table("checklist").select("*").eq("family_code", family_code).execute()

if response.data:
    saved_checks = json.loads(response.data[0]["data"])
else:
    saved_checks = {}

not_completed = [name for name, done in saved_checks.items() if not done]

recommend_map = {
    "飲料水（1人1日3L × 3日分）": "スーパー",
    "非常食（1人3日分）": "スーパー",
    "携帯トイレ（1人3〜5回分 × 3日）": "コンビニ",
    "モバイルバッテリー": "ホームセンター",
    "懐中電灯": "ホームセンター",
    "乾電池": "コンビニ",
    "救急セット": "ドラッグストア",
    "常備薬": "ドラッグストア",
    "防寒具": "ショッピングモール",
}

st.subheader("不足している備品に応じたおすすめ店舗")

for item in not_completed:
    store_type = recommend_map.get(item)
    if store_type:
        st.write(f"- **{item}** → おすすめ: **{store_type}**")

# =========================
# 住所入力
# =========================
pref = st.selectbox("都道府県", pref_list)
city_list = city_map.get(pref, [])
city = st.selectbox("市区町村", city_list)

place = st.text_input("場所名（例：お台場、渋谷、新宿）")

parts = [pref, city, place]
search_text = " ".join([p for p in parts if p])

category_map = {
    "スーパー": "commercial.supermarket",
    "コンビニ": "commercial.convenience",
    "ドラッグストア": "commercial.pharmacy",
    "ホームセンター": "commercial.hardware",
    "ショッピングモール": "commercial.shopping_mall",
}

category_name = st.selectbox("探したい店の種類", list(category_map.keys()))
search = st.button("検索🔍")

# =========================
# 検索処理
# =========================
if search:
    with st.spinner("検索中…"):
        result = geocode(search_text)

        if not result:
            st.error("住所が見つかりませんでした。")
            st.stop()

        lat, lng = result

        stores = search_places(category_map[category_name], lat, lng)

    st.subheader(f"🔍 {search_text} の近くの {category_name}")

    if not stores:
        st.info("該当する店舗が見つかりませんでした。")
        st.stop()

    unique = {}
    for s in stores:
        props = s["properties"]
        name = props.get("name")

        if not name:
            continue

        slat = props.get("lat")
        slng = props.get("lon")

        if not slat or not slng:
            continue

        dist = calc_distance(lat, lng, slat, slng)

        if dist > 2:
            continue

        props["distance"] = dist
        unique[name] = props

    unique = dict(sorted(unique.items(), key=lambda item: item[1]["distance"]))

    markers = ""
    for props in unique.values():
        markers += f"&marker=lonlat:{props['lon']},{props['lat']};color:blue;size:small"

    center_marker = f"&marker=lonlat:{lng},{lat};color:red;size:medium"

    map_url = (
        f"https://maps.geoapify.com/v1/staticmap?"
        f"style=osm-carto"
        f"&center=lonlat:{lng},{lat}"
        f"&zoom=14"
        f"&size=600x400"
        f"{center_marker}"
        f"{markers}"
        f"&apiKey={API_KEY}"
    )

    st.image(map_url)

    for name, props in unique.items():
        st.write(f"### {name}")

        # 住所（翻訳なし）
        address = props.get("formatted", "")
        st.write(f"📍 {address}")

        dist_text = f"{props['distance']:.2f} km"
        st.write(f"🚶 距離: {dist_text}")

        brand = props.get("brand")
        opening = props.get("opening_hours")
        if opening == "24/7":
            opening = "24時間営業"

        categories = props.get("categories", [])

        if brand:
            st.write(f"🏪 ブランド: {brand}")

        if opening:
            st.write(f"⏰ 営業時間: {opening}")

        if categories:
            st.write(f"📦 カテゴリ: {', '.join(categories)}")
