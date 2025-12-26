import streamlit as st
import google.generativeai as genai
import random

# ==========================================
# 1. 页面配置 & 核心样式定义
# ==========================================
st.set_page_config(
    page_title="MCST | UNCLE YANG",
    page_icon="🌙", # 换成了更温柔的月亮图标
    layout="centered"
)

# --- Session State 锁定随机词 ---
if "placeholders" not in st.session_state:
    raw_placeholders = {
        "date": ["1995.06", "2001.11", "1988.03", "1999.09", "1992.12"],
        "location": ["Shanghai / 上海", "Paris / 巴黎", "Kyoto / 京都", "Hangzhou / 杭州"],
        "zodiac": ["Cancer / 巨蟹", "Libra / 天秤", "Rabbit / 兔", "Snake / 蛇"],
    }
    st.session_state.placeholders = {
        "date": random.choice(raw_placeholders["date"]),
        "location": random.choice(raw_placeholders["location"]),
        "zodiac": random.choice(raw_placeholders["zodiac"])
    }

# --- CSS 全新轻奢风格注入 ---
st.markdown("""
    <style>
    /* 引入高级字体：Cinzel Decorative(标题装饰), Inter(正文极简) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* 全局背景：柔和的奶油米色渐变，干净通透 */
    .stApp {
        background: linear-gradient(to bottom, #FDFBFB, #F4F0EC);
        color: #4A4A4A; /* 深灰文字，比纯黑更柔和 */
        font-family: 'Inter', sans-serif;
    }
    
    /* 标题样式：使用优雅的衬线体，配合玫瑰金渐变色 */
    h1 {
        font-family: 'Cinzel Decorative', serif !important;
        background: linear-gradient(45deg, #B76E79, #D4AF37); /* 玫瑰金到香槟金 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        letter-spacing: 2px;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 10px !important;
    }
    /* 副标题 */
    h3 {
        font-family: 'Inter', sans-serif !important;
        color: #8E8E93 !important; /* 苹果风格的灰色 */
        font-size: 0.9rem !important;
        text-align: center;
        font-weight: 400 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* 核心卡片区域：苹果风格的干净白卡片，带柔和阴影 */
    [data-testid="stForm"] {
        background: #FFFFFF;
        border-radius: 24px; /* 更大的圆角，更柔和 */
        box-shadow: 0 10px 40px rgba(183, 110, 121, 0.15); /* 淡淡的玫瑰色阴影 */
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    /* 表单小标题 */
    [data-testid="stForm"] h4 {
        color: #B76E79 !important; /* 玫瑰金色 */
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-align: center;
        margin-bottom: 25px;
    }

    /* 输入框标签 */
    .stTextInput label, .stSelectbox label {
        color: #666666 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    
    /* 输入框本体：极简白底，细边框 */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #F9F9F9 !important;
        color: #333333 !important;
        border: 1px solid #E5E5EA !important; /* 苹果风格的浅灰边框 */
        border-radius: 12px !important;
        padding-left: 15px;
        transition: all 0.3s ease;
    }
    /* 输入框聚焦时的高光 */
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #B76E79 !important; /* 聚焦变成玫瑰金 */
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(183, 110, 121, 0.1);
    }
    
    /* 按钮美化：渐变胶囊按钮 */
    .stButton>button {
        width: 100%;
        /* 柔和的玫瑰金到淡紫色的渐变 */
        background: linear-gradient(135deg, #CBA475 0%, #B76E79 50%, #9E8FB2 100%);
        color: white !important;
        border: none;
        border-radius: 30px; /* 胶囊形状 */
        height: 50px;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 1px;
        box-shadow: 0 8px 20px rgba(183, 110, 121, 0.3);
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(183, 110, 121, 0.4);
    }
    
    /* 底部品牌栏：干净的浅色 */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        color: #AAAAAA; text-align: center; padding: 12px;
        font-size: 10px; font-family: 'Inter', sans-serif; letter-spacing: 1px;
        border-top: 1px solid #F0F0F0; z-index: 999;
    }
    .brand-mark { color: #B76E79 !important; font-weight: 600; }
    
    /* 侧边栏调整为浅色 */
    section[data-testid="stSidebar"] {
        background-color: #FDFBFB;
        border-right: 1px solid #F0F0F0;
    }
    section[data-testid="stSidebar"] h3 { color: #333 !important; text-align: left; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] li { color: #666 !important; }
    
    /* 分析结果区域的美化 */
    .stSuccess {
        background-color: rgba(183, 110, 121, 0.1) !important;
        border: none !important;
        color: #B76E79 !important;
        border-radius: 12px;
    }
    /* Markdown 结果标题 */
    h2 {
        font-family: 'Cinzel Decorative', serif !important;
        color: #B76E79 !important;
        font-size: 1.4rem !important;
        margin-top: 30px !important;
        border-bottom: 2px solid rgba(183, 110, 121, 0.2);
        padding-bottom: 10px;
    }
    </style>
    
    <div class="footer">
        Created with ✨ by <span class="brand-mark">Uncle YANG</span> | MCST System
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏 & API Key 处理
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ 设置 / Settings")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key 已加载 / Loaded")
    else:
        api_key = st.text_input("请输入 Google API Key", type="password")
    st.markdown("---")
    st.markdown("### 关于系统")
    st.caption("""
    **MCST 多维轨迹系统 (Venus Edition)**
    
    融合感性与理性的深度洞察。
    解构你的时空、角色与内在光芒。
    
    *Designed for the awaken soul.*
    """)

# ==========================================
# 3. 核心逻辑 (Gemini 2.5 Flash - 最快最稳)
# ==========================================
def get_mcst_analysis(user_data):
    generation_config = {
        "temperature": 0.85, "top_p": 0.95, "top_k": 40, "max_output_tokens": 8192,
    }
    # 使用最稳的 2.5 Flash 模型
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", generation_config=generation_config)

    system_prompt = f"""
    **SYSTEM ROLE**
    你是一位基于 MCST 方法论的资深人生分析师，专注于为女性用户提供深度、温暖且富有启发性的洞察。
    
    **TONE & STYLE (重要)**
    1.  **温暖而有力**：像一位充满智慧的姐姐或导师，语言要优雅、细腻，富有同理心，避免过于冷硬的学术词汇。
    2.  **神秘感与治愈感**：适当使用一些富有灵性的隐喻（如星辰、海洋、花园、能量），但落脚点必须是现实的建议。
    3.  **极简高级**：段落清晰，金句频出。
    4.  **品牌植入**：输出最后必须标注：“✨ Analysis created by Uncle YANG's MCST System”。

    **INPUT DATA**
    - 时空坐标：{user_data['birth_date']} | {user_data['location']}
    - 社会角色：{user_data['gender']}
    - 文化符号：{user_data['zodiac']}
    - 生理认知：{user_data['blood_type']} 型 | {user_data['mbti']}

    **OUTPUT STRUCTURE (Markdown)**
    直接输出以下结构，不要有开场白：
    
    ## 🌸 01. THE MACRO FIELD | 你的世代与花园
    (分析她所处的时代背景与成长土壤，如何塑造了她独特的底色。侧重于环境给予的滋养与挑战。)
    
    ## 💫 02. THE INNER CONSTELLATION | 内在星系与内核
    (结合 MBTI 与符号系统，解读她性格中最耀眼的光芒和潜在的能量模式。强调她的天赋。)
    
    ## 🌊 03. TIDES & PATTERNS | 生命潮汐与张力
    (温柔地指出她人生中可能反复出现的课题、情感模式或内在拉扯，并提供化解的视角。)
    
    ## ✨ 04. TEMPORAL ANCHOR | 当下定锚与祝福
    (针对她当前阶段给予哲学性的建议、行动指引和一句充满力量的祝福。)
    """
    response = model.generate_content(system_prompt)
    return response.text

# ==========================================
# 4. 主界面布局
# ==========================================
# 标题使用两行，营造杂志感
st.title("MCST TRAJECTORY")
st.markdown("### 多维符号人生轨迹系统 · 维纳斯版")
st.write(" ") 

with st.form("mcst_form"):
    st.markdown("#### ✧ 开始你的探索旅程 ✧")
    st.write(" ")
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.text_input("出生年月 (Birth Date)", placeholder=f"e.g. {st.session_state.placeholders['date']}")
    with col2:
        location = st.text_input("成长地 (Origin)", placeholder=f"e.g. {st.session_state.placeholders['location']}")

    col3, col4 = st.columns(2)
    with col3:
        gender = st.selectbox("性别 / 社会角色 (Role)", ["Female / 女", "Male / 男", "Other / 其他"])
    with col4:
        zodiac = st.text_input("星座生肖 (Symbols)", placeholder=f"e.g. {st.session_state.placeholders['zodiac']}")

    col5, col6 = st.columns(2)
    with col5:
        blood_type = st.selectbox("血型 (Blood Type)", ["B Type", "A Type", "O Type", "AB Type", "Unknown"])
    with col6:
        mbti = st.selectbox("MBTI (Cognition)", 
                            ["INFJ", "INFP", "ENFJ", "ENFP", "INTJ", "INTP", "ENTJ", "ENTP", 
                             "ISFJ", "ESFJ", "ISTJ", "ESTJ", "ISFP", "ESFP", "ISTP", "ESTP"])

    st.write(" ") 
    # 按钮文字加了Emoji
    submitted = st.form_submit_button("✨ 解读我的生命轨迹 / Start Analysis")

# ==========================================
# 5. 结果渲染
# ==========================================
if submitted:
    if not api_key:
        st.error("请先在侧边栏设置 API Key。")
    elif not birth_date or not location:
        st.warning("⚠️ 为了获得准确解读，请至少填写「出生年月」和「成长地」。")
    else:
        user_input = {
            "birth_date": birth_date, "location": location,
            "gender": gender, "zodiac": zodiac,
            "blood_type": blood_type, "mbti": mbti
        }
        # 加载动画的文字也改得更温柔了
        with st.spinner("💫 正在连接时空场域，感知你的独特能量..."):
            try:
                genai.configure(api_key=api_key)
                result = get_mcst_analysis(user_input)
                # 成功提示条
                st.success("解读完成，属于你的生命画卷已展开。")
                st.markdown("---")
                with st.container():
                    st.markdown(result)
            except Exception as e:
                st.error(f"系统繁忙，请稍后再试: {e}")
