# 💊 PharmaGen AI — Pharmaceutical Industry Assistant

PharmaGen AI is a **production-ready Generative AI chatbot** designed to assist with pharmaceutical industry queries. It leverages advanced LLM capabilities to provide intelligent, context-aware responses with memory support.

---

## 🚀 Features

* 💬 Conversational AI chatbot using LLM (Gemini)
* 🧠 Memory-enabled chat (context-aware responses)
* 🏥 Specialized for pharmaceutical domain queries
* ⚡ Fast and interactive UI using Streamlit
* 🔄 Session-based conversation tracking
* 🧹 Clear conversation functionality
* 📦 Modular and scalable architecture

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **LLM:** Google Gemini API
* **Backend Logic:** Python
* **State Management:** Streamlit Session State
* **Architecture:** Modular (Client, Memory, Prompt Builder)

---

## 📂 Project Structure

```
pharmagen-ai/
│
├── app.py                     # Main Streamlit app
├── chatbot/
│   ├── gemini_client.py      # Handles Gemini API calls
│   ├── memory_manager.py     # Manages conversation memory
│   ├── prompt_builder.py     # Builds structured prompts
│
├── .env                      # API keys (not included in repo)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pharmagen-ai.git
cd pharmagen-ai
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate     # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variables

Create a `.env` file and add:

```env
GEMINI_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. User enters a pharmaceutical query
2. Input is stored in memory
3. Prompt is generated using `prompt_builder`
4. Gemini API generates a response
5. Response is stored and displayed
6. Context is maintained across conversation

---

## 💡 Example Use Cases

* Drug information queries
* Pharmaceutical regulations
* Clinical research insights
* Industry trends
* Manufacturing processes

---

## 🔒 Environment Variables

| Variable       | Description               |
| -------------- | ------------------------- |
| GEMINI_API_KEY | API key for Google Gemini |

---

## 🧪 Future Improvements

* 🌐 Multi-language support
* 📊 Analytics dashboard
* 🧾 Export chat history
* 🔐 Authentication system
* ☁️ Cloud deployment (Streamlit Cloud / AWS)

---

## 📸 UI Preview

Simple and clean chat-based interface powered by Streamlit.

---

## 👨‍💻 Author

**Mahesh Bodhankar**
Aspiring Data Analyst & GenAI Developer

---

## ⭐ Acknowledgements

* Streamlit
* Google Gemini API
* Open-source Python ecosystem

---

## 📌 License

This project is for educational and portfolio purposes.

---

> 🚀 Built as a real-world GenAI project to demonstrate LLM integration, memory handling, and modular AI system design.
