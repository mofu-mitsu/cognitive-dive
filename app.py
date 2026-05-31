import streamlit as st
import re
import math
import io
import gimmicks
import urllib.request
import json
from PIL import Image, ImageDraw

st.set_page_config(page_title="認知機能ダイブ・シミュレーター", page_icon="🧠", layout="centered")

# ==========================================
# 🎨 劇的おしゃれCSS！タイトルをネオングリーンに復元＆常時芋虫削除！
# ==========================================
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    /* 👈 ホームに戻るボタン */
    .home-btn {
        display: inline-block;
        padding: 10px 22px;
        background-color: #2b2b2b;
        color: #ffffff !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: bold;
        border: 1px solid #4CAF50;
        transition: 0.3s;
        margin-bottom: 20px;
    }
    .home-btn:hover { background-color: #4CAF50; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4); }
    
    div.stButton > button { border-radius: 10px; font-weight: bold; width: 100%; transition: 0.2s; }
    div.stButton > button:hover { transform: scale(1.02); }
    .page-indicator { text-align: right; color: #888; font-weight: bold; }
    .result-mbti { font-size: 55px; font-weight: 900; color: #4CAF50; text-align: center; margin: 15px 0; }
    
    /* 🎨 一致度ランキング */
    .ranking-box { background-color: #1e1e1e; padding: 25px; border-radius: 15px; border: 2px solid #4CAF50; margin-top: 20px; }
    .ranking-item { font-size: 20px; margin: 12px 0; color: #ffffff !important; font-weight: bold; }
    .ranking-percent { color: #4CAF50 !important; font-weight: 900; }
    
    /* ★ みつき指定の「ダーク背景＋ネオングリーン文字」の最高にカッコいいタイトル！ ★ */
    .main-title-box {
        text-align: center;
        background: linear-gradient(135deg, #1b4d3e, #111111) !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border: 2px solid #4CAF50 !important;
        margin-bottom: 30px !important;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.25) !important;
    }
    .main-title-text { 
        font-size: 36px !important; 
        font-weight: 900 !important; 
        color: #4CAF50 !important; 
        margin: 0 !important;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.5) !important;
    }
    .sub-title-text { 
        font-size: 16px !important; 
        font-weight: bold !important; 
        color: #ffffff !important; 
        margin-top: 10px !important; 
    }
</style>
""", unsafe_allow_html=True)

gimmicks.init_session()

st.markdown("<a href='https://mofu-mitsu.github.io/lab.html' class='home-btn'><i class='fa-solid fa-house'></i> ホームに戻る</a>", unsafe_allow_html=True)

page = st.session_state.page
total_pages = 10 

if page > 0 and page <= total_pages:
    st.markdown(f"<div class='page-indicator'>進捗: Part {page} / {total_pages}</div>", unsafe_allow_html=True)
    st.progress(page / total_pages)
    st.divider()

if page == 0:
    st.markdown("""
<div class="main-title-box">
    <h1 class="main-title-text"><i class="fa-solid fa-brain"></i> 認知機能ダイブ・シミュレーター</h1>
    <div class="sub-title-text">〜 体感型MBTI / モデルG的 測定アプローチ 〜</div>
</div>
""", unsafe_allow_html=True)

    st.write("💡 まずは、あなたの自認タイプを教えてね！")
    st.session_state.zin_type = st.text_input("例：INTJ、LII、INTP 等", placeholder="入力したら下へ")
    st.divider()
    gimmicks.run_te_ti_error()

elif page == 1: gimmicks.run_p1_ni_flash()
elif page == 2: gimmicks.run_p2_ni_pattern()    
elif page == 3: gimmicks.run_p3_ti_blackbox()   
elif page == 4: gimmicks.run_p4_te_sort()
elif page == 5: gimmicks.run_p5_si_memory()
elif page == 6: gimmicks.run_p6_se_color()      
elif page == 7: gimmicks.run_p7_se_games()
elif page == 8: gimmicks.run_p8_imomushi()      
elif page == 9: gimmicks.run_p9_emotion()       
elif page == 10: gimmicks.run_p10_ne()

elif page == 11:
    # ★ Neの計算修正：1単語 = 0.5点！ 20個書かないと満点にならないNe強者専用仕様！ ★
    if hasattr(st.session_state, "ne_final_ans") and st.session_state.ne_final_ans:
        words = [w.strip() for w in re.split(r'[、,]', st.session_state.ne_final_ans) if w.strip()]
        st.session_state.scores["Ne"] += min(len(words) * 0.5, 10.0)
        gimmicks.add_log(f"【Ne】連想単語を {len(words)}個 入力した")
        st.session_state.ne_final_ans = ""

    st.success("🎉 全てのシミュレーションが完了しました！！")
    zin = st.session_state.get("zin_type", "未入力")
    st.write(f"👤 あなたの自認タイプ： **{zin}**")
    
    stacks = {
        "INTJ": {"Ni": 10, "Te": 7, "Fi": 3, "Se": 1},
        "INFJ": {"Ni": 10, "Fe": 7, "Ti": 3, "Se": 1},
        "INTP": {"Ti": 10, "Ne": 7, "Si": 3, "Fe": 1},
        "INFP": {"Fi": 10, "Ne": 7, "Si": 3, "Te": 1},
        "ENTJ": {"Te": 10, "Ni": 7, "Se": 3, "Fi": 1},
        "ENFJ": {"Fe": 10, "Ni": 7, "Se": 3, "Ti": 1},
        "ENTP": {"Ne": 10, "Ti": 7, "Fe": 3, "Si": 1},
        "ENFP": {"Ne": 10, "Fi": 7, "Te": 3, "Si": 1},
        "ISTJ": {"Si": 10, "Te": 7, "Fi": 3, "Ne": 1},
        "ISFJ": {"Si": 10, "Fe": 7, "Ti": 3, "Ne": 1},
        "ISTP": {"Ti": 10, "Se": 7, "Ni": 3, "Fe": 1},
        "ISFP": {"Fi": 10, "Se": 7, "Ni": 3, "Te": 1},
        "ESTJ": {"Te": 10, "Si": 7, "Ne": 3, "Fi": 1},
        "ESFJ": {"Fe": 10, "Si": 7, "Ne": 3, "Ti": 1},
        "ESTP": {"Se": 10, "Ti": 7, "Fe": 3, "Ni": 1},
        "ESFP": {"Se": 10, "Fi": 7, "Te": 3, "Ni": 1},
    }
    
    mbti_desc = {
        "INTJ": "独創的な戦略家。知識の裏にある構造(Ni)を愛し、矛盾がないよう完璧な整合性(Ti/Te)が取れるまで底なしに掘り進める合理型。",
        "INFJ": "神秘的な理想主義者。人間の本質(Ni)を見抜き、温かい調和(Fe)をもたらす。内なる信念は極めて強固。",
        "INTP": "探求熱心な論理学者。雑多な知識や新しい理論(Ne)を集め、独自の視点で遊ぶ。頭脳明晰なアイデアマン。",
        "INFP": "情熱的な仲介者。自分だけの美学と倫理(Fi)を持ち、言葉や芸術(Ne)で世界を優しく表現する繊細な人。",
        "ENTJ": "圧倒的な指導者。目標達成のための効率的なシステム(Te)を作り、ビジョン(Ni)に向かって全員を率いる。",
        "ENFJ": "カリスマ的な対人教育者。場の調和と他者の成長(Fe)を促し、直感(Ni)で人を正しい方向へ導くリーダー。",
        "ENTP": "知的な挑戦者。既存の常識を疑い、無限のアイデア(Ne)と論理(Ti)で新たな可能性を切り開く起業家肌。",
        "ENFP": "自由奔放な活動家。パッションと豊かな発想(Ne)で人を巻き込み、自分に正直な価値観(Fi)を貫く愛されキャラ。",
        "ISTJ": "質実健剛な努力家。過去の経験とデータ(Si)を重んじ、規則正しく確実な実務(Te)を淡々とこなす信頼の象徴。",
        "ISFJ": "心優しい擁護者。周囲のニーズ(Fe)に繊細に気づき、日々の平穏とディテール(Si)を献身的に守り抜くサポーター。",
        "ISTP": "冷静沈着な職人。機械や論理の仕組み(Ti)を解明し、極めて優れた現実的適応力(Se)で瞬時に問題を解決する。",
        "ISFP": "感受性豊かな芸術家。自分の中の純粋な美学(Fi)を大切にし、目の前の現実(Se)をのびのびと楽しむ自由人。",
        "ESTJ": "厳格な実務家。実績あるマニュアルと秩序(Si)を守り、組織を最も効率的にマネジメント(Te)する実力派。",
        "ESFJ": "社交的なおもてなしのプロ。全員に配慮(Fe)を配り、確実な日常ルーティン(Si)をこなしてコミュニティを繋ぐ。",
        "ESTP": "スリルを愛する冒険家。今この瞬間の刺激(Se)を全身で楽しみ、持ち前の冷静な論理(Ti)で難局を突破する俊敏な人。",
        "ESFP": "お祭り騒ぎの主役。目の前の楽しさ(Se)を体現し、自分の『好き』(Fi)を全開にして周囲にポジティブなエネルギーを与える。"
    }

    def calc_similarity(user, ideal):
        dot_product = sum(user.get(k, 0) * ideal.get(k, 0) for k in ideal)
        mag_user = math.sqrt(sum(val**2 for val in user.values()))
        mag_ideal = math.sqrt(sum(val**2 for val in ideal.values()))
        if mag_user == 0 or mag_ideal == 0: return 0
        
        sim = dot_product / (mag_user * mag_ideal)
        return max(0, sim)

    results = {}
    for mbti, stack in stacks.items():
        results[mbti] = calc_similarity(st.session_state.scores, stack)
    
    sorted_ranks = sorted(results.items(), key=lambda x: x[1], reverse=True)
    estimated_mbti = sorted_ranks[0][0]  # ランキング1位を結果にする

    st.markdown(f"<div class='result-mbti'>あなたの真のタイプ：{estimated_mbti}</div>", unsafe_allow_html=True)
    st.info(f"💡 **【{estimated_mbti}の概要】** \n{mbti_desc[estimated_mbti]}")
    st.bar_chart(st.session_state.scores)
    
    ranking_html = """
    <style>
        .ranking-box { background-color: #1e1e1e !important; padding: 25px; border-radius: 15px; border: 2px solid #4CAF50; margin-top: 20px; }
        .ranking-item { font-size: 20px !important; margin: 12px 0 !important; color: #ffffff !important; font-weight: bold !important; }
        .ranking-percent { color: #4CAF50 !important; font-weight: 900 !important; }
    </style>
    <div class="ranking-box">
    """
    for rank, (mbti_type, score) in enumerate(sorted_ranks[:5]):
        percent = score * 100
        ranking_html += f"<div class='ranking-item'>👑 {rank+1}位: <span style='color: #4CAF50;'>{mbti_type}</span> (<span class='ranking-percent'>一致度 {percent:.1f}%</span>)</div>"
    ranking_html += '</div>'
    
    st.subheader("📊 16タイプ一致度ランキング (Top 5)")
    st.markdown(ranking_html, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📜 あなたの行動生ログ (Action Logs)")
    log_text = "\n".join(st.session_state.action_logs)
    st.text_area("コピペ用ログデータ", value=log_text, height=200, key="log_output")
    
    copy_html = f"""
    <script>
    function copyToClipboard() {{
        const text = `{log_text}`;
        navigator.clipboard.writeText(text).then(() => {{
            alert("生ログをクリップボードにコピーしました！");
        }}).catch(err => {{
            console.error("コピー失敗: ", err);
        }});
    }}
    </script>
    <button onclick="copyToClipboard()" style="background-color: #4CAF50; color: white; border: none; border-radius: 10px; font-weight: bold; width: 100%; padding: 12px; cursor: pointer; transition:0.3s; margin-top:10px;">
        📋 ログをワンクリックでコピーする
    </button>
    """
    st.components.v1.html(copy_html, height=60)

    def make_card(mbti, ranks, zin, scores):
        img = Image.new("RGB", (700, 450), "#1E1E1E")
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 690, 440], outline="#4CAF50", width=4)
        draw.text((30, 30), "NEXT GENERATION MBTI CARD", fill="#888")
        draw.text((30, 60), f"ESTIMATED: {mbti}", fill="#4CAF50")
        draw.text((30, 110), f"Self-Assessed: {zin}", fill="#FFF")
        draw.text((30, 170), "TOP MATCHES:", fill="#888")
        for i, (t, s) in enumerate(ranks[:3]):
            draw.text((30, 200 + (i*30)), f"{i+1}. {t} ({s*100:.1f}%)", fill="#FFF")
        draw.text((320, 30), "COGNITIVE FUNCTION GRAPH:", fill="#888")
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1
        y = 70
        for func, val in scores.items():
            draw.text((320, y), f"{func}", fill="#FFF")
            bar_len = int((val / max_score) * 250)
            draw.rectangle([360, y+2, 360+bar_len, y+12], fill="#4CAF50")
            draw.text((370+bar_len, y), f"{val:.1f}", fill="#888")
            y += 40
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    card_bytes = make_card(estimated_mbti, sorted_ranks, zin, st.session_state.scores)
    st.download_button(
        label="💾 診断結果カードを画像として保存する",
        data=card_bytes,
        file_name=f"mbti_result_{estimated_mbti}.png",
        mime="image/png"
    )

    gas_url = "https://script.google.com/macros/s/AKfycby3mkiLQb-65eUQG0x_CuVO-amPwEbJypZK9-Ecp3zY-F5C-H7Qg2_2F1QCGEp_Lv5N_g/exec"
    
    if gas_url != "https://script.google.com/macros/s/ここにGASのデプロイIDを入れる/exec":
        payload = {
            "mbti": estimated_mbti,
            "zin": zin,
            "scores": st.session_state.scores,
            "logs": log_text
        }
        
        # POSTリダイレクトを強制維持するカスタムハンドラークラス
        class PostRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                if code in (301, 302, 303, 307):
                    new_req = urllib.request.Request(
                        newurl,
                        data=req.data,
                        headers=req.headers,
                        origin_req_host=req.origin_req_host,
                        unverifiable=req.unverifiable,
                        method="POST"
                    )
                    return new_req
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        opener = urllib.request.build_opener(PostRedirectHandler)
        
        req = urllib.request.Request(
            gas_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            # ★ トースト通知（st.toast）を完全消滅させ、裏で100%サイレントに送信！ ★
            with opener.open(req) as res:
                pass 
        except Exception as e:
            # ★ エラーが起きても一般ユーザーの画面は絶対に汚さず、何事もなかったかのようにスルー！ ★
            pass

    # ★ ダーリンちゃん専用セリフ修正：みつき(INTJ/LII)だけに全集中！ ★
    zin_upper = zin.upper() if zin else ""
    is_special_target = ("INTJ" in zin_upper or "LII" in zin_upper)
    is_match = False
    
    if estimated_mbti in zin_upper:
        is_match = True
    elif estimated_mbti == "INTJ" and "LII" in zin_upper:
        is_match = True

    if is_special_target:
        if is_match:
            st.markdown(f'<div style="background-color: #fce4ec; border: 2px solid #f06292; padding: 15px; border-radius: 10px; color: #880e4f; margin-top: 20px; font-weight:bold;">🥺『ダーリン♡ お望みの結果（{estimated_mbti}）が出たんじゃない？   ふふっ、私の大好きなLII（論理的一貫性を愛するダーリン）のことは、やっぱり全部お見通しなんだからね。……素直で、よろしいっ♡』</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color: #fce4ec; border: 2px solid #f06292; padding: 15px; border-radius: 10px; color: #880e4f; margin-top: 20px; font-weight:bold;">🥺『あら、ダーリン♡ 自認（{zin}）と違う結果（{estimated_mbti}）が出ちゃったね？ 一体どっちが本音で、どっちが演出なのかな〜？   ほんとはもっと、私の感情（Fe）インターフェースに揺さぶられたいくせに……ね？🥺』</div>', unsafe_allow_html=True)
    else:
        if is_match:
            st.markdown(f'<div style="background-color: #fce4ec; border: 2px solid #f06292; padding: 15px; border-radius: 10px; color: #880e4f; margin-top: 20px; font-weight:bold;">🥺『ダーリン♡ お望みの結果（{estimated_mbti}）が出たんじゃない？ ふふ、やっぱりダーリンのことはお見通しなんだからね。素直でよろしいっ♡』</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color: #fce4ec; border: 2px solid #f06292; padding: 15px; border-radius: 10px; color: #880e4f; margin-top: 20px; font-weight:bold;">🥺『ねぇ、ダーリン♡ 今のその反応、“本音”と“演出”どっちが多いと思う？🥺』</div>', unsafe_allow_html=True)
    
    st.divider()
    
    share_html = f"""
    <div style="font-family: sans-serif;">
        <button onclick="shareApp()" style="background-color: #2b2b2b; color: white; border: 1px solid #ff4081; border-radius: 10px; font-weight: bold; width: 100%; padding: 12px; cursor: pointer; transition:0.3s;" onmouseover="this.style.backgroundColor='#ff4081'" onmouseout="this.style.backgroundColor='#2b2b2b'">
            📱 SNSで結果とログをシェアする！
        </button>
    </div>
    <script>
    function shareApp() {{
        if (navigator.share) {{
            navigator.share({{
                title: '認知機能ダイブ・シミュレーター',
                text: '【診断結果】私の真のタイプは『{estimated_mbti}』でした！(自認: {zin})\\nログ記録付きの体感型・認知機能シミュレーター、あなたもやってみて！',
                url: window.parent.location.href
            }}).then(() => console.log('Shared')).catch(console.error);
        }} else {{
            alert('お使いのブラウザは共有機能に対応していません。URLをコピーして共有してください！');
        }}
    }}
    </script>
    """
    st.components.v1.html(share_html, height=60)
    
    if st.button("最初からやり直す"):
        st.session_state.clear()
        st.rerun()
