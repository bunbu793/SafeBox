import streamlit as st

st.set_page_config(page_title="自治体別防災パンフレット", page_icon="📄")

st.title("📄 自治体別防災パンフレット")
st.write("ここでは防災パンフレットを配布されているリンクに移動します。"
            "都道府県を選択すると、自治体の防災パンフレットページへ移動できます。")

pref_links = {
    "北海道": "https://www.pref.hokkaido.lg.jp/ss/kurashi/bousai.html",
    "青森県": "https://www.pref.aomori.lg.jp/safety/bosai/",
    "岩手県": "https://www.pref.iwate.jp/bousai/",
    "宮城県": "https://www.pref.miyagi.jp/soshiki/kikitaisaku/",
    "秋田県": "https://www.pref.akita.lg.jp/pages/archive/479",
    "山形県": "https://www.pref.yamagata.jp/020001/bosai/",
    "福島県": "https://www.pref.fukushima.lg.jp/sec/01a00d/",
    "茨城県": "https://www.pref.ibaraki.jp/bousai/",
    "栃木県": "https://www.pref.tochigi.lg.jp/c01/bousai/",
    "群馬県": "https://www.pref.gunma.jp/05/bousai/",
    "埼玉県": "https://www.pref.saitama.lg.jp/a0401/bousai/",
    "千葉県": "https://www.pref.chiba.lg.jp/bousai/",
    "東京都": "https://www.bousai.metro.tokyo.lg.jp/",
    "神奈川県": "https://www.pref.kanagawa.jp/docs/u3x/bousai/",
    "新潟県": "https://www.pref.niigata.lg.jp/sec/bousai/",
    "富山県": "https://www.pref.toyama.jp/1015/bousai/",
    "石川県": "https://www.pref.ishikawa.lg.jp/bousai/",
    "福井県": "https://www.pref.fukui.lg.jp/doc/bousai/",
    "山梨県": "https://www.pref.yamanashi.jp/bousai/",
    "長野県": "https://www.pref.nagano.lg.jp/bosai/",
    "岐阜県": "https://www.pref.gifu.lg.jp/page/10187.html",
    "静岡県": "https://www.pref.shizuoka.jp/bousai/",
    "愛知県": "https://www.pref.aichi.jp/bousai/",
    "三重県": "https://www.pref.mie.lg.jp/bousai/",
    "滋賀県": "https://www.pref.shiga.lg.jp/bousai/",
    "京都府": "https://www.pref.kyoto.jp/bosai/",
    "大阪府": "https://www.pref.osaka.lg.jp/bousai/",
    "兵庫県": "https://web.pref.hyogo.lg.jp/kk42/bousai.html",
    "奈良県": "https://www.pref.nara.jp/1718.htm",
    "和歌山県": "https://www.pref.wakayama.lg.jp/pref/bousai/",
    "鳥取県": "https://www.pref.tottori.lg.jp/bousai/",
    "島根県": "https://www.pref.shimane.lg.jp/bousai/",
    "岡山県": "https://www.pref.okayama.jp/page/353718.html",
    "広島県": "https://www.pref.hiroshima.lg.jp/site/bousai/",
    "山口県": "https://www.pref.yamaguchi.lg.jp/bousai/",
    "徳島県": "https://www.pref.tokushima.lg.jp/bousai/",
    "香川県": "https://www.pref.kagawa.lg.jp/bousai/",
    "愛媛県": "https://www.pref.ehime.jp/bousai/",
    "高知県": "https://www.pref.kochi.lg.jp/bousai/",
    "福岡県": "https://www.pref.fukuoka.lg.jp/bousai/",
    "佐賀県": "https://www.pref.saga.lg.jp/bousai/",
    "長崎県": "https://www.pref.nagasaki.jp/bousai/",
    "熊本県": "https://www.pref.kumamoto.jp/bousai/",
    "大分県": "https://www.pref.oita.jp/site/bousai/",
    "宮崎県": "https://www.pref.miyazaki.lg.jp/bousai/",
    "鹿児島県": "https://www.pref.kagoshima.jp/bousai/",
    "沖縄県": "https://www.pref.okinawa.jp/site/bousai/"
}

pref = st.selectbox("都道府県を選択してください", list(pref_links.keys()))

st.link_button(
    f"{pref}の防災ページへ移動する",
    pref_links[pref]
)
