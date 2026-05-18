import streamlit as st
import os
from dotenv import load_dotenv
from utils.transcript import get_transcript
from utils.article_generator import generate_article, get_language_list
from utils.pdf_generator import generate_pdf

load_dotenv()

# Load API Key from Streamlit Cloud secrets if available
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube → Article & PDF",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0b0f19 !important;
}
h1, h2, h3, h4 { font-family: 'Syne', sans-serif; color: #ffffff !important; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(135deg, #00E5FF, #00BCD4, #009688);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

.subtitle {
    color: #8b9bb4;
    font-size: 1rem;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
}

.step-badge {
    display: inline-block;
    background: linear-gradient(135deg, #00E5FF, #00BCD4);
    color: #0b0f19;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.article-box {
    background: #111827;
    border: 1px solid #00BCD4;
    border-radius: 12px;
    padding: 1.8rem;
    color: #e0e8f0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.8;
    white-space: pre-wrap;
    box-shadow: 0 4px 20px rgba(0, 229, 255, 0.08);
}

.stButton > button {
    background: linear-gradient(135deg, #00E5FF, #00BCD4);
    color: #0b0f19;
    border: none;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.6rem 2rem;
    border-radius: 10px;
    transition: all 0.2s;
    width: 100%;
    box-shadow: 0 4px 15px rgba(0, 188, 212, 0.25);
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0, 188, 212, 0.35);
}

.info-pill {
    display: inline-block;
    background: #111827;
    border: 1px solid #00BCD4;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 0.8rem;
    color: #00E5FF;
    margin: 2px;
}

.lang-badge {
    display: inline-block;
    background: linear-gradient(135deg, #FF6F3C, #FF8C42);
    color: #ffffff;
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-left: 8px;
}

.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    background-color: #111827 !important;
    border: 1px solid #334155 !important;
    color: #ffffff !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus {
    border-color: #00E5FF !important;
    box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2) !important;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎬 YouTube Sumarizer AI → Article & PDF</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Paste any YouTube URL · Pick a language · Get a full article + PDF with cheatsheet — powered by Groq AI.</div>',
    unsafe_allow_html=True
)
st.divider()

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown('<span class="step-badge">Step 1 — Video URL</span>', unsafe_allow_html=True)
youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed"
)

st.markdown('<span class="step-badge">Step 2 — Options</span>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    article_style = st.selectbox(
        "Article Style",
        ["Informative Blog", "Technical Deep-Dive", "Beginner-Friendly", "News Summary"]
    )
with col2:
    article_length = st.selectbox(
        "Article Length",
        ["Short (~300 words)", "Medium (~600 words)", "Long (~1000 words)"]
    )

# Language selection — full width, prominent
st.markdown('<span class="step-badge">Step 3 — Output Language</span>', unsafe_allow_html=True)
languages = get_language_list()
output_language = st.selectbox(
    "Output Language",
    languages,
    index=0,
    help="The article and PDF will be generated in the selected language.",
    label_visibility="collapsed"
)
st.markdown(
    f'<div style="margin-top:4px;margin-bottom:8px;color:#8b9bb4;font-size:0.85rem;">'
    f'🌐 Article will be written in: <span style="color:#00E5FF;font-weight:600;">{output_language}</span>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Generate Button ────────────────────────────────────────────────────────────
st.markdown("")
generate_btn = st.button("🚀 Generate Article & PDF")

# ── Logic ──────────────────────────────────────────────────────────────────────
if generate_btn:
    if not youtube_url.strip():
        st.error("⚠️ Please enter a YouTube URL.")
    elif not os.environ.get("GROQ_API_KEY"):
        st.error("⚠️ GROQ_API_KEY is not set. Please add it to your .env file or Streamlit secrets.")
    else:
        # ── Transcript ─────────────────────────────────────────────────────────
        with st.spinner("📥 Extracting transcript from YouTube..."):
            transcript, video_title, error = get_transcript(youtube_url)

        if error:
            st.error(f"❌ Transcript Error: {error}")
            st.info(
                "💡 **Tips to fix this:**\n"
                "- Make sure the video has subtitles/captions enabled\n"
                "- Try a different video\n"
                "- If rate-limited, wait 2–5 minutes and try again\n"
                "- Some region-locked or age-restricted videos may not work"
            )
        else:
            word_count = len(transcript.split())
            st.success(f"✅ Transcript extracted — **{word_count:,} words**")
            st.markdown(f'<span class="info-pill">🎞 {video_title}</span>', unsafe_allow_html=True)

            with st.expander("📄 View Raw Transcript"):
                st.text_area(
                    "Transcript",
                    transcript[:3000] + ("..." if len(transcript) > 3000 else ""),
                    height=200,
                )

            # ── Article ────────────────────────────────────────────────────────
            st.markdown("")
            st.markdown(
                f'<span class="step-badge">Generating Article</span>'
                f'<span class="lang-badge">{output_language}</span>',
                unsafe_allow_html=True
            )
            with st.spinner(f"✍️ Writing article in {output_language} using Groq AI..."):
                article, gen_error = generate_article(
                    transcript, video_title, article_style, article_length, output_language
                )

            if gen_error:
                st.error(f"❌ Generation Error: {gen_error}")
            else:
                st.success(f"✅ Article generated in {output_language}!")
                st.markdown(f"### 📝 Generated Article")
                st.markdown(f'<div class="article-box">{article}</div>', unsafe_allow_html=True)

                # ── PDF ────────────────────────────────────────────────────────
                st.markdown("")
                st.markdown('<span class="step-badge">Creating PDF</span>', unsafe_allow_html=True)
                with st.spinner("📄 Building PDF with cheatsheet..."):
                    pdf_bytes, pdf_error = generate_pdf(article, video_title, output_language)

                if pdf_error:
                    st.error(f"❌ PDF Error: {pdf_error}")
                else:
                    st.success("✅ PDF ready — includes article + cheatsheet!")
                    safe_title = "".join(c for c in video_title if c.isalnum() or c in " _-")[:40].strip()
                    lang_tag = output_language.split(" ")[0].lower()
                    st.download_button(
                        label=f"⬇️ Download PDF ({output_language})",
                        data=pdf_bytes,
                        file_name=f"{safe_title}_{lang_tag}.pdf",
                        mime="application/pdf",
                    )
                    st.caption("📋 PDF includes: full article + key points cheatsheet + article structure + supported languages reference")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small style='color:#556677'>Built with Streamlit · Groq LLaMA-3.3 · youtube-transcript-api · ReportLab</small></center>",
    unsafe_allow_html=True
)