import streamlit as st
import google.generativeai as genai
import random
import os

# ==========================================
# 1. 页面配置 & 样式
# ==========================================
st.set_page_config(
    page_title="MCST | UNCLE YANG",
    page_icon="🌌",
    layout="centered"
)

# 随机提示语库
placeholders = {
    "date": ["1993.11", "2001.05", "1985.02", "1998.07", "1990.09"],
    "location": ["Shanghai", "London", "Kyoto", "Beijing", "New York"],
    "zodiac": ["Scorpio/Snake", "Gemini/Pig", "Capricorn/Ox", "Aquarius/Tiger"],
}
ph_date = random.choice(placeholders["date"])
ph_loc = random.choice(placeholders["location"])
ph_zodiac = random.choice(placeholders["zodiac"])

# CSS 样式注入 (深色高级感)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600&display=swap');
    
    /* 全局背景：玄学深空渐变 */
    .stApp {
        background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e);
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* 标题样式 */
    h1 {
        font-weight: 200 !important;
        color: #FFFFFF !important;
        letter-spacing: 3px;
        font-size: 2.2rem !important;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    h3 {
        font-weight: 300 !important;
        color: #B0B0B0 !important;
        font-size: 1rem !important;
        letter-spacing: 1px;
    }
    
    /* 核心区域：毛玻璃卡片风格 */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* 输入框美化 */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #E0E0E0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* 按钮美化 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #7928CA 0%, #FF0080 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        height: 55px;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(121, 40, 202, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 8px 25px rgba(121, 40, 202, 0.6);
    }
    
    /* 底部品牌栏 */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(14, 17, 23, 0.8);
        backdrop-filter: blur(5px);
        color: #666;
        text-align: center;
        padding: 12px;
        font-size: 10px;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 999;
    }
    .brand-mark {
        color: #999;
        font-weight: bold;
    }
    
    /* 侧边栏调整 */
    section[data-testid="stSidebar"] {
        background-color: #12141C;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
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
    
    # 优先尝试从 Secrets 读取 Key
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ SYSTEM ONLINE (Key Loaded)")
    else:
        # 如果没有配置 Secrets，则显示输入框让用户自己填
        api_key = st.text_input("API Key", type="password", help="Input Google Gemini API Key")
        
    st.markdown("---")
    st.caption("""
    **MCST 多维轨迹系统**
    
    融合多重编码：
    - 🌐 世代地缘时空
    - 🚻 社会化性别张力
    - 🧬 认知决策架构
    
    理性的结构，诗性的解构。
    """)

# ==========================================
# 3. 核心逻辑 (Gemini 1.5 Pro)
# ==========================================
def get_mcst_analysis(user_data):
    generation_config = {
        "temperature": 0.85,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config
    )

    system_prompt = f"""
    **SYSTEM ROLE**
    你是一位基于 MCST（Multi-Coding Symbolic Trajectory）方法论的资深分析师。
    
    **TONE & STYLE**
    1. **玄学与理性的交织**：像一位量子物理学家在谈论命运。使用精确的结构化语言，但用隐喻和意象来填充血肉。
    2. **极简高级感**：语言要克制、冷峻。
    3. **深度共鸣**：分析重点在于“结构性张力”和“内在矛盾”。
    4. **品牌植入**：输出最后必须标注：“Analysis generated by Uncle YANG's MCST System”。

    **INPUT DATA**
    - 时空坐标：{user_data['birth_date']} | {user_data['location']}
    - 社会角色：{user_data['gender']}
    - 文化符号：{user_data['zodiac']}
    - 生理认知：{user_data['blood_type']} 型 | {user_data['mbti']}

    **OUTPUT STRUCTURE (Markdown)**
    不要有开场白，直接输出：
    
    ## 01. THE MACRO FIELD | 宏观场域
    (分析世代底色、地缘环境与性别角色的社会化张力)
    
    ## 02. THE STRUCTURAL CORE | 结构内核
    (结合 MBTI 与符号系统，剖析底层的决策与行动逻辑)
    
    ## 03. PATTERNS & TENSIONS | 循环与张力
    (指出人生中反复出现的结构性困境与内在拉扯，使用高级隐喻)
    
    ## 04. TEMPORAL ANCHOR | 阶段定锚
    (对当前生命阶段的哲学性建议与姿态调整)
    """
    
    response = model.generate_content(system_prompt)
    return response.text

# ==========================================
# 4. 主界面布局
# ==========================================
st.title("MCST TRAJECTORY")
st.markdown("### 多维符号人生轨迹系统 / Multi-Coding Symbolic Trajectory")
st.write(" ") 

# 使用 Form 将输入和按钮包裹在一起
with st.form("mcst_form"):
    st.write("#### 📐 INPUT PARAMETERS / 输入参数")
    st.write(" ")
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.text_input("出生年月 / Birth Date", placeholder=f"e.g. {ph_date}")
    with col2:
        location = st.text_input("成长地 / Origin", placeholder=f"e.g. {ph_loc}")

    col3, col4 = st.columns(2)
    with col3:
        gender = st.selectbox("性别 / Gender & Social Role", ["Male / 男", "Female / 女", "Other / 其他"])
    with col4:
        zodiac = st.text_input("星座生肖 / Cultural Symbols", placeholder=f"e.g. {ph_zodiac}")

    col5, col6 = st.columns(2)
    with col5:
        blood_type = st.selectbox("血型 / Blood Type", ["B Type", "A Type", "O Type", "AB Type", "Unknown"])
    with col6:
        mbti = st.selectbox("MBTI / Cognitive Architecture", 
                            ["INTJ", "INTP", "ENTJ", "ENTP", 
                             "INFJ", "INFP", "ENFJ", "ENFP",
                             "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                             "ISTP", "ISFP", "ESTP", "ESFP"])

    st.write(" ") 
    
    submitted = st.form_submit_button("⚡ INITIATE SYSTEM ANALYSIS / 启动系统分析")

# ==========================================
# 5. 结果渲染
# ==========================================
if submitted:
    if not api_key:
        st.error("🔴 SYSTEM ACCESS DENIED: Please input API Key in the sidebar.")
    elif not birth_date or not location:
        st.warning("⚠️ DATA INCOMPLETE: Critical parameters missing.")
    else:
        user_input = {
            "birth_date": birth_date,
            "location": location,
            "gender": gender,
            "zodiac": zodiac,
            "blood_type": blood_type,
            "mbti": mbti
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
