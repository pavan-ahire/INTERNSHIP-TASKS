# 🧬 PharmaGen AI — Intelligent Pharmaceutical Chat Assistant

PharmaGen AI is an advanced **Generative AI-powered pharmaceutical assistant** built to provide accurate, context-aware, and intelligent responses for pharmaceutical industry-related queries.  
Powered by **Google Gemini LLM** and developed with **Streamlit**, the system supports conversational memory, modular architecture, and real-time AI interaction.

---

# 🚀 Key Features

- 💬 AI-powered pharmaceutical chatbot
- 🧠 Context-aware conversations with memory support
- 🏥 Specialized for pharmaceutical and healthcare domain queries
- ⚡ Fast and interactive Streamlit-based interface
- 🔄 Session-based chat history management
- 🧹 One-click conversation reset functionality
- 📦 Scalable and modular code architecture
- 🤖 Real-time response generation using Gemini API

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| LLM | Google Gemini API |
| Memory Handling | Streamlit Session State |
| Prompt Engineering | Custom Prompt Builder |
| Architecture | Modular AI System |

---

# 📁 Project Structure

```bash
pharmagen-ai/
│
├── app.py
│
├── chatbot/
│   ├── gemini_client.py
│   ├── memory_manager.py
│   ├── prompt_builder.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pharmagen-ai.git

cd pharmagen-ai
```

---

## 2️⃣ Create Virtual Environment

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

## 3️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 5️⃣ Launch the Application

```bash
streamlit run app.py
```

---

# 🧠 How PharmaGen AI Works

```text
User Query
     ↓
Memory Storage
     ↓
Prompt Builder
     ↓
Gemini API Processing
     ↓
AI Response Generation
     ↓
Response Saved in Memory
```

---

# 🔥 Core Functionalities

## 💬 Conversational AI
Users can interact naturally with the chatbot for pharmaceutical-related discussions and information retrieval.

---

## 🧠 Memory-Enabled Responses
The chatbot maintains session memory to generate context-aware and more human-like conversations.

---

## 🏥 Pharmaceutical Knowledge Assistance
Designed specifically for:
- Drug-related queries
- Manufacturing insights
- Pharma workflows
- Regulatory discussions
- Clinical research information

---

# 💡 Example Use Cases

- 📌 Drug composition and usage information
- 📌 Pharmaceutical manufacturing processes
- 📌 Clinical trial discussions
- 📌 Industry trend analysis
- 📌 Regulatory guidance assistance

---

# 🔐 Environment Variables

| Variable Name | Description |
|----------------|-------------|
| `GEMINI_API_KEY` | API key for accessing Google Gemini models |

---

# ⚠️ Current Limitations

- Responses depend on LLM-generated outputs
- Internet/API availability required
- Session memory resets after app restart

---

# 🚀 Future Enhancements

- 🌐 Multi-language pharmaceutical assistant
- 📊 Dashboard for analytics & insights
- 🧾 Export chat history as PDF/DOCX
- 🔐 User authentication system
- ☁️ Cloud deployment support
- 🧠 Persistent long-term memory integration

---

# 📸 User Interface

Clean and modern chatbot interface built using Streamlit for seamless user interaction.

---

# 👨‍💻 Developed By

## **Pavan Ahire**
AI/ML & Generative AI Developer

---

# 🙌 Acknowledgements

Special thanks to:

- Streamlit
- Google Gemini API
- Python Open-Source Community

---

# 📜 License

This project is created for educational, learning, and portfolio purposes.

---

> 🚀 A real-world Generative AI application demonstrating LLM integration, conversational memory, prompt engineering, and modular AI system architecture.
