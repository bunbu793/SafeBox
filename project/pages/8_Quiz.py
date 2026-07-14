import streamlit as st
import random

st.set_page_config(page_title="防災クイズ", page_icon="📝")

# -------------------------
# セッション初期化
# -------------------------
if "rank" not in st.session_state:
    st.session_state.rank = 1          # Lv1スタート
if "points" not in st.session_state:
    st.session_state.points = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "mode" not in st.session_state:
    st.session_state.mode = None
if "practice_questions" not in st.session_state:
    st.session_state.practice_questions = []
if "test_questions" not in st.session_state:
    st.session_state.test_questions = []
if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []
if "play_animation" not in st.session_state:
    st.session_state.play_animation = False

# -------------------------
# レベル別問題データベース
# -------------------------
def get_lv1_questions():
    return [
        {
            "q": "地震が起きたとき、まず最初にすべき行動は？",
            "choices": ["頭を守る", "外に走って出る", "スマホを見る", "窓を開ける"],
            "answer": "頭を守る",
        },
        {
            "q": "避難所で最も大切なことは？",
            "choices": ["静かにする", "情報を共有する", "荷物を広げる", "好きな場所を占領する"],
            "answer": "情報を共有する",
        },
        {
            "q": "災害時に役立つのはどれ？",
            "choices": ["懐中電灯", "ゲーム機", "大きなスピーカー", "観葉植物"],
            "answer": "懐中電灯",
        },
        {
            "q": "非常食として正しいものは？",
            "choices": ["缶詰", "生肉", "アイスクリーム", "ケーキ"],
            "answer": "缶詰",
        },
        {
            "q": "災害時に水が止まった場合、まず使うべき水は？",
            "choices": ["ペットボトルの水", "トイレの水", "お風呂の残り湯", "川の水"],
            "answer": "お風呂の残り湯",
        },
        {
            "q": "避難するときに必要なものは？",
            "choices": ["スマホ", "貴重品", "水", "全部必要"],
            "answer": "全部必要",
        },
        {
            "q": "災害用伝言ダイヤルの番号は？",
            "choices": ["171", "911", "119", "777"],
            "answer": "171",
        },
        {
            "q": "地震の揺れが収まった後にすべきことは？",
            "choices": ["火の確認", "すぐ寝る", "SNSに投稿", "走り回る"],
            "answer": "火の確認",
        },
        {
            "q": "避難所でのトラブルを防ぐために大切なことは？",
            "choices": ["譲り合い", "大声で話す", "荷物を広げる", "他人を無視する"],
            "answer": "譲り合い",
        },
        {
            "q": "災害時に一番大切なのは？",
            "choices": ["命を守ること", "荷物を守ること", "家を守ること", "SNSで情報発信"],
            "answer": "命を守ること",
        },
    ]

def get_lv2_questions():
    return [
        {
            "q": "地震の揺れが強いとき、家の中で最も危険なのは？",
            "choices": ["窓際", "机の下", "布団の中", "玄関"],
            "answer": "窓際",
        },
        {
            "q": "耐震家具の固定に使うべきものは？",
            "choices": ["L字金具", "ガムテープ", "ひも", "接着剤"],
            "answer": "L字金具",
        },
        {
            "q": "地震が起きたとき、エレベーターに乗っていたら？",
            "choices": ["最寄り階で降りる", "そのまま上に行く", "非常ボタンを押す", "ジャンプする"],
            "answer": "最寄り階で降りる",
        },
        {
            "q": "地震の揺れで火災が起きやすい場所は？",
            "choices": ["キッチン", "玄関", "寝室", "トイレ"],
            "answer": "キッチン",
        },
        {
            "q": "地震後にガスの安全確認をする方法は？",
            "choices": ["元栓を閉める", "匂いを嗅ぐ", "火をつける", "ガス管を叩く"],
            "answer": "元栓を閉める",
        },
        {
            "q": "ブロック塀が危険なのはどんなとき？",
            "choices": ["老朽化している", "新築", "低い塀", "鉄筋入り"],
            "answer": "老朽化している",
        },
        {
            "q": "地震の揺れで最も倒れやすい家具は？",
            "choices": ["背の高い家具", "低い棚", "机", "椅子"],
            "answer": "背の高い家具",
        },
        {
            "q": "地震で停電したときに使うべきものは？",
            "choices": ["懐中電灯", "ロウソク", "スマホのライト", "車のライト"],
            "answer": "懐中電灯",
        },
        {
            "q": "地震の後に危険な場所は？",
            "choices": ["倒壊した建物の近く", "公園", "広場", "学校"],
            "answer": "倒壊した建物の近く",
        },
        {
            "q": "地震の揺れが収まった後に外に出るとき注意すべきものは？",
            "choices": ["落下物", "風", "雨", "日差し"],
            "answer": "落下物",
        },
        {
            "q": "地震の後に余震が続く場合の行動として正しいものは？",
            "choices": ["安全な場所で待機", "すぐに家に戻る", "走り回る", "高い場所に登る"],
            "answer": "安全な場所で待機",
        },
        {
            "q": "地震の揺れでガラスが割れた場合に使うべきものは？",
            "choices": ["スリッパや靴", "素足", "手袋だけ", "タオル"],
            "answer": "スリッパや靴",
        },
        {
            "q": "地震の揺れが起きたとき、学校にいる場合の基本行動は？",
            "choices": ["机の下に隠れる", "外に走って出る", "窓から飛び降りる", "廊下に出る"],
            "answer": "机の下に隠れる",
        },
        {
            "q": "地震の後にライフラインの復旧情報を得る方法として適切なのは？",
            "choices": ["自治体の公式情報", "噂話", "SNSだけ", "近所の人の推測"],
            "answer": "自治体の公式情報",
        },
        {
            "q": "地震の揺れで本棚が倒れないようにする対策は？",
            "choices": ["壁に固定する", "本を減らす", "床に置く", "何もしない"],
            "answer": "壁に固定する",
        },
    ]

