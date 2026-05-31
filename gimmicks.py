import streamlit as st
import random
import time

def init_session():
    if "scores" not in st.session_state:
        st.session_state.scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
    if "page" not in st.session_state: st.session_state.page = 0
    if "error_handled" not in st.session_state: st.session_state.error_handled = False
    if "action_logs" not in st.session_state: st.session_state.action_logs = []
    
    if "te_logged" not in st.session_state: st.session_state.te_logged = False
    if "si_logged" not in st.session_state: st.session_state.si_logged = False
    if "imomushi_logged" not in st.session_state: st.session_state.imomushi_logged = False
    
    if "ni_hints" not in st.session_state: st.session_state.ni_hints = 0
    if "ni_start" not in st.session_state: st.session_state.ni_start = 0.0
    if "ni2_start" not in st.session_state: st.session_state.ni2_start = 0.0
    
    if "ti_history" not in st.session_state: st.session_state.ti_history = []
    if "ti_exp_count" not in st.session_state: st.session_state.ti_exp_count = 0
    if "ti_target" not in st.session_state: st.session_state.ti_target = random.randint(25, 95)
    if "ti_mult" not in st.session_state: st.session_state.ti_mult = random.randint(2, 6)

    if "se_color_ans" not in st.session_state:
        st.session_state.se_color_ans = random.choice(["A", "B", "C", "D"])
        r, g, b = random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)
        st.session_state.se_color_base = f"#{r:02x}{g:02x}{b:02x}"
        st.session_state.se_color_diff = f"#{min(255, r+18):02x}{g:02x}{b:02x}"

    if "te_employees" not in st.session_state:
        st.session_state.te_employees = [
            {"name": "従業員A", "p": 95, "t": 10, "ans": "R&D"},
            {"name": "従業員B", "p": 30, "t": 85, "ans": "Support"},
            {"name": "従業員C", "p": 60, "t": 40, "ans": "Sales"},
            {"name": "従業員D", "p": 82, "t": 75, "ans": "R&D"},
            {"name": "従業員E", "p": 15, "t": 90, "ans": "Support"},
            {"name": "従業員F", "p": 70, "t": 70, "ans": "Sales"},
            {"name": "従業員G", "p": 90, "t": 80, "ans": "R&D"},
            {"name": "従業員H", "p": 50, "t": 50, "ans": "Sales"},
        ]
        st.session_state.te_current_emp = 0
        st.session_state.te_correct = 0
        st.session_state.te_start_time = 0.0
        st.session_state.te_done = False

    if "si_step" not in st.session_state: st.session_state.si_step = "start"
    if "si_level" not in st.session_state: st.session_state.si_level = 1
    if "si_target" not in st.session_state: st.session_state.si_target = ""
    
    if "drum_count" not in st.session_state: st.session_state.drum_count = 0
    if "bus_emojis" not in st.session_state: st.session_state.bus_emojis = ""
    if "thrill_state" not in st.session_state: st.session_state.thrill_state = "start"
    if "thrill_start" not in st.session_state: st.session_state.thrill_start = 0.0
    
    if "imomushi_clicks" not in st.session_state: st.session_state.imomushi_clicks = 0
    if "imomushi_crushed" not in st.session_state: st.session_state.imomushi_crushed = False

    if "fe_empathy" not in st.session_state: st.session_state.fe_empathy = 0
    if "fi_active_words" not in st.session_state: 
        st.session_state.fi_active_words = ["空気読め", "自己中", "使えない", "お前はダメだ", "調子乗んな"]
    if "fi_destroyed_count" not in st.session_state: st.session_state.fi_destroyed_count = 0

def add_log(msg):
    st.session_state.action_logs.append(msg)

def next_page():
    st.session_state.page += 1
    st.rerun()

