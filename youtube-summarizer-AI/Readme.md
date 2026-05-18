# 🚀 AI-Powered YouTube Content Transformer

Transform any YouTube video into detailed articles, summaries, and downloadable PDFs using the power of **Generative AI**.  
This application leverages advanced LLMs from **Groq**, intelligent transcript extraction, and a sleek **Streamlit** interface to automate content creation efficiently.

---

# 🌟 Features

✔️ Extract subtitles and transcripts from YouTube videos  
✔️ Generate high-quality AI articles instantly  
✔️ Multiple article modes:
- Blog Style
- Technical Documentation
- Beginner-Friendly
- News Summary

✔️ Support for multiple languages  
✔️ Export generated content as PDF  
✔️ Smart transcript recovery system  
✔️ Fast and responsive Streamlit dashboard  
✔️ Error handling for unavailable videos and API issues  

---

# 🧠 AI Workflow

```text
YouTube URL
      ↓
Transcript Extraction
(API + yt-dlp Fallback)
      ↓
Text Processing
      ↓
Groq LLaMA Model
      ↓
AI Article Generation
      ↓
PDF Export
```

---

# 🛠️ Technologies & Libraries

| Category | Tools Used |
|----------|-------------|
| Frontend | Streamlit |
| Language Model | Groq LLaMA 3 |
| Backend | Python |
| Transcript API | youtube-transcript-api |
| Backup Extraction | yt-dlp |
| PDF Generator | ReportLab |
| Environment Variables | dotenv |

---

# 📂 Folder Structure

```bash
youtube-content-transformer/
│
├── app.py
│
├── utils/
│   ├── transcript.py
│   ├── article_generator.py
│   ├── pdf_generator.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Installation Guide

## Step 1 — Clone the Project

```bash
git clone https://github.com/your-username/youtube-content-transformer.git
cd youtube-content-transformer
```

---

## Step 2 — Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Add API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Step 5 — Run the Streamlit App

```bash
streamlit run app.py
```

---

# 🔥 Main Functionalities

## 🎬 Transcript Extraction
The system first attempts transcript extraction using:
- `youtube-transcript-api`

If unavailable, it automatically switches to:
- `yt-dlp`

---

## 🤖 AI Article Generation
The extracted transcript is processed through the Groq LLaMA model to generate:
- Summaries
- Long-form articles
- Technical explanations
- Beginner guides

---

## 📄 PDF Export
Generated content can be downloaded instantly as a structured PDF document.

---

# 💡 Why This Project?

This project demonstrates:
- Real-world LLM integration
- Prompt engineering
- AI content automation
- Transcript processing pipeline
- Scalable modular architecture
- Production-level error handling

---

# ⚠️ Limitations

- Videos without subtitles may fail
- Private videos are unsupported
- YouTube may temporarily rate-limit requests

---

# 🚀 Future Scope

- 🎥 Video thumbnail & preview support
- 📚 Article history management
- 🧾 DOCX export feature
- ☁️ Cloud deployment
- 📊 SEO & readability analytics
- 🧠 Personalized summarization

---

# 👨‍💻 Created By

## **Pavan Ahire**
Generative AI | Machine Learning | Python Developer

---

# 🙏 Credits

Special thanks to the open-source community and tools:

- Streamlit
- Groq AI
- yt-dlp
- youtube-transcript-api
- ReportLab

---

# 📜 License

Open-source project developed for educational and portfolio purposes.

---

> 💡 An end-to-end Generative AI application showcasing intelligent transcript extraction, AI-powered content generation, and automated PDF creation.