def get_lv3_questions():
    return [
        {
            "q": "避難指示が出たときにまず確認すべきことは？",
            "choices": ["避難経路", "天気", "SNSの反応", "テレビ番組表"],
            "answer": "避難経路",
        },
        {
            "q": "避難するときに靴として適切なのは？",
            "choices": ["運動靴", "サンダル", "ハイヒール", "裸足"],
            "answer": "運動靴",
        },
        {
            "q": "避難所に向かうとき、持ち出し品として優先度が高いものは？",
            "choices": ["水・食料・貴重品", "ゲーム機", "観葉植物", "大きな家具"],
            "answer": "水・食料・貴重品",
        },
        {
            "q": "避難所でのプライバシー確保に役立つものは？",
            "choices": ["仕切り用の布や段ボール", "大きな声", "ライト", "鏡"],
            "answer": "仕切り用の布や段ボール",
        },
        {
            "q": "避難所での情報収集に適切なものは？",
            "choices": ["自治体の掲示板", "噂話", "不確かなSNS情報", "占い"],
            "answer": "自治体の掲示板",
        },
        {
            "q": "避難所での感染症対策として重要なものは？",
            "choices": ["手洗い・消毒", "大声で話す", "マスクを外す", "密集する"],
            "answer": "手洗い・消毒",
        },
        {
            "q": "避難所での食事の配布時に心がけるべきことは？",
            "choices": ["譲り合い", "先に取りに行く", "多めに取る", "列を無視する"],
            "answer": "譲り合い",
        },
        {
            "q": "避難所での夜間の過ごし方として適切なのは？",
            "choices": ["静かに休む", "大音量で音楽を流す", "走り回る", "明かりをつけっぱなしにする"],
            "answer": "静かに休む",
        },
        {
            "q": "避難所でのペットの扱いとして適切なのは？",
            "choices": ["ルールに従い指定場所で管理", "自由に歩かせる", "他人に預ける", "隠して連れて行く"],
            "answer": "ルールに従い指定場所で管理",
        },
        {
            "q": "避難所でのトラブルを防ぐために重要なことは？",
            "choices": ["コミュニケーション", "無視する", "怒鳴る", "自分だけ優先する"],
            "answer": "コミュニケーション",
        },
        {
            "q": "避難所に到着したときにまず行うべきことは？",
            "choices": ["受付で登録する", "好きな場所に寝る", "荷物を広げる", "スマホゲームを始める"],
            "answer": "受付で登録する",
        },
        {
            "q": "避難所での子どものケアとして適切なのは？",
            "choices": ["安心させる声かけ", "放置する", "叱りつける", "一人にさせる"],
            "answer": "安心させる声かけ",
        },
        {
            "q": "避難所での高齢者への配慮として適切なのは？",
            "choices": ["段差や移動のサポート", "重い荷物を持たせる", "順番を後回しにする", "声をかけない"],
            "answer": "段差や移動のサポート",
        },
        {
            "q": "避難所でのゴミの扱いとして適切なのは？",
            "choices": ["分別して指定場所に捨てる", "その場に置く", "隠す", "燃やす"],
            "answer": "分別して指定場所に捨てる",
        },
        {
            "q": "避難所での水の使い方として適切なのは？",
            "choices": ["節約して使う", "好きなだけ使う", "他人の分も使う", "遊びに使う"],
            "answer": "節約して使う",
        },
    ]

