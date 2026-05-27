import streamlit as st
import os
import tomllib
from google import genai
from groq import Groq

# -------------------------------------------------------------------------
# CORE SECURITY & API KEY RESOLVER
# -------------------------------------------------------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")

if not GEMINI_KEY or not GROQ_KEY:
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        target_secrets = os.path.join(base_path, ".streamlit", "secrets.toml")
        if os.path.exists(target_secrets):
            with open(target_secrets, "rb") as file_stream:
                loaded_toml = tomllib.load(file_stream)
                GEMINI_KEY = loaded_toml.get("GEMINI_API_KEY")
                GROQ_KEY = loaded_toml.get("GROQ_API_KEY")
    except Exception:
        pass

if not GEMINI_KEY: GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GROQ_KEY: GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_KEY or not GROQ_KEY:
    st.error("🔒 Security Alert: API Keys are missing from Environment Secrets!")
    st.stop()

try:
    gemini_client = genai.Client(api_key=GEMINI_KEY)
    groq_client = Groq(api_key=GROQ_KEY)
except Exception as e:
    st.error(f"Initialization Error: Check API key formats. {e}")
    st.stop()

# -------------------------------------------------------------------------
# GEMINI STUDIO LIGHT WORKSPACE UI STYLING
# -------------------------------------------------------------------------
st.set_page_config(page_title="Intelligent Email Studio", page_icon="✉️", layout="centered")

