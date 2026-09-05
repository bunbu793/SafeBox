import streamlit as st
import requests
import urllib.parse
import pandas as pd
import math
import json
from supabase import create_client

from kobito_helper import KOBITO_IMAGES, inject_kobito_css, show_kobito_popup

# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="SafeBox Manager - Shopping Guide",
    page_icon="🛒",
    layout="centered"
)

inject_kobito_css()

# =========================================================
# APIキー
# =========================================================

API_KEY = st.secrets["GEOAPIFY_KEY"]

# =========================================================
# Supabase
# =========================================================

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

# =========================================================
# 距離計算
# =========================================================

def calc_distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# =========================================================
# Geoapify Geocoding
# =========================================================

def geocode(address):

    encoded = urllib.parse.quote(address)

    url = (
        "https://api.geoapify.com/v1/geocode/search"
        f"?text={encoded}"
        f"&apiKey={API_KEY}"
    )

    try:
        res = requests.get(
            url,
            timeout=10
        )

        res.raise_for_status()

        data = res.json()

    except requests.RequestException:
        return None

    features = data.get("features", [])

    if not features:
        return None

    props = features[0].get("properties", {})

    lat = props.get("lat")
    lon = props.get("lon")

    if lat is None or lon is None:
        return None

    return lat, lon


# =========================================================
# 店舗検索
# =========================================================

def search_places(category, lat, lng):

    url = (
        "https://api.geoapify.com/v2/places"
        f"?categories={category}"
        f"&filter=circle:{lng},{lat},3000"
        f"&limit=20"
        f"&details=store"
        f"&apiKey={API_KEY}"
    )

    try:
        res = requests.get(
            url,
            timeout=10
        )

        res.raise_for_status()

        data = res.json()

    except requests.RequestException:
        return []

    return data.get("features", [])


# =========================================================
# 市区町村データ
# =========================================================

@st.cache_data
def load_city_data():

    df = pd.read_csv(
        "https://raw.githubusercontent.com/bunbu793/SafeBox/main/japan_city_code.csv",
        encoding="utf-8"
    )

    df.columns = (
        df.columns
        .str.normalize("NFKC")
        .str.replace("\n", "")
        .str.strip()
    )

    df = (
        df
        .sort_values(
            by=["団体コード"],
            ascending=True
        )
        .fillna("")
    )

    return df


try:

    df = load_city_data()

except Exception as e:

    st.error(
        "市区町村データの読み込みに失敗しました。"
    )

    st.stop()


pref_list = (
    df["都道府県名(漢字)"]
    .drop_duplicates()
    .tolist()
)

city_map = {
    pref: [
        c
        for c in df[
            df["都道府県名(漢字)"] == pref
        ]["市区町村名(漢字)"]
        .unique()
        .tolist()
        if c
    ]
    for pref in pref_list
}

# =========================================================
# UI
# =========================================================

st.title("🛒 防災用品ショッピングガイド")

st.caption(
    "不足している防災用品を確認し、近くのお店を探せます。"
)

# =========================================================
# ログインチェック
# =========================================================

if "family_code" not in st.session_state:

    st.warning(
        "初めにログインしてください。"
    )

    st.stop()

family_code = st.session_state["family_code"]

st.success(
    f"ログイン中：{family_code}"
)

show_kobito_popup(
    KOBITO_IMAGES["shopping"],
    "足りないものは近くのお店で探そう！",
    "kobito_shopping_shown"
)

# =========================================================
# チェックリスト連動
# =========================================================

st.divider()

st.subheader("⚠️ 不足している防災用品")

try:

    response = (
        supabase
        .table("checklist")
        .select("*")
        .eq("family_code", family_code)
        .execute()
    )

    if response.data:

        try:
            saved_checks = json.loads(
                response.data[0]["data"]
            )
        except Exception:
            saved_checks = {}

    else:

        saved_checks = {}

except Exception:

    saved_checks = {}


not_completed = [
    name
    for name, done in saved_checks.items()
    if not done
]

# =========================================================
# おすすめ店舗
# =========================================================

recommend_map = {
    "飲料水（1人1日3L × 3日分）": "スーパー",
    "飲料水": "スーパー",

    "非常食（1人3日分）": "スーパー",
    "非常食": "スーパー",

    "携帯トイレ（1人3〜5回分 × 3日）": "コンビニ",
    "携帯トイレ": "コンビニ",

    "モバイルバッテリー": "ホームセンター",
    "懐中電灯": "ホームセンター",
    "乾電池": "コンビニ",

    "救急セット": "ドラッグストア",
    "常備薬": "ドラッグストア",

    "防寒具": "ショッピングモール",
}


if not_completed:

    for item in not_completed:

        store_type = recommend_map.get(item)

        if store_type:

            with st.container(border=True):

                st.markdown(
                    f"### {item}"
                )

                st.write(
                    f"おすすめ店舗：**{store_type}**"
                )