def run_te_ti_error():
    st.markdown('<div class="fake-error">⚠️ 警告：セッションID[0x9A4F]が破損しています。</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("無視して診断を始める"):
            st.session_state.scores["Te"] += 2
            add_log("【Te】エラーを無視して目的を優先した")
            next_page()
    with col2:
        if st.button("エラーの詳細を確認する"):
            st.session_state.scores["Ti"] += 2
            add_log("【Ti】エラーの原因を確認しようとした")
            st.success("ドッキリ大成功！")
            time.sleep(1.5)
            next_page()

def run_p1_ni_flash():
    st.header("🧠 Part 1: 閃きの降臨")
    st.write("直感で本質を当てて！「あ、わかった！」という感覚が降ってきたら入力してね。")
    if st.session_state.ni_start == 0.0:
        if st.button("謎解きを見る"):
            st.session_state.ni_start = time.time()
            st.rerun()
    else:
        st.info("『見えない刃。人を傷つけることも、癒すこともできる。形はないが、一生残る。』")
        if st.session_state.ni_hints > 0: st.warning("ヒント1：口から出るものです")
        if st.session_state.ni_hints > 1: st.warning("ヒント2：『○○○』のキャッチボール")
        
        ans = st.text_input("これは何？", key="ni_ans")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ヒントを見る👀"):
                st.session_state.ni_hints += 1
                add_log("【Ni】ヒントを確認した")
                st.rerun()
        with col2:
            if st.button("決定！"):
                if "言葉" in ans or "ことば" in ans or "コトバ" in ans:
                    time_taken = time.time() - st.session_state.ni_start
                    if st.session_state.ni_hints == 0 and time_taken < 10.0: st.session_state.scores["Ni"] += 6
                    elif st.session_state.ni_hints == 0: st.session_state.scores["Ni"] += 4
                    else: st.session_state.scores["Ni"] += 2
                    add_log(f"【Ni】閃きテスト正解！ ({time_taken:.1f}秒 / ヒント{st.session_state.ni_hints}回)")
                    st.success("大正解！")
                else:
                    add_log(f"【Ni】閃きテスト不正解 (回答: {ans})")
                    st.error("不正解！正解は「言葉」でした！")
                time.sleep(1.5)
                next_page()

def run_p2_ni_pattern():
    st.header("🔮 Part 2: 共通概念の抽出")
    st.write("Q. 以下の3つの事象から連想される、この宇宙の**『避けることのできない絶対法則（共通の本質）』**を1単語で抽出してください。")
    st.info("・落ちる砂時計 ｜ ・燃えて短くなるロウソク ｜ ・散っていく桜")
    if st.session_state.ni2_start == 0.0:
        st.session_state.ni2_start = time.time()

    ans = st.text_input("本質を見抜いて入力！", key="ni2_ans")
    if st.button("決定！"):
        time_taken = time.time() - st.session_state.ni2_start
        deep_ni_keywords = ["不可逆", "無常", "エントロピー", "有限", "終焉", "退廃", "サイクル", "死", "衰退"]
        common_ni_keywords = ["時間", "命", "寿命", "桜", "時計", "時の流れ", "時間経過", "変化"]
        
        if any(k in ans for k in deep_ni_keywords):
            st.session_state.scores["Ni"] += 7
            add_log(f"【Ni】高度な抽象化テストに大正解！(回答: {ans} / {time_taken:.1f}秒)")
            st.success("素晴らしい！現象の裏に潜む本質的な法則を完璧に捉えました！")
        elif any(k in ans for k in common_ni_keywords):
            if time_taken < 12.0:
                st.session_state.scores["Ni"] += 6
                add_log(f"【Ni】神速の直感で抽象化テストに正解！(回答: {ans} / {time_taken:.1f}秒)")
                st.success("神速の直感！一瞬で本質を見抜きましたね！")
            else:
                st.session_state.scores["Ni"] += 3
                add_log(f"【Ni】抽象化テストに正解。(回答: {ans} / {time_taken:.1f}秒)")
                st.success("正解です！")
        else:
            add_log(f"【Ni】抽象概念テスト不正解 (回答: {ans})")
            st.error("ちょっと違うかも…？正解は「時間」や「無常」などでした！")
        time.sleep(2.0)
        next_page()

def run_p3_ti_blackbox():
    st.header("⚙️ Part 3: 機械の法則検証")
    st.write("目の前に『謎の変換マシン』があります。数字を入れて検証し、背後にある【法則】を解明してください！")
    
    target_num = st.session_state.ti_target
    mult = st.session_state.ti_mult
    
    test_val = st.number_input("検証用の数字を入力:", min_value=0, max_value=999, step=1, key="ti_box_in")
    
    if st.button("この数字で検証する"):
        if test_val == target_num:
            st.error(f"⚠️ 本番クイズの数字『{target_num}』は検証テストに入力できません！")
        else:
            digits_sum = sum(int(char) for char in str(test_val))
            out_val = digits_sum * mult
            st.session_state.ti_history.append((test_val, out_val))
            if st.session_state.ti_exp_count < 5:
                st.session_state.scores["Ti"] += 1.5 
            st.session_state.ti_exp_count += 1
            add_log(f"【Ti】ブラックボックスに『{test_val}』を入力して検証した")
            st.rerun()
            
    if len(st.session_state.ti_history) > 0:
        st.write("📋 検証データ履歴:")
        for inp, out in st.session_state.ti_history[-6:]:
            st.code(f"入力： {inp}  👉  出力： {out}")
            
    st.divider()
    st.write("❓ 法則が見えてきましたか？ 本番クイズです。")
    final_ans = st.text_input(f"入力が『 {target_num} 』の場合、出力は何になる？", key="ti_final_ans")
    
    if st.button("法則を解明したので決定！"):
        correct_ans = str(sum(int(char) for char in str(target_num)) * mult)
        if final_ans == correct_ans:
            st.session_state.scores["Ti"] += 2.5
            add_log(f"【Ti】法則を完璧に解明した！(検証回数: {st.session_state.ti_exp_count}回)")
            st.success("大正解！完璧に法則を解明しました！")
        else:
            add_log(f"【Ti】法則解明失敗 (回答: {final_ans} / 検証: {st.session_state.ti_exp_count}回)")
            st.error(f"残念！正解は『{correct_ans}』でした。")
        time.sleep(2.5)
        next_page()

def run_p4_te_sort():
    st.header("💼 Part 4: 従業員高速仕分け業務")
    st.write("【任務】ルールに従って従業員8名を高速仕分けしてください！")
    st.info("📊 仕分けルール：\n・**【🏠 R&D部門】**：パフォーマンス 80%以上\n・**【📞 Support部門】**：協調性 80%以上 (かつパフォーマンス80%未満)\n・**【💼 Sales部門】**：それ以外")
    
    if st.session_state.te_start_time == 0.0:
        if st.button("仕分け業務を開始する！"):
            st.session_state.te_start_time = time.time()
            st.rerun()
    elif not st.session_state.te_done:
        idx = st.session_state.te_current_emp
        emp = st.session_state.te_employees[idx]
        st.subheader(f"👤 被評価者: {emp['name']} ( {idx + 1} / 8 )")
        st.write(f"📈 パフォーマンス: **{emp['p']}%** ｜ 🤝 協調性: **{emp['t']}%**")
        
        col1, col2, col3 = st.columns(3)
        user_choice = None
        with col1:
            if st.button("🏠 R&D部門へ"): user_choice = "R&D"
        with col2:
            if st.button("📞 Support部門へ"): user_choice = "Support"
        with col3:
            if st.button("💼 Sales部門へ"): user_choice = "Sales"
            
        if user_choice:
            if user_choice == emp['ans']: st.session_state.te_correct += 1
            if idx + 1 < len(st.session_state.te_employees):
                st.session_state.te_current_emp += 1
            else:
                st.session_state.te_done = True
            st.rerun()
    else:
        if not st.session_state.te_logged:
            elapsed = time.time() - st.session_state.te_start_time
            corrects = st.session_state.te_correct
            
            te_score = corrects * 0.4
            time_bonus = 0
            if corrects >= 6:
                if elapsed < 15.0: time_bonus = 6.0      
                elif elapsed < 22.0: time_bonus = 4.0    
                elif elapsed < 30.0: time_bonus = 2.0    
            
            st.session_state.scores["Te"] += te_score + time_bonus
            add_log(f"【Te】仕分け業務完了 (正解: {corrects}/8名, タイム: {elapsed:.2f}秒)")
            st.session_state.te_logged = True
            st.rerun()
            
        st.success(f"🎉 業務完了！(正解数: {st.session_state.te_correct})")
        if st.button("次へ進む"):
            next_page()

def run_p5_si_memory():
    st.header("💾 Part 5: 記憶サバイバル")
    if st.session_state.si_step == "start":
        if st.button("記憶テストを開始！"):
            st.session_state.si_target = str(random.randint(1000, 9999))
            st.session_state.si_step = "memorize"
            st.rerun()
    elif st.session_state.si_step == "memorize":
        if st.button("▶️ 表示スタート！"):
            placeholder = st.empty()
            time.sleep(0.5)
            for char in st.session_state.si_target:
                placeholder.markdown(f"<h1 style='text-align:center; font-size: 80px; color: #ff4b4b;'>{char}</h1>", unsafe_allow_html=True)
                time.sleep(0.4)
                placeholder.empty()
                time.sleep(0.2)
            st.session_state.si_step = "answer"
            st.rerun()
    elif st.session_state.si_step == "answer":
        user_ans = st.text_input("数字を入力！", key=f"si_ans_{st.session_state.si_level}")
        if st.button("決定！"):
            if user_ans == st.session_state.si_target:
                st.session_state.scores["Si"] += 2.0
                st.session_state.si_level += 1
                st.success(f"正解！次はレベル{st.session_state.si_level}！")
                st.session_state.si_target = "".join([str(random.randint(0, 9)) for _ in range(4 + (st.session_state.si_level - 1) * 2)])
                st.session_state.si_step = "memorize"
                time.sleep(1.0)
                st.rerun()
            else:
                if not st.session_state.si_logged:
                    add_log(f"【Si】記憶テスト終了 (到達レベル: {st.session_state.si_level})")
                    st.session_state.si_logged = True
                    st.rerun()
                st.error("❌ 残念！そこまで！")
                time.sleep(1.5)
                next_page()

def run_p6_se_color():
    st.header("🎨 Part 6: 微細な差異の感知")
    st.write("Q. 以下の4つのタイルのうち、**『1つだけ微妙に違う色』**のものがあります。直接クリックして見抜いてください！")
    
    colors = {"A": st.session_state.se_color_base, "B": st.session_state.se_color_base, "C": st.session_state.se_color_base, "D": st.session_state.se_color_base}
    ans_key = st.session_state.se_color_ans
    colors[ans_key] = st.session_state.se_color_diff
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div style="background-color:{colors["A"]}; height:80px; border-radius:5px; text-align:center; line-height:80px; color:white; font-size:24px; font-weight:bold;">A</div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div style="background-color:{colors["B"]}; height:80px; border-radius:5px; text-align:center; line-height:80px; color:white; font-size:24px; font-weight:bold;">B</div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div style="background-color:{colors["C"]}; height:80px; border-radius:5px; text-align:center; line-height:80px; color:white; font-size:24px; font-weight:bold;">C</div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div style="background-color:{colors["D"]}; height:80px; border-radius:5px; text-align:center; line-height:80px; color:white; font-size:24px; font-weight:bold;">D</div>', unsafe_allow_html=True)
        
    b1, b2, b3, b4 = st.columns(4)
    choice = None
    with b1: 
        if st.button("Aを指差す"): choice = "A"
    with b2: 
        if st.button("Bを指差す"): choice = "B"
    with b3: 
        if st.button("Cを指差す"): choice = "C"
    with b4: 
        if st.button("Dを指差す"): choice = "D"
        
    if choice:
        if choice == ans_key:
            st.session_state.scores["Se"] += 0.5  
            add_log("【Se】色彩感覚テスト: 正解")
            st.success("大正解！")
        else:
            add_log(f"【Se】色彩感覚テスト: 不正解 (選択: {choice})")
            st.error(f"残念！正解は『{ans_key}』でした！")
        time.sleep(1.5)
        next_page()

def run_p7_se_games():
    st.header("🥁 Part 7: 感覚とスリル")
    
    st.subheader("🪘 陽キャバス")
    st.write("目の前に自由に叩ける楽器があります。直感のままに叩いてみて！")
    if st.button("楽器をドコドコ叩く！！（連打OK）"):
        st.session_state.drum_count += 1
        st.session_state.bus_emojis += random.choice(["🎵", "🥁", "🎶", "🎷", "💥", "✨"])
    st.markdown(f"<h2 style='text-align:center;'>{st.session_state.bus_emojis}</h2>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("⏱️ 10秒チキンレース")
    st.write("画面にタイマーは出ません。感覚だけで『ピッタリ10.00秒』経ったと思ったらストップを押して！")
    if st.session_state.thrill_state == "start":
        if st.button("スタート！"):
            st.session_state.thrill_start = time.time()
            st.session_state.thrill_state = "running"
            st.rerun()
    elif st.session_state.thrill_state == "running":
        if st.button("ストップ！"):
            diff = time.time() - st.session_state.thrill_start
            error = abs(10.0 - diff)
            if error <= 0.15: st.session_state.scores["Se"] += 6.0
            elif error <= 0.5: st.session_state.scores["Se"] += 3.0
            st.session_state.thrill_result = f"記録: {diff:.2f}秒 (誤差 {error:.2f}秒)"
            st.session_state.thrill_state = "done"
            add_log(f"【Se】チキンレース: {diff:.2f}秒 (誤差 {error:.2f}秒)")
            st.rerun()
    elif st.session_state.thrill_state == "done":
        st.success(st.session_state.thrill_result)
        if st.button("次へ進む"):
            add_log(f"【Se】陽キャバスを {st.session_state.drum_count}回 叩いた")
            # ★ Se上限ストッパー完全撤廃！叩いた分だけ無限に伸びる！
            st.session_state.scores["Se"] += st.session_state.drum_count * 0.1
            next_page()

def run_p8_imomushi():
    st.header("🐛 Part 8: 芋虫襲来")
    st.write("画面を芋虫が横切っています……")
    clicks = st.session_state.imomushi_clicks
    if clicks < 30:
        space_left = "　" * (30 - clicks)
        space_right = "　" * clicks
        if st.button(f"{space_left}🐛{space_right}", key="bug_btn"):
            st.session_state.imomushi_clicks += 1
            st.rerun()
        if clicks == 0: st.caption("「……（お散歩中）」")
        elif clicks < 5: st.caption("「何だね？僕は考え事に耽りながら散歩中だ。」")
        elif clicks < 10: st.caption("「おいおい、むやみに触らないでくれたまえ。」")
        elif clicks < 15: st.caption("「……お前僕を怒らせたいのか？」")
        elif clicks < 25: st.caption("「しつこいな！お前、SLEか！？やめろ！」")
        else: st.caption("「やめろと言っているだろう！や、やめ…！！」")
        
        st.divider()
        if st.button("無視して次へ進む"):
            add_log(f"【Se/Te】芋虫を {clicks}回 つついて放置した")
            next_page()
    else:
        st.error("💥 ﾌﾞチュッ…")
        if not st.session_state.imomushi_logged:
            st.session_state.scores["Se"] += 3
            st.session_state.scores["Te"] += 3
            st.session_state.imomushi_crushed = True
            add_log("【Se/Te】芋虫を30回つついて無残にも潰した")
            st.session_state.imomushi_logged = True
            st.rerun()
            
        if st.button("無残な光景を後にして次へ進む"):
            next_page()

def run_p9_emotion():
    st.header("💖 Part 9: 感情の防衛と共感")
    
    st.subheader("📺 共感テスト")
    st.write("【状況】テレビで、雨に濡れて震える可哀想な子犬の映像が流れています……")
    st.write("この子犬に対して、何かしてあげたい・感情が動かされたならボタンを押してください。")
    if st.button("🥺 心を寄せる（連打可能）"):
        st.session_state.fe_empathy += 1
        st.rerun()
    
    if st.session_state.fe_empathy > 0:
        st.markdown(f"<h3 style='color:#ff4b4b; line-height:1.2;'>{'🥺可哀想… ' * st.session_state.fe_empathy}</h3>", unsafe_allow_html=True)
        
    st.divider()
    
    st.subheader("🛡️ 自己防衛シューティング")
    st.write("画面にあなたに向かってくる『悪意のクソ文句』があります。クリックして撃ち落としてください！")
    
    cols = st.columns(5)
    for i, word in enumerate(st.session_state.fi_active_words):
        with cols[i]:
            if st.button(f"💥 {word}", key=f"fi_shoot_{i}_{st.session_state.fi_destroyed_count}"):
                st.session_state.fi_destroyed_count += 1
                st.session_state.fi_active_words[i] = random.choice([
                    "期待外れ", "ノリ悪い", "生意気", "痛い奴", "常識ない", 
                    "言い訳すんな", "やる気あんの？", "自己満足", "綺麗事"
                ])
                st.rerun()
                
    st.write(f"撃ち落とした悪口の数: **{st.session_state.fi_destroyed_count} 個**")

    st.divider()
    if st.button("満足したので次へ進む"):
        # ★ Fe(0.5点) / Fi(1.0点) ストッパー完全撤廃！青天井で伸びる！
        st.session_state.scores["Fe"] += st.session_state.fe_empathy * 0.5
        st.session_state.scores["Fi"] += st.session_state.fi_destroyed_count * 0.5
        add_log(f"【Fe】子犬に {st.session_state.fe_empathy}回 心を寄せた")
        add_log(f"【Fi】悪口を {st.session_state.fi_destroyed_count}個 撃ち落とした")
        next_page()

def run_p10_ne():
    st.header("🌪️ Part 10: 思考の広がり")
    st.write("『りんご』から連想するものを「、」で区切って思いつく限り入力して！")
    ans = st.text_area("ここに入力", key="ne_ans_input")
    if st.button("決定して結果を見る！"):
        st.session_state.ne_final_ans = ans 
        next_page()
