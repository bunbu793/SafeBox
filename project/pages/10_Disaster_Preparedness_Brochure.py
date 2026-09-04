import streamlit as st

st.set_page_config(page_title="自治体別防災パンフレット", page_icon="📄")

st.title("📄 自治体別防災パンフレット")
st.write("都道府県を選択すると、自治体の防災パンフレットページへ移動できます。")

pref_links = {
    "北海道": "https://www.pref.hokkaido.lg.jp/category/d007/c032/",
    "青森県": "https://www.pref.aomori.lg.jp/life/bosai/",
    "岩手県": "https://www.pref.iwate.jp/kurashikankyou/anzenanshin/bosai/index.html",
    "宮城県": "https://www.pref.miyagi.jp/life/2/8/244/index.html",
    "秋田県": "https://www.pref.akita.lg.jp/pages/genre/syobo",
    "山形県": "https://www.pref.yamagata.jp/020072/bosai/kochibou/index.html",
    "福島県": "https://www.pref.fukushima.lg.jp/sec/01010a/",
    "茨城県": "https://www.pref.ibaraki.jp/soshiki/seikatsukankyo/bousaikiki/index.html",
    "栃木県": "https://www.pref.tochigi.lg.jp/c01/index.html",
    "群馬県": "https://www.pref.gunma.jp/page/8038.html",
    "埼玉県": "https://www.pref.saitama.lg.jp/kurashi/bosai/index.html",
    "千葉県": "https://www.bousai.pref.chiba.lg.jp/",
    "東京都": "https://www.bousai.metro.tokyo.lg.jp/",
    "神奈川県": "https://www.pref.kanagawa.jp/docs/j8g/",
    "新潟県": "https://www.pref.niigata.lg.jp/site/bosai/",
    "富山県": "https://www.pref.toyama.jp/bousaianzen/index.html",
    "石川県": "https://www.pref.ishikawa.lg.jp/bousai/",
    "福井県": "https://www.pref.fukui.lg.jp/doc/kikitaisaku/portalsite.html",
    "長野県": "https://www.pref.nagano.lg.jp/kurashi/shobo/bosai/index.html",
    "山梨県": "https://www.pref.yamanashi.jp/bousai/",
    "岐阜県": "https://www.pref.gifu.lg.jp/life/1/3/",
    "静岡県": "https://www.pref.shizuoka.jp/bosaikinkyu/index.html",
    "愛知県": "https://www.pref.aichi.jp/bousai/",
    "三重県": "http://www.pref.mie.lg.jp/s_bosai/bosai/index.htm",
    "滋賀県": "https://www.pref.shiga.lg.jp/ippan/bousai/",
    "京都府": "https://www.pref.kyoto.jp/kikikanri/index.html",
    "大阪府": "https://www.pref.osaka.lg.jp/life/list2.php?ctg03_id=11&ctg02_id=67",
    "兵庫県": "http://web.pref.hyogo.lg.jp/safe/index.html",
    "奈良県": "https://www.pref.nara.jp/n010/44720.html",
    "和歌山県": "https://www.pref.wakayama.lg.jp/prefg/011400/",
    "鳥取県": "https://www.pref.tottori.lg.jp/dd.aspx?menuid=8945",
    "島根県": "http://www.pref.shimane.lg.jp/bousai_info/bousai/",
    "岡山県": "https://www.pref.okayama.jp/soshiki/12/",
    "広島県": "https://www.pref.hiroshima.lg.jp/life/3/",
    "山口県": "https://www.pref.yamaguchi.lg.jp/soshiki/6/",
    "徳島県": "https://www.pref.tokushima.lg.jp/ippannokata/bosai/",
    "香川県": "https://www.pref.kagawa.lg.jp/bosai/",
    "愛媛県": "https://www.pref.ehime.jp/site/bousai/",
    "高知県": "https://www.pref.kochi.lg.jp/soshiki/010101/",
    "福岡県": "https://www.pref.fukuoka.lg.jp/life/1/",
    "佐賀県": "https://www.pref.saga.lg.jp/list00512.html",
    "長崎県": "https://www.pref.nagasaki.jp/bunrui/anzen-anshin/bosai-kokuminhogo/index.html",
    "熊本県": "https://www.pref.kumamoto.jp/life/1/1/",
    "大分県": "https://www.pref.oita.jp/site/bosaitaisaku/",
    "宮崎県": "https://www.pref.miyazaki.lg.jp/bosai/",
    "鹿児島県": "http://www.pref.kagoshima.jp/bosai/index.html",
    "沖縄県": "https://www.pref.okinawa.jp/bosaianzen/index.html"
}

pref = st.selectbox("都道府県を選択してください", list(pref_links.keys()))

st.link_button(
    f"{pref}の防災ページへ移動する",
    pref_links[pref]
)
