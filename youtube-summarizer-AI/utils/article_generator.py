"""
article_generator.py
─────────────────────
Calls Groq API (LLaMA-3) to convert YouTube transcript into a polished article.
Supports multiple output languages and article styles.
"""

import os
from groq import Groq

LENGTH_MAP = {
    "Short (~300 words)": 300,
    "Medium (~600 words)": 600,
    "Long (~1000 words)": 1000,
}

STYLE_MAP = {
    "Informative Blog": (
        "an engaging, informative blog post with a warm, conversational tone. "
        "Include key insights, real-world implications, and takeaways."
    ),
    "Technical Deep-Dive": (
        "a detailed technical article. Use precise terminology, explain concepts "
        "thoroughly, and include technical context and reasoning."
    ),
    "Beginner-Friendly": (
        "a beginner-friendly article that explains every concept simply. "
        "Avoid jargon, use analogies, and keep sentences short."
    ),
    "News Summary": (
        "a concise news-style summary. Lead with the most important point, "
        "follow the inverted pyramid structure, and remain objective."
    ),
}

LANGUAGE_MAP = {
    "English": "English",
    "Hindi (हिंदी)": "Hindi",
    "Spanish (Español)": "Spanish",
    "French (Français)": "French",
    "German (Deutsch)": "German",
    "Portuguese (Português)": "Portuguese",
    "Arabic (العربية)": "Arabic",
    "Chinese Simplified (中文)": "Simplified Chinese",
    "Japanese (日本語)": "Japanese",
    "Korean (한국어)": "Korean",
    "Italian (Italiano)": "Italian",
    "Russian (Русский)": "Russian",
    "Dutch (Nederlands)": "Dutch",
    "Turkish (Türkçe)": "Turkish",
    "Bengali (বাংলা)": "Bengali",
    "Marathi (मराठी)": "Marathi",
    "Tamil (தமிழ்)": "Tamil",
    "Telugu (తెలుగు)": "Telugu",
    "Gujarati (ગુજરાતી)": "Gujarati",
    "Punjabi (ਪੰਜਾਬੀ)": "Punjabi",
}


def build_prompt(transcript: str, title: str, style: str, length: str, language: str) -> str:
    word_count = LENGTH_MAP.get(length, 600)
    style_desc = STYLE_MAP.get(style, STYLE_MAP["Informative Blog"])
    lang_name = LANGUAGE_MAP.get(language, "English")

    max_chars = 12000
    trimmed = transcript[:max_chars]
    if len(transcript) > max_chars:
        trimmed += "\n\n[Transcript trimmed for length]"

    lang_instruction = ""
    if lang_name != "English":
        lang_instruction = f"\n- OUTPUT LANGUAGE: Write the ENTIRE article in {lang_name}. Every word of the article must be in {lang_name}, including headings, introduction, body, and conclusion."

    prompt = f"""You are an expert content writer and multilingual journalist. Transform the YouTube video transcript into a polished article.

VIDEO TITLE: {title}

ARTICLE REQUIREMENTS:
- Style: Write as {style_desc}
- Target length: approximately {word_count} words{lang_instruction}
- Structure: Use a compelling title, introduction, 2-4 body sections with clear headings (##), and a conclusion
- Do NOT mention "transcript", "video", or "YouTube" — write as if it's an original article
- Start directly with the article title, no preamble
- Use markdown formatting (## for section headings)

TRANSCRIPT (may be in any language):
{trimmed}

Now write the full article:"""
    return prompt


def generate_article(
    transcript: str,
    video_title: str,
    article_style: str,
    article_length: str,
    language: str = "English",
) -> tuple[str, str | None]:

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "", "GROQ_API_KEY is not set."

    try:
        client = Groq(api_key=api_key)
        prompt = build_prompt(transcript, video_title, article_style, article_length, language)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048,
        )

        article = response.choices[0].message.content.strip()
        return article, None

    except Exception as e:
        return "", f"Groq API error: {e}"


def get_language_list():
    return list(LANGUAGE_MAP.keys())


def get_language_code(language_label: str) -> str:
    return LANGUAGE_MAP.get(language_label, "English")