else:

    st.success(
        "現在、不足している備品はありません！"
    )


# =========================================================
# 店舗検索
# =========================================================

st.divider()

st.subheader("🔎 店舗を探す")

st.caption(
    "探したい地域とお店の種類を入力してください。"
)

# =========================================================
# 地域
# =========================================================

st.markdown("#### 📍 場所")

col1, col2 = st.columns(2)

with col1:

    pref = st.selectbox(
        "都道府県",
        pref_list
    )

with col2:

    city_list = city_map.get(
        pref,
        []
    )

    city = st.selectbox(
        "市区町村",
        city_list
    )

place = st.text_input(
    "場所名",
    placeholder="例：渋谷、新宿、お台場"
)

# =========================================================
# 店舗種類
# =========================================================

category_map = {
    "スーパー": "commercial.supermarket",
    "コンビニ": "commercial.convenience",
    "ドラッグストア": "commercial.pharmacy",
    "ホームセンター": "commercial.hardware",
    "ショッピングモール": "commercial.shopping_mall",
}

category_name = st.selectbox(
    "🏪 探したい店の種類",
    list(category_map.keys())
)

# =========================================================
# 検索ボタン
# =========================================================

search = st.button(
    "🔍 店舗を検索",
    use_container_width=True
)

# =========================================================
# 検索処理
# =========================================================

if search:

    parts = [
        pref,
        city,
        place.strip()
    ]

    search_text = " ".join(
        [p for p in parts if p]
    )

    with st.spinner(
        "近くの店舗を検索しています..."
    ):

        result = geocode(
            search_text
        )

        if not result:

            st.error(
                "指定した場所が見つかりませんでした。"
            )

            st.stop()

        lat, lng = result

        stores = search_places(
            category_map[category_name],
            lat,
            lng
        )

    # =====================================================
    # 店舗整理
    # =====================================================

    unique = {}

    for store in stores:

        props = store.get(
            "properties",
            {}
        )

        name = props.get("name")

        if not name:
            continue

        slat = props.get("lat")
        slng = props.get("lon")

        if slat is None or slng is None:
            continue

        distance = calc_distance(
            lat,
            lng,
            slat,
            slng
        )

        # 2km以内
        if distance > 2:
            continue

        props["distance"] = distance

        # 同じ店舗名の重複を除外
        unique[name] = props

    unique = dict(
        sorted(
            unique.items(),
            key=lambda item: item[1]["distance"]
        )
    )

    # =====================================================
    # 検索結果
    # =====================================================

    st.divider()

    st.subheader(
        f"🔍 {search_text} の近くの{category_name}"
    )

    if not unique:

        st.info(
            "2km以内に該当する店舗が見つかりませんでした。"
        )

        st.stop()

    # =====================================================
    # 件数
    # =====================================================

    st.info(
        f"見つかった店舗：**{len(unique)} 件**"
    )

    # =====================================================
    # 地図
    # =====================================================

    st.markdown("### 🗺️ 地図")

    markers = ""

    for props in unique.values():

        markers += (
            "&marker="
            f"lonlat:{props['lon']},{props['lat']}"
            ";color:blue"
            ";size:small"
        )

    center_marker = (
        "&marker="
        f"lonlat:{lng},{lat}"
        ";color:red"
        ";size:medium"
    )

    map_url = (
        "https://maps.geoapify.com/v1/staticmap?"
        "style=osm-carto"
        f"&center=lonlat:{lng},{lat}"
        "&zoom=14"
        "&size=700x450"
        f"{center_marker}"
        f"{markers}"
        f"&apiKey={API_KEY}"
    )

    st.image(
        map_url,
        use_container_width=True
    )

    # =====================================================
    # 店舗一覧
    # =====================================================

    st.markdown("### 🏪 店舗一覧")

    for index, (name, props) in enumerate(
        unique.items(),
        start=1
    ):

        with st.container(
            border=True
        ):

            # 店名
            st.markdown(
                f"## {index}. {name}"
            )

            # 距離
            distance = props.get(
                "distance",
                0
            )

            st.write(
                f"🚶 距離：**{distance:.2f} km**"
            )

            # 住所
            address = props.get(
                "formatted",
                ""
            )

            if address:

                st.write(
                    f"📍 {address}"
                )

            # ブランド
            brand = props.get(
                "brand"
            )

            if brand:

                st.write(
                    f"🏪 ブランド：{brand}"
                )

            # 営業時間
            opening = props.get(
                "opening_hours"
            )

            if opening == "24/7":

                opening = "24時間営業"

            if opening:

                st.write(
                    f"⏰ 営業時間：{opening}"
                )

            # カテゴリ
            categories = props.get(
                "categories",
                []
            )

            if categories:

                # 長すぎる場合を少し整理
                category_text = ", ".join(
                    categories[:5]
                )

                st.write(
                    f"📦 カテゴリ：{category_text}"
                )