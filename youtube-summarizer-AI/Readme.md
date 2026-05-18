# 🎥 YouTube AI Article Generator & PDF Summarizer

A powerful **Generative AI-based application** that transforms YouTube videos into well-structured articles and downloadable PDFs.  
Built using **Streamlit**, **Groq LLaMA models**, and intelligent transcript extraction techniques, this project automates content summarization and article generation in multiple formats and languages.

---

## 🚀 Core Features

- 🎬 Extract transcripts directly from YouTube videos
- 🤖 Generate AI-written articles using Groq LLaMA models
- 🌍 Support for multi-language content generation
- 📝 Multiple writing styles (Technical, Blog, Beginner, News, etc.)
- 📄 Download generated content as PDF
- ⚡ Fast and interactive Streamlit interface
- 🔁 Dual transcript extraction system with fallback support
- 🎨 Modern and responsive UI design
- 🛡️ Handles transcript failures and unavailable videos gracefully

---

## 🛠️ Technologies Used

### Frontend
- Streamlit

### Backend
- Python

### AI & LLM
- Groq API
- LLaMA 3.3

### Transcript Extraction
- youtube-transcript-api
- yt-dlp

### PDF Generation
- ReportLab

### Environment Handling
- python-dotenv

---

## 📁 Project Structure

```bash
youtube-ai-article-generator/
│
├── app.py                         # Main Streamlit application
│
├── utils/
│   ├── transcript.py              # Transcript extraction logic
│   ├── article_generator.py       # AI article generation
│   ├── pdf_generator.py           # PDF creation module
│
├── requirements.txt
├── .env                           # API keys (ignored in Git)
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/youtube-ai-article-generator.git

cd youtube-ai-article-generator
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 5️⃣ Launch the Application

```bash
streamlit run app.py
```

---

# 🔍 Application Workflow

1. User submits a YouTube video URL
2. System extracts transcript using:
   - `youtube-transcript-api`
   - `yt-dlp` fallback mechanism
3. Extracted transcript is processed
4. Transcript is sent to the Groq LLaMA model
5. AI generates article based on:
   - Selected writing style
   - Article length
   - Preferred language
6. Generated article is displayed instantly
7. User can export the article as a downloadable PDF

---

# ✨ Project Highlights

- ⚡ Fast AI-powered article generation
- 🔁 Reliable transcript extraction pipeline
- 🌐 Multi-language support
- 📄 Automated PDF generation
- 🧩 Modular and scalable architecture
- 🛡️ Real-world error handling implementation
- 🎯 Beginner-friendly interface with advanced functionality

---

# 🔐 Environment Variables

| Variable Name | Purpose |
|----------------|---------|
| `GROQ_API_KEY` | API key used for Groq LLM access |

---

# ⚠️ Current Limitations

- Some YouTube videos may not contain transcripts
- Private or region-restricted videos may fail
- Excessive requests can trigger YouTube rate limits

---

# 🚀 Planned Enhancements

- 🎥 Embedded YouTube video preview
- 📊 AI-powered article analytics
- 🧾 DOCX and Markdown export support
- ☁️ Cloud deployment integration
- 🧠 Context-aware memory summarization
- 📚 Save article history

---

# 👨‍💻 Developer

**Pavan Ahire**  
AI/ML & Generative AI Developer

---

# 🙌 Acknowledgements

Special thanks to:

- Streamlit
- Groq AI
- LLaMA Models
- youtube-transcript-api
- yt-dlp
- ReportLab

---

# 📜 License

This project is developed for educational, learning, and portfolio purposes.

---

> 🚀 A real-world Generative AI project showcasing transcript extraction, LLM integration, intelligent summarization, and automated document generation.
