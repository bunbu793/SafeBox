import streamlit as st
import requests
import urllib.parse
import pandas as pd
import math
import json
from supabase import create_client

#=========================
#翻訳　(英語⇒日本語)
#=========================
CATEGORY_JP = {
    "commercial.supermarket": "スーパー",
    "commercial.convenience": "コンビニ",
    "commercial.pharmacy": "ドラッグストア",
    "commercial.hardware": "ホームセンター",
    "commercial.shopping_mall": "ショッピングモール",
    "commercial": "商業施設",
    "building.commercial": "商業ビル",
    "building": "建物"
}

# =========================
# 全国対応：英語 → 日本語住所変換
# =========================

# 都道府県（47個だけで全国対応）
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

# 丁目（全国共通）
CHOME_MAP = {
    "1-chome": "1丁目",
    "2-chome": "2丁目",
    "3-chome": "3丁目",
    "4-chome": "4丁目",
    "5-chome": "5丁目",
}

# 通り（全国共通）
STREET_MAP = {
    "Dori Avenue": "通",
    "Dori": "通",
    "Avenue": "通",
    "Street": "通り",
    "Route": "号線",
}

# 政令指定都市の Ward（全国対応）
WARD_MAP = {
    "Chikusa Ward": "千種区",
    "Naka Ward": "中区",
    "Higashi Ward": "東区",
    "Kita Ward": "北区",
    "Nishi Ward": "西区",
    "Meito Ward": "名東区",
    "Showa Ward": "昭和区",
    "Mizuho Ward": "瑞穂区",
    "Atsuta Ward": "熱田区",
    "Nakagawa Ward": "中川区",
    "Minami Ward": "南区",
    "Midori Ward": "緑区",
    "Moriyama Ward": "守山区",
    "Tempaku Ward": "天白区",
    # 他都市も追加可能
}

# 市区町村（CSVから自動生成）
CITY_MAP = {}
for jp in df["市区町村名(漢字)"].unique():
    eng = jp.replace("市", "").replace("区", "")
    CITY_MAP[eng] = jp

# =========================
# 住所変換関数（全国対応）
# =========================
def to_japanese_address(address: str) -> str:

    # 都道府県
    for eng, jp in PREF_MAP.items():
        address = address.replace(eng, jp)

    # 市区町村（CSVで全国対応）
    for eng, jp in CITY_MAP.items():
        address = address.replace(eng, jp)

    # 区
    for eng, jp in WARD_MAP.items():
        address = address.replace(eng, jp)

    # 丁目
    for eng, jp in CHOME_MAP.items():
        address = address.replace(eng, jp)

    # 通り
    for eng, jp in STREET_MAP.items():
        address = address.replace(eng, jp)

    return address

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

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

family_code = st.session_state["family_code"]
st.success(f"ログイン中：{family_code}")

# =========================
# チェックリスト連動（不足品取得）
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
    "モバイルバッテリー": "家電量販店",
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

place = st.text_input("場所名（例：名古屋駅、栄）")

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

        # 名称不明は除外
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

    # 距離順
    unique = dict(sorted(unique.items(), key=lambda item: item[1]["distance"]))

    # 地図ピン
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

    # 店舗リスト
    for name, props in unique.items():
        st.write(f"### {name}")

        address = props.get("formatted", "")
        st.write(f"📍 {address}")

        dist_text = f"{props['distance']:.2f} km"
        st.write(f"🚶 距離: {dist_text}")

        # 在庫情報
        brand = props.get("brand")
        opening = props.get("opening_hours")
        if opening == "24/7":
            opening = "24時間営業"  
        categories = props.get("categories", [])
        jp_categories = []

        for c in categories:
            jp_categories.append(CATEGORY_JP.get(c, c))  # 辞書にない場合はそのまま

        if brand:
            st.write(f"🏪 ブランド: {brand}")

        if opening:
            st.write(f"⏰ 営業時間: {opening}")

        if jp_categories:
            st.write(f"📦 カテゴリ: {', '.join(jp_categories)}")