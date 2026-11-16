
import streamlit as st
from openai import OpenAI
import base64
import config
from rag_engine import FarmerRAG

# 1. Page setup
st.set_page_config(
    page_title="Namma Vivasayam",
    page_icon="🌾",
    layout="wide"
)

if not config.OPENAI_API_KEY:
    st.error("Please add your OpenAI API key in .env")
    st.stop()

@st.cache_resource
def load_rag():
    return FarmerRAG()

with st.spinner("🌾 Loading Namma Vivasayam..."):
    rag = load_rag()

client = OpenAI(api_key=config.OPENAI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "scheme_answer" not in st.session_state:
    st.session_state.scheme_answer = ""

if "faq_answer" not in st.session_state:
    st.session_state.faq_answer = ""

# 2. English and Tamil translations
translations = {
    "English": {
        "title": "Namma Vivasayam",
        "subtitle": "Your Farmer Welfare Assistant – Tamil Nadu",
        "banner": "Vanakkam! Welcome to Namma Vivasayam",
        "agriculture": "Agriculture",
        "schemes": "Learn about schemes",
        "subsidies": "Subsidies",
        "financial": "Get financial support",
        "assistant": "AI Assistant",
        "ask_language": "Ask in your language",
        "upload": "Add Farmer Schemes",
        "upload_caption": "Upload Tamil Nadu farmer scheme PDFs.",
        "upload_pdf": "Upload scheme PDFs",
        "add": "Add Schemes",
        "documents": "Uploaded Documents",
        "no_documents": "No indexed documents yet.",
        "about": "About Namma Vivasayam",
        "about_text": "Your AI assistant for Tamil Nadu agriculture and farmer welfare schemes.",
        "clear": "Clear Chat",
        "chat": "Chat",
        "faq": "FAQ",
        "welcome": "Welcome to Namma Vivasayam!",
        "ask": "Ask questions about Tamil Nadu farmer schemes.",
        "suggested": "Suggested Questions",
        "type": "Type your farming question...",
        "voice": "Ask using your voice",
        "submit_voice": "Submit Voice Question",
        "faq_title": "Frequently Asked Questions",
        "guide": "Quick Guide",
        "guide_caption": "Choose your farming requirement.",
        "choose": "Choose your need",
        "find": "Find Schemes",
        "popular": "Popular Schemes",
        "select_pdf": "Please select PDF files.",
        "select_scheme": "Please select a scheme.",
        "finding": "Finding answer...",
        "searching": "Searching PDF documents...",
        "processing_voice": "Understanding voice...",
        "crop": "Crop Insurance",
        "seed": "Seed Subsidy",
        "machinery": "Farm Machinery",
        "irrigation": "Irrigation Support",
        "footer": "Farmers Prosper, Tamil Nadu Grows"
    },
    "தமிழ்": {
        "title": "நம்ம விவசாயம்",
        "subtitle": "தமிழ்நாடு விவசாயிகள் நல உதவியாளர்",
        "banner": "வணக்கம்! நம்ம விவசாயத்திற்கு வரவேற்கிறோம்",
        "agriculture": "விவசாயம்",
        "schemes": "அரசுத் திட்டங்களை அறியுங்கள்",
        "subsidies": "மானியங்கள்",
        "financial": "நிதி உதவி பெறுங்கள்",
        "assistant": "AI உதவியாளர்",
        "ask_language": "உங்கள் மொழியில் கேளுங்கள்",
        "upload": "விவசாயத் திட்டங்களைச் சேர்க்கவும்",
        "upload_caption": "தமிழ்நாடு விவசாயத் திட்ட PDF கோப்புகளைப் பதிவேற்றவும்.",
        "upload_pdf": "திட்ட PDF கோப்புகளைப் பதிவேற்றவும்",
        "add": "திட்டங்களைச் சேர்க்கவும்",
        "documents": "பதிவேற்றப்பட்ட ஆவணங்கள்",
        "no_documents": "ஆவணங்கள் எதுவும் இல்லை.",
        "about": "நம்ம விவசாயம் பற்றி",
        "about_text": "தமிழ்நாடு விவசாயம் மற்றும் நலத்திட்டங்களுக்கான AI உதவியாளர்.",
        "clear": "உரையாடலை அழிக்கவும்",
        "chat": "உரையாடல்",
        "faq": "கேள்விகள்",
        "welcome": "நம்ம விவசாயத்திற்கு வரவேற்கிறோம்!",
        "ask": "தமிழ்நாடு விவசாயத் திட்டங்கள் பற்றி கேளுங்கள்.",
        "suggested": "பரிந்துரைக்கப்பட்ட கேள்விகள்",
        "type": "உங்கள் விவசாயக் கேள்வியை எழுதுங்கள்...",
        "voice": "குரல் மூலம் கேளுங்கள்",
        "submit_voice": "குரல் கேள்வியை அனுப்பவும்",
        "faq_title": "அடிக்கடி கேட்கப்படும் கேள்விகள்",
        "guide": "விரைவு வழிகாட்டி",
        "guide_caption": "உங்கள் விவசாயத் தேவையைத் தேர்ந்தெடுக்கவும்.",
        "choose": "உங்கள் தேவையைத் தேர்ந்தெடுக்கவும்",
        "find": "திட்டங்களைத் தேடுங்கள்",
        "popular": "பிரபலமான திட்டங்கள்",
        "select_pdf": "PDF கோப்புகளைத் தேர்ந்தெடுக்கவும்.",
        "select_scheme": "ஒரு திட்டத்தைத் தேர்ந்தெடுக்கவும்.",
        "finding": "பதிலைத் தேடுகிறது...",
        "searching": "ஆவணங்களில் தேடுகிறது...",
        "processing_voice": "குரலைப் புரிந்துகொள்கிறது...",
        "crop": "பயிர் காப்பீடு",
        "seed": "விதை மானியம்",
        "machinery": "விவசாய இயந்திரங்கள்",
        "irrigation": "நீர்ப்பாசன உதவி",
        "footer": "விவசாயிகள் வளர்ச்சி, தமிழ்நாட்டின் முன்னேற்றம்"
    }
}

language = st.session_state.language
t = translations[language]

# 3. Styling
st.markdown("""
<style>
.stApp {
    background: #f5f9f1;
}
.block-container {
    max-width: 1500px;
    padding-top: 3.5rem;
    padding-bottom: 1rem;
}
h1, h2, h3 {
    color: #105331;
}
div.stButton > button {
    border-radius: 12px;
    border: 1px solid #c4dec6;
}
div.stButton > button[kind="primary"] {
    background: #176b37;
    color: white;
    border-color: #176b37;
}
.card {
    background: white;
    padding: 14px;
    border: 1px solid #dce8d8;
    border-radius: 14px;
    text-align: center;
}
.card b {
    color: #105331;
    font-size: 18px;
}
.card p {
    color: #526173;
    margin: 6px 0;
}
.st-key-banner_box {
    position: relative;
    border-radius: 18px;
    overflow: hidden;
}
.farmer-hero {
    position: relative;
    width: 100%;
    border-radius: 18px;
    overflow: hidden;
}
.farmer-hero img {
    display: block;
    width: 100%;
    height: auto;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        rgba(255,255,255,0.94),
        rgba(255,255,255,0.65) 35%,
        transparent 65%
    );
}
.hero-text {
    position: absolute;
    top: 50%;
    left: 3%;
    transform: translateY(-50%);
    max-width: 60%;
}
.hero-text h1 {
    color: #064b28;
    font-size: clamp(24px, 3vw, 44px);
    margin: 0 0 12px;
}
.hero-text h3 {
    color: #14532d;
    font-size: clamp(14px, 1.5vw, 21px);
    margin: 0 0 12px;
}
.hero-text p {
    color: #176b37;
    font-weight: bold;
}
.st-key-language_row {
    position: absolute;
    top: 16px;
    right: 18px;
    width: 250px;
    z-index: 10;
}
@media (max-width: 700px) {
    .st-key-language_row {
        width: 180px;
        top: 8px;
        right: 8px;
    }
    .hero-text h1 {
        font-size: 20px;
    }
    .hero-text h3 {
        font-size: 12px;
    }
    .hero-text p {
        font-size: 11px;
    }
}
</style>
""", unsafe_allow_html=True)

# 4. Farmer banner and language buttons
banner = config.BANNER_IMAGE

with st.container(key="banner_box"):
    if banner.exists():
        image = base64.b64encode(banner.read_bytes()).decode()

        st.markdown(f"""
        <div class="farmer-hero">
            <img src="data:image/png;base64,{image}"
                 alt="Tamil Nadu farmer">
            <div class="hero-overlay"></div>
            <div class="hero-text">
                <h1>🌾 {t['title']}</h1>
                <h3>{t['subtitle']}</h3>
                <p>{t['banner']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Add farmer_banner.png inside assets folder.")

    with st.container(key="language_row"):
        english_col, tamil_col = st.columns(2)

        with english_col:
            if st.button(
                "English",
                key="english_button",
                use_container_width=True,
                type="primary" if language == "English" else "secondary"
            ):
                st.session_state.language = "English"
                st.session_state.scheme_answer = ""
                st.session_state.faq_answer = ""
                st.rerun()

        with tamil_col:
            if st.button(
                "தமிழ்",
                key="tamil_button",
                use_container_width=True,
                type="primary" if language == "தமிழ்" else "secondary"
            ):
                st.session_state.language = "தமிழ்"
                st.session_state.scheme_answer = ""
                st.session_state.faq_answer = ""
                st.rerun()

st.write("")

# 5. Information cards
cards = [
    ("🌱 " + t["agriculture"], t["schemes"]),
    ("🪙 " + t["subsidies"], t["financial"]),
    ("🤖 " + t["assistant"], t["ask_language"])
]

for col, (title, description) in zip(st.columns(3), cards):
    with col:
        st.markdown(
            f'<div class="card"><b>{title}</b><p>{description}</p></div>',
            unsafe_allow_html=True
        )

st.write("")

# 6. Ask questions using FAISS and OpenAI
def ask_farmer(question):
    try:
        answer, sources = rag.ask_question(
            question,
            language,
            st.session_state.messages.copy()
        )

        st.session_state.messages.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer, "sources": sources}
        ])

        return answer

    except Exception as e:
        st.error(f"Unable to answer: {e}")
        return None

# 7. Suggested questions
questions = {
    "English": [
        "What schemes are available for farmers?",
        "How can I get subsidized seeds?",
        "What irrigation support is available?",
        "What documents are needed?"
    ],
    "தமிழ்": [
        "விவசாயிகளுக்கு என்னென்ன திட்டங்கள் உள்ளன?",
        "மானிய விலையில் விதைகளை எப்படிப் பெறுவது?",
        "நீர்ப்பாசனத்திற்கு என்ன உதவிகள் உள்ளன?",
        "என்ன ஆவணங்கள் தேவை?"
    ]
}

faqs = {
    "English": [
        "What farmer schemes are available in Tamil Nadu?",
        "How can I apply for a subsidy?",
        "What documents are required?",
        "What benefits are available for small farmers?"
    ],
    "தமிழ்": [
        "தமிழ்நாட்டில் என்ன விவசாயத் திட்டங்கள் உள்ளன?",
        "மானியத்திற்கு எப்படி விண்ணப்பிப்பது?",
        "என்ன ஆவணங்கள் தேவை?",
        "சிறு விவசாயிகளுக்கு என்ன நன்மைகள் உள்ளன?"
    ]
}

# 8. Three-column layout
left, center, right = st.columns([1.2, 3, 1.3], gap="medium")

# LEFT: PDF upload
with left:
    st.subheader("🌿 " + t["upload"])
    st.caption(t["upload_caption"])

    files = st.file_uploader(
        t["upload_pdf"],
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("➕ " + t["add"], type="primary", use_container_width=True):
        if files:
            for file in files:
                with st.spinner(f"Processing {file.name}..."):
                    try:
                        result = rag.add_pdf(file.name, file.getvalue())
                        st.success(f"{file.name}: {result}")
                    except Exception as e:
                        st.error(f"PDF error: {e}")
        else:
            st.warning(t["select_pdf"])

    with st.expander("📄 " + t["documents"]):
        if rag.files:
            for name in rag.files.values():
                st.write("📄", name)
        else:
            st.write(t["no_documents"])

    st.markdown("**ℹ️ " + t["about"] + "**")
    st.caption(t["about_text"])

    if st.button("🗑️ " + t["clear"], use_container_width=True):
        st.session_state.messages = []
        st.session_state.scheme_answer = ""
        st.session_state.faq_answer = ""
        st.rerun()

# CENTER: Chat and FAQ
with center:
    chat_tab, faq_tab = st.tabs([
        "💬 " + t["chat"],
        "❓ " + t["faq"]
    ])

    with chat_tab:
        st.subheader("🌱 " + t["welcome"])
        st.write(t["ask"])
        st.markdown("**💡 " + t["suggested"] + "**")

        question_cols = st.columns(2)

        for i, question in enumerate(questions[language]):
            with question_cols[i % 2]:
                if st.button(question, key=f"q{i}", use_container_width=True):
                    with st.spinner(t["finding"]):
                        if ask_farmer(question) is not None:
                            st.rerun()

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

                for source in msg.get("sources", []):
                    st.caption(
                        f"📄 {source['file']} | Page {source['page']}"
                    )

        question = st.chat_input(t["type"])

        if question:
            with st.spinner(t["searching"]):
                if ask_farmer(question) is not None:
                    st.rerun()

        audio = st.audio_input("🎤 " + t["voice"])

        if audio and st.button(t["submit_voice"]):
            with st.spinner(t["processing_voice"]):
                try:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio,
                        language="ta" if language == "தமிழ்" else "en"
                    )
                    if ask_farmer(transcript.text) is not None:
                        st.rerun()
                except Exception as e:
                    st.error(f"Voice error: {e}")

    with faq_tab:
        st.subheader("❓ " + t["faq_title"])

        for i, question in enumerate(faqs[language]):
            if st.button(question, key=f"faq{i}"):
                with st.spinner(t["finding"]):
                    answer = ask_farmer(question)
                    if answer is not None:
                        st.session_state.faq_answer = answer

        # Display FAQ answer directly
        if st.session_state.faq_answer:
            st.markdown("### 💬 " + t["assistant"])
            st.write(st.session_state.faq_answer)

# RIGHT: Scheme finder
with right:
    st.subheader("📢 " + t["guide"])
    st.caption(t["guide_caption"])

    scheme_questions = {
        t["crop"]: {
            "English": "Tell me about crop insurance schemes.",
            "தமிழ்": "பயிர் காப்பீட்டுத் திட்டங்கள் பற்றி கூறுங்கள்."
        },
        t["seed"]: {
            "English": "How can I get subsidized seeds?",
            "தமிழ்": "மானிய விலையில் விதைகளை எப்படிப் பெறுவது?"
        },
        t["machinery"]: {
            "English": "What farm machinery subsidies are available?",
            "தமிழ்": "விவசாய இயந்திரங்களுக்கு என்ன மானியங்கள் உள்ளன?"
        },
        t["irrigation"]: {
            "English": "What irrigation schemes are available?",
            "தமிழ்": "என்ன நீர்ப்பாசனத் திட்டங்கள் உள்ளன?"
        }
    }

    selected = st.selectbox(
        t["choose"],
        list(scheme_questions),
        index=None,
        placeholder=t["choose"],
        key="scheme_select"
    )

    if st.button(
        "🔍 " + t["find"],
        type="primary",
        use_container_width=True
    ):
        if selected:
            with st.spinner(t["finding"]):
                answer = ask_farmer(scheme_questions[selected][language])
                if answer is not None:
                    st.session_state.scheme_answer = answer
        else:
            st.warning(t["select_scheme"])

    # Display scheme answer directly below Find Schemes
    if st.session_state.scheme_answer:
        st.markdown("### 💬 " + t["assistant"])
        st.write(st.session_state.scheme_answer)

    st.markdown("**⭐ " + t["popular"] + "**")

    for scheme in scheme_questions:
        st.write("✅", scheme)

# 9. Footer
st.divider()
st.markdown(
    f"<center style='color:#176b37;'>"
    f"🌱 <b>{t['title']} | {t['footer']}</b>"
    f"</center>",
    unsafe_allow_html=True
)