def get_lv4_questions():
    return [
        {
            "q": "家庭の備蓄で最低限必要な水の量は？（1人1日あたり）",
            "choices": ["3リットル", "500ミリリットル", "10リットル", "1リットル"],
            "answer": "3リットル",
        },
        {
            "q": "非常食として適切なものは？",
            "choices": ["長期保存できる食品", "生もの", "冷凍食品のみ", "調理が複雑な料理"],
            "answer": "長期保存できる食品",
        },
        {
            "q": "備蓄品として優先度が高いものは？",
            "choices": ["水・食料・薬", "観葉植物", "大型テレビ", "装飾品"],
            "answer": "水・食料・薬",
        },
        {
            "q": "非常用持ち出し袋に入れるべきものは？",
            "choices": ["懐中電灯・ラジオ・電池", "大きな家具", "大量の本", "観葉植物"],
            "answer": "懐中電灯・ラジオ・電池",
        },
        {
            "q": "備蓄品の点検頻度として適切なのは？",
            "choices": ["半年〜1年に1回", "10年に1回", "一度買えば点検不要", "毎日"],
            "answer": "半年〜1年に1回",
        },
        {
            "q": "非常用トイレとして適切なものは？",
            "choices": ["簡易トイレ・凝固剤", "そのまま流す", "庭に穴を掘るだけ", "使わない"],
            "answer": "簡易トイレ・凝固剤",
        },
        {
            "q": "備蓄品として役立つものは？",
            "choices": ["カセットコンロ", "IHコンロのみ", "電子レンジのみ", "炊飯器のみ"],
            "answer": "カセットコンロ",
        },
        {
            "q": "非常用の情報収集手段として適切なのは？",
            "choices": ["電池式ラジオ", "テレビのみ", "SNSのみ", "噂話"],
            "answer": "電池式ラジオ",
        },
        {
            "q": "備蓄品としての乾電池の管理方法として適切なのは？",
            "choices": ["使用期限を確認する", "期限を気にしない", "冷凍庫に入れる", "外に置いておく"],
            "answer": "使用期限を確認する",
        },
        {
            "q": "非常用持ち出し袋に入れるべき書類は？",
            "choices": ["身分証・保険証のコピー", "雑誌", "チラシ", "古いノート"],
            "answer": "身分証・保険証のコピー",
        },
        {
            "q": "備蓄品としての薬の管理方法として適切なのは？",
            "choices": ["使用期限を確認し入れ替える", "期限切れでも使う", "大量に買って放置", "他人の薬を使う"],
            "answer": "使用期限を確認し入れ替える",
        },
        {
            "q": "非常用持ち出し袋に入れる衣類として適切なのは？",
            "choices": ["動きやすい服", "フォーマルスーツ", "ドレス", "厚手のコートのみ"],
            "answer": "動きやすい服",
        },
        {
            "q": "備蓄品としての水の保管場所として適切なのは？",
            "choices": ["直射日光を避けた場所", "屋外の直射日光下", "車内", "暖房の近く"],
            "answer": "直射日光を避けた場所",
        },
        {
            "q": "非常用持ち出し袋に入れるべき衛生用品は？",
            "choices": ["マスク・ティッシュ・消毒液", "香水のみ", "化粧品のみ", "何も入れない"],
            "answer": "マスク・ティッシュ・消毒液",
        },
        {
            "q": "備蓄品としての食料の選び方として適切なのは？",
            "choices": ["長期保存できて簡単に食べられるもの", "調理が複雑なもの", "冷蔵が必要なもの", "生もの"],
            "answer": "長期保存できて簡単に食べられるもの",
        },
    ]

