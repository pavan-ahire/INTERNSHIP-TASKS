
# 🎬 YouTube Summarizer AI → Article & PDF Generator

An advanced **Generative AI application** that converts YouTube videos into structured articles and downloadable PDFs.
Built with Streamlit and powered by Groq LLaMA models, this system extracts transcripts, generates high-quality content, and delivers formatted outputs in multiple languages.

---

## 🚀 Features

* 🎥 Extract transcript from any YouTube video
* ✍️ Generate AI-powered articles (multiple styles)
* 🌐 Multi-language article generation
* 📄 Export article as downloadable PDF
* 🧠 Smart fallback system (Transcript API + yt-dlp)
* ⚡ Fast UI with Streamlit
* 🎨 Clean, modern UI with custom styling
* 🔄 Handles errors (rate limiting, unavailable videos)

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **LLM:** Groq (LLaMA 3.3)
* **Transcript Extraction:** youtube-transcript-api, yt-dlp
* **PDF Generation:** ReportLab
* **Backend:** Python
* **Environment Management:** dotenv

---

## 📂 Project Structure

```id="0lgvhh"
youtube-summarizer-ai/
│
├── app.py                        # Main Streamlit application
├── utils/
│   ├── transcript.py            # Extract transcript (API + fallback)
│   ├── article_generator.py     # Generate article using LLM
│   ├── pdf_generator.py         # Convert article to PDF
│
├── .env                         # API keys (not included)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash id="q7qkq2"
git clone https://github.com/your-username/youtube-summarizer-ai.git
cd youtube-summarizer-ai
```

---

### 2️⃣ Create Virtual Environment

```bash id="9cb2nl"
python -m venv myenv
myenv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash id="q1a3qa"
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variables

Create a `.env` file:

```env id="9r1j5s"
GROQ_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the App

```bash id="x7x9tw"
streamlit run app.py
```

---

## 🧠 How It Works

1. User pastes YouTube URL
2. Transcript is extracted using:

   * youtube-transcript-api (primary)
   * yt-dlp (fallback)
3. Transcript is processed and sent to Groq LLM
4. Article is generated based on:

   * Style (Blog, Technical, Beginner, News)
   * Length (Short, Medium, Long)
   * Language
5. Article is displayed in UI
6. PDF is generated and available for download

---

## 💡 Key Highlights

* 🔁 Robust fallback system for transcript extraction
* 🌍 Multi-language AI content generation
* 📄 Automated PDF creation with structured formatting
* ⚙️ Modular and scalable architecture
* 🧪 Handles real-world issues (rate limits, unavailable videos)

---

## 🔒 Environment Variables

| Variable     | Description          |
| ------------ | -------------------- |
| GROQ_API_KEY | API key for Groq LLM |

---

## ⚠️ Known Limitations

* Some videos may not provide transcripts
* Region-restricted / private videos may fail
* YouTube rate limiting may occur on heavy usage

---

## 🧪 Future Improvements

* 🎥 Video preview inside UI
* 📊 Article analytics (readability, keywords)
* 🧾 Export to DOCX / Markdown
* ☁️ Cloud deployment (Streamlit Cloud / AWS)
* 🧠 Memory-based summarization

---

## 👨‍💻 Author

**Mahesh Bodhankar**
Aspiring Data Analyst & GenAI Developer

---

## ⭐ Acknowledgements

* Streamlit
* Groq AI (LLaMA models)
* youtube-transcript-api
* yt-dlp
* ReportLab

---

## 📌 License

This project is for educational and portfolio use.

---

> 🚀 Built as a real-world GenAI system demonstrating transcript processing, LLM integration, and automated content generation pipeline.
