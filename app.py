import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ---------------------------
# 🔧 CONFIGURATION
# ---------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------------------
# 🎨 STREAMLIT PAGE SETTINGS
# ---------------------------
st.set_page_config(
    page_title="GenAI Incident Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# 🧩 SIDEBAR (Theme + Settings)
# ---------------------------
st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("Customize your AI assistant's behavior below:")

assistant_role = st.sidebar.selectbox(
    "Choose Assistant Mode:",
    ["SRE Expert", "Cloud Engineer", "DevOps Mentor", "Linux Troubleshooter"]
)

tone = st.sidebar.selectbox(
    "Response Tone:",
    ["Professional", "Detailed", "Concise"]
)

st.sidebar.markdown("---")
theme = st.sidebar.radio("🎨 Theme", ["Light 🌞", "Dark 🌙"])

# ---------------------------
# 🌈 CUSTOM PAGE STYLING
# ---------------------------
if theme == "Dark 🌙":
    st.markdown("""
        <style>
        /* ======== Global App Background ======== */
        .stApp {
            background-color: #0b0f1a !important;
            color: #f5f5f5 !important;
        }

        /* ======== Main Text Styling ======== */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stTextInput, .stSelectbox label, .stRadio label {
            color: #f5f5f5 !important;
        }

        /* ======== Sidebar Styling ======== */
        section[data-testid="stSidebar"] {
            background-color: #111728 !important;
            color: #f5f5f5 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #f5f5f5 !important;
        }

        /* Sidebar Inputs (Dropdowns, Radios, etc.) */
        .stSelectbox div[data-baseweb="select"],
        .stRadio,
        .stTextInput input {
            background-color: #1a1f2e !important;
            color: #f5f5f5 !important;
            border: 1px solid #3949ab !important;
        }

        /* ======== Input & TextArea ======== */
        textarea, .stTextInput input {
            background-color: #1a1f2e !important;
            border: 1px solid #5c6bc0 !important;
            color: #ffffff !important;
            caret-color: #00eaff !important; /* bright cyan cursor */
        }

        /* ======== Buttons ======== */
        .stButton button {
            background: linear-gradient(90deg, #2196f3, #00bcd4) !important;
            color: #ffffff !important;
            border-radius: 8px;
            border: none !important;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #42a5f5, #26c6da) !important;
            transform: scale(1.02);
        }

        /* ======== Scrollbar ======== */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: #3949ab;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #5c6bc0;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8fafc !important;
            color: #2c3e50 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ---------------------------
# 🧠 PAGE HEADER
# ---------------------------
st.markdown("""
    <h1 style='text-align:center; font-size:40px; font-weight:700; color:#2c3e50;'>🧠 GenAI Incident Assistant</h1>
    <p style='text-align:center; font-size:18px; color:#555;'>AI-powered tool to help DevOps & SRE teams troubleshoot faster ⚡</p>
""", unsafe_allow_html=True)

st.markdown(
    f"<div style='text-align:center; font-size:16px;'>Current Theme: {'🌙 Dark Mode' if theme == 'Dark 🌙' else '🌞 Light Mode'}</div>",
    unsafe_allow_html=True
)

# ---------------------------
# 💬 USER INPUT
# ---------------------------
user_input = st.text_area(
    "🔍 Describe the incident or issue:",
    placeholder="Example: Our Kubernetes pods are stuck in CrashLoopBackOff after a new deployment..."
)

# ---------------------------
# 🚀 GENERATE RESPONSE
# ---------------------------
if st.button("Generate AI Response 🚀"):
    if not user_input.strip():
        st.warning("⚠️ Please describe the issue first!")
    else:
        with st.spinner("Analyzing incident and generating insights..."):
            try:
                # Construct the prompt
                prompt = f"""
                You are acting as a {assistant_role} with expertise in troubleshooting production issues.
                The tone of your response should be {tone.lower()}.
                Analyze the incident below, identify possible causes, and provide
                actionable troubleshooting steps. Include Linux commands, monitoring strategies,
                and best practices if relevant.

                Incident Description:
                {user_input}
                """

                response = model.generate_content(prompt)

                # 🎯 Display AI response
                st.subheader("🧩 Suggested Resolution:")
                st.markdown(response.text)

                # 💾 Save incident log
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("incident_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[Time]: {timestamp}\n[Role]: {assistant_role}\n[User Input]: {user_input}\n[Response]: {response.text}\n{'-'*80}\n")

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------------------------
# 📈 FUTURE ENHANCEMENTS
# ---------------------------
with st.expander("📈 Future Enhancement Ideas"):
    st.markdown("""
    - Integration with **Prometheus/Grafana** for real-time alert data  
    - Root cause probability scoring  
    - Automated runbook generation  
    - Slack or PagerDuty integration  
    - Multi-cloud diagnostic plugin
    """)

# ---------------------------
# 🗂️ LOG VIEWER
# ---------------------------
with st.expander("🗂️ View Past Logs"):
    try:
        with open("incident_log.txt", "r", encoding="utf-8") as log:
            st.text(log.read())
    except FileNotFoundError:
        st.info("No logs yet. Generate a response first!")

# ---------------------------
# 📜 FOOTER
# ---------------------------
st.markdown(
    '<div style="text-align:center; margin-top:40px; color:gray;">💻 Built by <b>Suhana Shaik</b> — Exploring AI-driven automation for SRE workflows.</div>',
    unsafe_allow_html=True
)