st.markdown("""
    <style>
    /* Gemini Premium Light Theme Base */
    .stApp {
        background-color: #f4f7fa;
        color: #1e293b;
    }
    
    .gemini-header {
        font-size: 2.3rem !important;
        font-weight: 700 !important;
        color: #0f172a;
        text-align: center;
        margin-top: 1.5rem !important;
        letter-spacing: -0.5px;
    }
    
    .gemini-caption {
        text-align: center;
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    
    /* Rounded Pill Buttons (Google Style) */
    .stButton>button {
        background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
        color: white !important;
        border-radius: 24px !important;
        border: none;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1557b0 0%, #114692 100%);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.2);
    }
    
    /* Clean Cards for Structured Layout */
    .analysis-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 18px rgba(226, 232, 240, 0.4);
    }
    
    .field-section {
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 12px;
        margin-bottom: 12px;
    }
    .field-title {
        font-size: 0.88rem;
        font-weight: 600;
        color: #1a73e8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .field-content {
        font-size: 1rem;
        color: #334155;
        line-height: 1.5;
    }
    
    /* Inputs Styling */
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0;
        padding: 6px;
        border-radius: 30px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent;
        border-radius: 20px;
        color: #475569;
        font-weight: 500;
        padding: 0 22px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1a73e8 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# CORE RESILIENT BACKEND PIPELINES
# -------------------------------------------------------------------------
def analyze_email_with_fallback(email_content):
    prompt = f"""
    Analyze the following raw email accurately and extract the information matching these fields strictly. 
    If a field doesn't have any relevant content in the email, write 'None'. Do not write any conversational intro or outro text.

    Format the output exactly like this:
    [CATEGORY]: <Meetings / Work / Personal / etc.>
    [PRIORITY]: <High / Medium / Low>
    [ACTION_REQUIRED]: <Yes / No>
    [SUMMARY]: <Concise overview sentence>
    [DEADLINES_MEETINGS]: <Any deadlines or meeting schedules found>
    [KEY_NAMES]: <Names of people mentioned>
    [DATES_TIMES]: <Specific date and time metrics mentioned>
    [ASSIGNED_TASKS]: <Explicit tasks assigned to specific individuals>
    [SUGGESTED_REMINDER]: <A logical follow-up action or reminder step>

    Raw Email Content:
    {email_content}
    """
    try:
        # Tab 1 requirement asks for Gemini parsing explicitly
        response = gemini_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text, "🧠 Parsed via Gemini 2.5 Flash Engine"
    except Exception:
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content, "🔄 Gemini Load Balanced. Managed via Groq Llama 3.1 Pipeline."
        except Exception as e:
            return None, f"All production routing engines down: {e}"

def generate_draft_with_fallback(tone, recipient, sender, context):
    prompt = f"""
    You are an intelligent AI Email Assistant. Draft a highly professional email from {sender} to {recipient} based on this core intent context:
    "{context}"
    
    The tone must be strictly: {tone}. 
    Make it look natural, clear, structured, and polished. Take accountability if required, state clear timelines, and end with a proper professional signature structure.

    Output format:
    Subject: <Clear Subject Line>
    
    Dear [Recipient],
    [Body Content]
    
    Best regards,
    [Sender]
    """
    try:
        response = gemini_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text, "🧠 Generated via Gemini 2.5"
    except Exception:
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content, "🔄 Swapped to Groq Pipeline Backup"
        except Exception as e:
            return None, f"Generation failed: {e}"

def generate_reply_with_fallback(thread, intent):
    prompt = f"""
    Evaluate the following email thread context and compose a natural, contextual, non-robotic reply incorporating the user's explicit response intent directives.
    
    Received Email Thread:
    "{thread}"
    
    User Response Intent/Notes:
    "{intent}"

    Output only the final complete email response text ready to send.
    """
    try:
        response = gemini_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text, "🧠 Generated via Gemini 2.5"
    except Exception:
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content, "🔄 Swapped to Groq Pipeline Backup"
        except Exception as e:
            return None, f"Generation failed: {e}"

# -------------------------------------------------------------------------
# APPLICATION LANDING SYSTEM
# -------------------------------------------------------------------------
st.markdown("<div class='gemini-header'>✉️ Intelligent Email Studio</div>", unsafe_allow_html=True)
st.markdown("<div class='gemini-caption'>Advanced unified load routing workspace engineered for high-availability communication frameworks.</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📁 Analyze Framework", "✍️ Draft Composer", "🔄 Smart Thread Reply"])

# -------------------------------------------------------------------------
# TAB 1: EXTENDED STRUCTURAL ANALYSIS
# -------------------------------------------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    incoming_email = st.text_area(
        "Paste Incoming Raw Communication Workspace:", 
        height=180, 
        placeholder="Paste your unorganized inbox email content here...",
        key="inc_box"
    )
    
    if st.button("Analyze Email Architecture", use_container_width=True):
        if not incoming_email.strip():
            st.warning("Please paste structured email records first.")
        else:
            with st.spinner("Processing deep semantic framework..."):
                raw_output, status_msg = analyze_email_with_fallback(incoming_email)
                
                if raw_output:
                    # Parse extracted values carefully for custom key-metric design cards
                    parsed_data = {}
                    keys_to_check = [
                        "CATEGORY", "PRIORITY", "ACTION_REQUIRED", "SUMMARY", 
                        "DEADLINES_MEETINGS", "KEY_NAMES", "DATES_TIMES", 
                        "ASSIGNED_TASKS", "SUGGESTED_REMINDER"
                    ]
                    
                    for k in keys_to_check:
                        parsed_data[k] = "None"
                        
                    for line in raw_output.split('\n'):
                        for k in keys_to_check:
                            if f"[{k}]:" in line:
                                parsed_data[k] = line.split(f"[{k}]:")[1].strip()
                            elif f"{k}:" in line:
                                parsed_data[k] = line.split(f"{k}:")[1].strip()

                    # Render beautiful clean structured view output exactly matching requirements
                    st.markdown("<div class='analysis-container'>", unsafe_allow_html=True)
                    st.caption(f"✨ {status_msg}")
                    st.markdown("<h3 style='color:#0f172a; margin-bottom:1.5rem;'> Email Metadata Dashboard</h3>", unsafe_allow_html=True)
                    
                    # Core Layout Badges Row
                    col_c, col_p, col_a = st.columns(3)
                    with col_c:
                        st.markdown(f"<div class='field-title'>Category</div><div class='field-content' style='font-weight:600;'>{parsed_data['CATEGORY']}</div>", unsafe_allow_html=True)
                    with col_p:
                        p_color = "#dc2626" if "High" in parsed_data['PRIORITY'] else "#1e293b"
                        st.markdown(f"<div class='field-title'>Priority</div><div class='field-content' style='font-weight:600; color:{p_color};'>{parsed_data['PRIORITY']}</div>", unsafe_allow_html=True)
                    with col_a:
                        st.markdown(f"<div class='field-title'>Action Required</div><div class='field-content' style='font-weight:600;'>{parsed_data['ACTION_REQUIRED']}</div>", unsafe_allow_html=True)
                    
                    st.markdown("<br><hr style='border:0; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)
                    
                    # Detailed Structural Breakdowns
                    sections = [
                        ("Summary", "SUMMARY"),
                        ("Deadlines & Meetings", "DEADLINES_MEETINGS"),
                        ("Key Names Mentioned", "KEY_NAMES"),
                        ("Dates & Times Extracted", "DATES_TIMES"),
                        ("Assigned Task Node Framework", "ASSIGNED_TASKS"),
                        ("Suggested Follow-up Reminder", "SUGGESTED_REMINDER")
                    ]
                    
                    for title, key in sections:
                        st.markdown(f"""
                            <div class='field-section'>
                                <div class='field-title'>{title}</div>
                                <div class='field-content'>{parsed_data[key]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(status_msg)

# -------------------------------------------------------------------------
# TAB 2: POLISHED DRAFT COMPOSER
# -------------------------------------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    recipient = st.text_input("Recipient Identity / Designation Name:", placeholder="e.g., Dr. Andrew")
    sender = st.text_input("Your Name (Sender):", placeholder="e.g., Aqsa")
    tone = st.selectbox("Strategic Email Voice Tone dropdown:", ["formal", "apologetic", "friendly", "persuasive"])
    context = st.text_area(
        "Core Intent Input (Context Guidelines):", 
        height=120, 
        placeholder="Briefly state the raw thoughts or context behind your message..."
    )
    
    if st.button("Generate Polished Draft Workspace", use_container_width=True):
        if not context.strip():
            st.warning("Please provide core message instructions first.")
        else:
            with st.spinner("Synthesizing clear prose parameters..."):
                result, status_msg = generate_draft_with_fallback(tone, recipient, sender, context)
                if result:
                    st.markdown("<div class='analysis-container'>", unsafe_allow_html=True)
                    st.caption(f"✨ {status_msg}")
                    st.text_area("Polished Production-Ready Email Output:", value=result, height=350)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(status_msg)

# -------------------------------------------------------------------------
# TAB 3: SMART THREAD REPLY
# -------------------------------------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    thread = st.text_area(
        "Received Email Thread Logs:", 
        height=140, 
        placeholder="Paste the email thread history here..." 
    )
    intent = st.text_input(
        "Your Intended Answer / Brief Notes Directives:", 
        placeholder="e.g., Can't do 4:30, available at 6:00 PM instead." 
    )
    
    if st.button("Generate Contextual Smart Reply Node", use_container_width=True):
        if not thread.strip() or not intent.strip():
            st.warning("Both historical thread logs and targeted response notes are required.")
        else:
            with st.spinner("Assembling multi-turn dialogue vectors..."):
                result, status_msg = generate_reply_with_fallback(thread, intent)
                if result:
                    st.markdown("<div class='analysis-container'>", unsafe_allow_html=True)
                    st.caption(f"✨ {status_msg}")
                    st.text_area("Suggested Response Output:", value=result, height=250)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(status_msg)