def get_lv5_questions():
    return [
        {
            "q": "災害時に家族と連絡を取る方法として事前に決めておくべきなのは？",
            "choices": ["連絡手段と集合場所", "その場のノリ", "SNSだけ", "電話だけ"],
            "answer": "連絡手段と集合場所",
        },
        {
            "q": "災害時に子どもに教えておくべきことは？",
            "choices": ["避難場所と連絡先", "ゲームのスコア", "テレビ番組表", "好きな食べ物"],
            "answer": "避難場所と連絡先",
        },
        {
            "q": "災害時に高齢者への配慮として重要なのは？",
            "choices": ["移動のサポート", "荷物を持たせる", "一人にさせる", "声をかけない"],
            "answer": "移動のサポート",
        },
        {
            "q": "災害時にペットを守るために事前に準備すべきことは？",
            "choices": ["キャリーケースや餌の備蓄", "何もしない", "外に放す", "他人に預ける"],
            "answer": "キャリーケースや餌の備蓄",
        },
        {
            "q": "災害時に近所との助け合いで重要なのは？",
            "choices": ["日頃からの顔の見える関係", "全く交流しない", "トラブルを避けるため話さない", "噂話だけする"],
            "answer": "日頃からの顔の見える関係",
        },
        {
            "q": "災害時に正しい情報を得るために重要なのは？",
            "choices": ["自治体や公的機関の情報", "噂話", "不確かなSNS情報", "占い"],
            "answer": "自治体や公的機関の情報",
        },
        {
            "q": "災害時にボランティアとして活動する際に重要なのは？",
            "choices": ["指示に従い安全に行動する", "勝手に動く", "自分のやりたいことだけする", "ルールを無視する"],
            "answer": "指示に従い安全に行動する",
        },
        {
            "q": "災害後の心のケアとして重要なのは？",
            "choices": ["話を聞いてもらうこと", "一人で抱え込む", "我慢する", "何も話さない"],
            "answer": "話を聞いてもらうこと",
        },
        {
            "q": "災害時にSNSを使う際に注意すべきことは？",
            "choices": ["デマを拡散しない", "感情的に投稿する", "未確認情報を広める", "誰かを責める投稿をする"],
            "answer": "デマを拡散しない",
        },
        {
            "q": "災害時に車で避難する際の注意点は？",
            "choices": ["渋滞や通行止めに注意する", "とにかく急ぐ", "歩行者を無視する", "狭い道に突っ込む"],
            "answer": "渋滞や通行止めに注意する",
        },
        {
            "q": "災害時に自宅が危険と判断された場合の行動として適切なのは？",
            "choices": ["指定避難所に向かう", "そのまま家にいる", "近所の空き地に行く", "車の中にいる"],
            "answer": "指定避難所に向かう",
        },
        {
            "q": "災害時に電気が復旧した直後に注意すべきことは？",
            "choices": ["ブレーカーや配線の安全確認", "すぐに家電をフル稼働", "大量に電気を使う", "何も確認しない"],
            "answer": "ブレーカーや配線の安全確認",
        },
        {
            "q": "災害時にガスが復旧した直後に注意すべきことは？",
            "choices": ["ガス漏れの有無を確認する", "すぐに火をつける", "大量にガスを使う", "確認せず使う"],
            "answer": "ガス漏れの有無を確認する",
        },
        {
            "q": "災害時に水道が復旧した直後に注意すべきことは？",
            "choices": ["濁りや異臭の確認", "すぐに大量に飲む", "確認せず使う", "他人にだけ使わせる"],
            "answer": "濁りや異臭の確認",
        },
        {
            "q": "災害後に地域の防災力を高めるために重要なのは？",
            "choices": ["防災訓練への参加", "何もしない", "他人任せにする", "過去の災害を忘れる"],
            "answer": "防災訓練への参加",
        },
    ]

# レジェンド用（ここでは例として20問。必要なら増やせる）
def get_legend_questions():
    base = get_lv1_questions() + get_lv2_questions() + get_lv3_questions() + get_lv4_questions() + get_lv5_questions()
    # 実際はここにさらに難問を追加して100問にしてもOK
    return base

# -------------------------
# 問題数ロジック
# -------------------------
def get_practice_count(rank: int) -> int:
    # Lv1:10問、以降5問ずつ増加
    if rank >= 20:
        return 100  # レジェンド
    return 10 + (rank - 1) * 5

def get_test_count() -> int:
    return 10

# -------------------------
# レベルに応じた問題セット取得
# -------------------------
def get_questions_for_rank(rank: int):
    if rank == 1:
        return get_lv1_questions()
    elif rank == 2:
        return get_lv2_questions()
    elif rank == 3:
        return get_lv3_questions()
    elif rank == 4:
        return get_lv4_questions()
    elif rank == 5:
        return get_lv5_questions()
    else:
        return get_legend_questions()

# -------------------------
# ヘッダー表示
# -------------------------
st.title("📝 防災クイズ")

legend = st.session_state.rank >= 20
if legend:
    st.success(f"🌟 レジェンドランク：Lv.{st.session_state.rank}")
else:
    st.info(f"現在のランク：Lv.{st.session_state.rank}")

st.success(f"累計ポイント：{st.session_state.points} pt")
st.write(f"連勝記録：{st.session_state.streak} 問")

st.divider()

