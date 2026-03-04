import streamlit as st
import math

# 設定網頁標題
st.set_page_config(page_title="SuisGarden 通寶機率計算器", layout="centered")
st.title("🎴 通寶擲骰機率計算器")

# --- 核心邏輯模塊 ---

def get_binomial_prob(n, p, k):
    """二項分佈累計機率 P(X >= k)"""
    if k <= 0: return 1.0
    if k > n: return 0.0
    return sum(math.comb(n, i) * (p**i) * ((1-p)**(n-i)) for i in range(k, n + 1))

def get_multinomial_prob(n, probs, reqs):
    """多項分佈累計機率 P(X1>=r1, X2>=r2, X3>=r3)"""
    if sum(reqs) > n: return 0.0
    p1, p2, p3 = probs
    r1, r2, r3 = reqs
    prob_sum = 0
    # 精準邊界條件優化
    for k1 in range(r1, n - r2 - r3 + 1):
        for k2 in range(r2, n - k1 - r3 + 1):
            k3 = n - k1 - k2
            coef = math.factorial(n) / (math.factorial(k1) * math.factorial(k2) * math.factorial(k3))
            prob_sum += coef * (p1**k1) * (p2**k2) * (p3**k3)
    return prob_sum

# --- UI 介面模塊 ---

mode = st.radio("選擇計算模式", ["單種錢幣 (Single)", "多種錢幣 (Multiple)"], horizontal=True)

st.divider()

# 基礎資訊輸入 (設定預設值以防啟動報錯)
col1, col2 = st.columns(2)
with col1:
    counts_input = st.text_input("擁有 [花錢 衡錢 厲錢]", value="3 4 3")
with col2:
    n = st.number_input("擲出通寶總數", min_value=1, value=3)

try:
    counts = list(map(int, counts_input.split()))
    if len(counts) != 3: st.error("請輸入 3 個數字"); st.stop()
    tot_coins = sum(counts)
    base_probs = [c / tot_coins for c in counts]
except:
    st.stop()

# --- 模式切換邏輯 ---

results = []

if "Single" in mode:
    st.subheader("單種需求設定")
    req_raw = st.text_input("需要擲出 [花錢 衡錢 厲錢]", value="1 1 1")
    requires = list(map(int, req_raw.split()))
    
    if len(requires) == 3:
        name_coins = ['花錢', '衡錢', '厲錢']
        for i in range(3):
            p = get_binomial_prob(n, base_probs[i], requires[i])
            results.append((p, f"{name_coins[i]} ({requires[i]})"))

else:
    st.subheader("多種需求組合設定")
    req_area = st.text_area("逐行輸入各組需求 (例如: 1 2 0)", value="2 1 0\n0 2 1")
    req_lines = [line.strip() for line in req_area.split('\n') if line.strip()]
    
    for i, line in enumerate(req_lines):
        try:
            req = list(map(int, line.split()))
            if len(req) == 3:
                p = get_multinomial_prob(n, base_probs, req)
                results.append((p, f"選項{i+1} (需求:{req})"))
        except:
            continue

# --- 結果顯示模塊 ---

if results:
    st.divider()
    st.subheader("📊 計算結果")
    
    for prob, label in results:
        # 使用 Progress bar 或 Metric 顯示
        st.write(f"**{label}**")
        st.progress(prob)
        st.caption(f"機率: {prob:.2%}")

    # 結論判定
    max_prob = max(p for p, l in results)
    winners = [l for p, l in results if p == max_prob]
    
    st.info("#### 💡 結論")
    if max_prob == 0:
        st.write("全部選項機率皆為 0%")
    else:
        st.write(f"最高機率選項： **{'、'.join(winners)}**")