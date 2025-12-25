import streamlit as st
import google.generativeai as genai
import random

# ==========================================
# 1. 页面配置 & 样式
# ==========================================
st.set_page_config(
    page_title="MCST | UNCLE YANG",
    page_icon="🌌",
    layout="centered"
)

# --- 修复：使用 Session State 锁定随机词，防止每次点击都乱跳 ---
if "placeholders" not in st.session_state:
    raw_placeholders = {
        "date": ["1993.11", "2001.05", "1985.02", "1998.07", "1990.09"],
        "location": ["Shanghai / 上海", "London / 伦敦", "Chengdu / 成都", "Beijing / 北京"],
        "zodiac": ["Scorpio / 天蝎", "Gemini / 双子", "Dragon / 龙", "Tiger / 虎"],
    }
    st.session_state.placeholders = {
        "date": random.choice(raw_placeholders["date"]),
        "location": random.choice(raw_placeholders["location"]),
        "zodiac": random.choice(raw_placeholders["zodiac"])
    }

# CSS 样式注入 (强制高对比度 & 深色模式适配)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600&display=swap');
    
    /* 全局强制深色背景 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* 强制所有文本颜色为亮色 */
    p, label, span, div { color: #E0E0E0 !important; }

    /* 标题样式 */
    h1 {
        font-weight: 200 !important; color: #FFFFFF !important;
        letter-spacing: 3px; font-size: 2.2rem !important;
        text-transform: uppercase; text-shadow: 0 0 15px rgba(255,255,255,0.3);
    }
    h3 {
        font-weight: 300 !important; color: #B0B0B0 !important;
        font-size: 1rem !important; letter-spacing: 1px; opacity: 0.8;
    }
    
    /* 核心卡片区域 */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px); border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15); padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* 输入框样式 */
    .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important; font-weight: 500 !important;
        font-size: 14px !important; margin-bottom: 5px !important;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.6) !important; color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 8px !important;
    }
    
    /* 按钮美化 */
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #7928CA 0%, #FF0080 100%);
        color: #FFFFFF !important; border: none; border-radius: 8px; height: 55px;
        font-size: 16px; font-weight: 600; letter-spacing: 2px;
        text-transform: uppercase; box-shadow: 0 4px 15px rgba(121, 40, 202, 0.4);
        margin-top: 15px;
    }
    .stButton>button:hover {
        box-shadow: 0 8px 25px rgba(121, 40, 202, 0.8); transform: scale(1.02);
    }
    
    /* 底部品牌栏 */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(5px);
        color: #888 !important; text-align: center; padding: 12px;
        font-size: 11px; font-family: 'Courier New', monospace; letter-spacing: 2px;
        border-top: 1px solid rgba(255, 255, 255, 0.1); z-index: 999;
    }
    .brand-mark { color: #ccc !important; font-weight: bold; }
    section[data-testid="stSidebar"] { background-color: #0E1117; border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    
    <div class="footer">
        SYSTEM ARCHITECT: <span class="brand-mark">UNCLE YANG</span> · MCST METHODOLOGY
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏 & API Key 处理
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM KERNEL")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ SYSTEM ONLINE (Key Loaded)")
    else:
        api_key = st.text_input("API Key", type="password", help="Input Google Gemini API Key")
    st.markdown("---")
    st.caption("**MCST 多维轨迹系统**\n\n融合多重编码：\n- 🌐 世代地缘时空\n- 🚻 社会化性别张力\n- 🧬 认知决策架构")

# ==========================================
# 3. 核心逻辑 (Gemini 1.5 Pro)
# ==========================================
def get_mcst_analysis(user_data):
    generation_config = {
        "temperature": 0.85, "top_p": 0.95, "top_k": 40, "max_output_tokens": 8192,
    }
    model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

    system_prompt = f"""
    **SYSTEM ROLE**
    你是一位基于 MCST（Multi-Coding Symbolic Trajectory）方法论的资深分析师。
    **TONE & STYLE**
    1. **玄学与理性的交织**：使用精确的结构化语言，但用隐喻和意象来填充血肉。
    2. **极简高级感**：语言要克制、冷峻。
    3. **深度共鸣**：分析重点在于“结构性张力”和“内在矛盾”。
    4. **品牌植入**：输出最后必须标注：“Analysis generated by Uncle YANG's MCST System”。

    **INPUT DATA**
    - 时空坐标：{user_data['birth_date']} | {user_data['location']}
    - 社会角色：{user_data['gender']}
    - 文化符号：{user_data['zodiac']}
    - 生理认知：{user_data['blood_type']} 型 | {user_data['mbti']}

    **OUTPUT STRUCTURE (Markdown)**
    直接输出：
    ## 01. THE MACRO FIELD | 宏观场域
    ## 02. THE STRUCTURAL CORE | 结构内核
    ## 03. PATTERNS & TENSIONS | 循环与张力
    ## 04. TEMPORAL ANCHOR | 阶段定锚
    """
    response = model.generate_content(system_prompt)
    return response.text

# ==========================================
# 4. 主界面布局
# ==========================================
st.title("MCST TRAJECTORY")
st.markdown("### 多维符号人生轨迹系统 / Multi-Coding Symbolic Trajectory")
st.write(" ") 

with st.form("mcst_form"):
    st.write("#### 📐 INPUT PARAMETERS / 输入参数")
    st.write(" ")
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.text_input("出生年月 / Birth Date", placeholder=f"e.g. {st.session_state.placeholders['date']}")
    with col2:
        location = st.text_input("成长地 / Origin", placeholder=f"e.g. {st.session_state.placeholders['location']}")

    col3, col4 = st.columns(2)
    with col3:
        gender = st.selectbox("性别 / Gender & Social Role", ["Male / 男", "Female / 女", "Other / 其他"])
    with col4:
        zodiac = st.text_input("星座生肖 / Cultural Symbols", placeholder=f"e.g. {st.session_state.placeholders['zodiac']}")

    col5, col6 = st.columns(2)
    with col5:
        blood_type = st.selectbox("血型 / Blood Type", ["B Type", "A Type", "O Type", "AB Type", "Unknown"])
    with col6:
        mbti = st.selectbox("MBTI / Cognitive Architecture", 
                            ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                             "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"])

    st.write(" ") 
    submitted = st.form_submit_button("⚡ INITIATE SYSTEM ANALYSIS / 启动系统分析")

# ==========================================
# 5. 结果渲染
# ==========================================
if submitted:
    if not api_key:
        st.error("🔴 SYSTEM ACCESS DENIED: Please input API Key in the sidebar.")
    elif not birth_date or not location:
        # 这里把警告改成了中文，方便排查
        st.warning("⚠️ 数据不完整 (DATA INCOMPLETE): 请确保填写了出生年月和成长地。")
    else:
        user_input = {
            "birth_date": birth_date, "location": location,
            "gender": gender, "zodiac": zodiac,
            "blood_type": blood_type, "mbti": mbti
        }
        with st.spinner("🔮 Decoding spacetime symbols... 正在解构多维场域..."):
            try:
                genai.configure(api_key=api_key)
                result = get_mcst_analysis(user_input)
                st.success("Analysis Sequence Complete. / 分析完成")
                st.markdown("---")
                with st.container():
                    st.markdown(result)
            except Exception as e:
                st.error(f"🔴 SYSTEM ERROR: {e}")