# -------------------------
# モード選択
# -------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 練習問題を始める"):
        st.session_state.mode = "practice"
        st.session_state.wrong_questions = []
        st.session_state.streak = 0
        st.session_state.play_animation = False

        all_qs = get_questions_for_rank(st.session_state.rank)
        n = get_practice_count(st.session_state.rank)
        # 足りなければランダム重複で補う
        if len(all_qs) >= n:
            st.session_state.practice_questions = random.sample(all_qs, n)
        else:
            st.session_state.practice_questions = all_qs + random.choices(all_qs, k=n - len(all_qs))

with col2:
    if st.button("🔥 テストを受ける（9問正解で合格）"):
        st.session_state.mode = "test"
        st.session_state.wrong_questions = []
        st.session_state.streak = 0
        st.session_state.play_animation = False

        # テスト問題は練習問題の中からランダム
        if not st.session_state.practice_questions:
            all_qs = get_questions_for_rank(st.session_state.rank)
            n = get_practice_count(st.session_state.rank)
            if len(all_qs) >= n:
                st.session_state.practice_questions = random.sample(all_qs, n)
            else:
                st.session_state.practice_questions = all_qs + random.choices(all_qs, k=n - len(all_qs))

        st.session_state.test_questions = random.sample(
            st.session_state.practice_questions,
            min(get_test_count(), len(st.session_state.practice_questions))
        )

st.divider()

# -------------------------
# 共通：問題表示ロジック
# -------------------------
def show_question_block(q_list, prefix):
    for idx, q in enumerate(q_list):
        st.write(f"### {q['q']}")
        user_answer = st.radio(
            "回答を選択してください",
            q["choices"],
            key=f"{prefix}_ans_{idx}"
        )

        if st.button(f"回答する（{idx+1}/{len(q_list)}）", key=f"{prefix}_btn_{idx}"):
            if user_answer == q["answer"]:
                st.success("正解！ +1pt")
                st.session_state.points += 1
                st.session_state.streak += 1
                st.session_state.play_animation = True  # アニメーション用フラグ

                # 連勝ボーナス
                if st.session_state.streak == 5:
                    st.session_state.points += 3
                    st.info("🔥 5連勝ボーナス +3pt")
                if st.session_state.streak == 10:
                    st.session_state.points += 10
                    st.info("🔥 10連勝ボーナス +10pt")
                if st.session_state.streak == 20:
                    st.session_state.points += 30
                    st.info("🔥 20連勝ボーナス +30pt")
            else:
                st.error("不正解… -1pt")
                st.session_state.points -= 1
                st.session_state.streak = 0
                if prefix == "practice":
                    st.session_state.wrong_questions.append(q)

# -------------------------
# 練習モード
# -------------------------
if st.session_state.mode == "practice":
    st.subheader(f"🎯 練習問題（{get_practice_count(st.session_state.rank)}問）")
    show_question_block(st.session_state.practice_questions, "practice")

    if st.session_state.wrong_questions:
        st.divider()
        st.subheader("📘 間違い直し（ポイント変動なし）")

        for idx, q in enumerate(st.session_state.wrong_questions):
            st.write(f"### {q['q']}")
            user_answer = st.radio(
                "復習回答を選択してください",
                q["choices"],
                key=f"fix_ans_{idx}"
            )

            if st.button(
                f"復習回答する（{idx+1}/{len(st.session_state.wrong_questions)}）",
                key=f"fix_btn_{idx}"
            ):
                if user_answer == q["answer"]:
                    st.success("正解！よく復習できました。")
                else:
                    st.error("まだ違う…もう一度見直そう。")

# -------------------------
# テストモード
# -------------------------
if st.session_state.mode == "test":
    st.subheader("🔥 テスト（10問）")
    test_qs = st.session_state.test_questions
    show_question_block(test_qs, "test")

    if st.button("テスト結果を集計する"):
        correct_count = 0
        for idx, q in enumerate(test_qs):
            ans = st.session_state.get(f"test_ans_{idx}")
            if ans == q["answer"]:
                correct_count += 1

        st.write(f"### テスト結果：{correct_count} / {len(test_qs)}")

        if correct_count >= 9:
            st.success("🎉 合格！ランクアップ！")
            st.session_state.rank += 1

            if correct_count == 9:
                st.session_state.points += 900
                st.info("テストボーナス：+900pt")
            else:
                st.session_state.points += 1200
                st.info("テストボーナス：+1200pt")

            if st.session_state.rank >= 20:
                st.success("🌟 レジェンド到達！あなたは防災マスターです。")
        else:
            st.error("不合格… また挑戦しよう！")
