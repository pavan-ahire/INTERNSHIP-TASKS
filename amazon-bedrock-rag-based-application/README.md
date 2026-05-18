# 📚 Enterprise RAG System

An **Enterprise Retrieval-Augmented Generation (RAG) System** built using **Python, Streamlit, AWS Bedrock, Amazon S3, and Boto3**.  
This application allows users to upload company documents, store them in S3, and ask questions in natural language using an AI-powered knowledge base with cited responses.

---

## 🚀 Features

- 🔍 Ask questions from enterprise documents using AI
- 📄 Upload TXT, PDF, and DOCX files
- ☁️ Store documents securely in Amazon S3
- 🤖 Powered by Amazon Bedrock Foundation Models
- 📚 Uses Bedrock Knowledge Base for retrieval
- 🖥️ Clean Streamlit web interface
- 📌 Citation-based answers from source documents

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Cloud Services:** AWS Bedrock, Amazon S3  
- **SDK:** Boto3  
- **Environment Management:** python-dotenv  

---

## 📂 Project Structure

```bash
enterprise-rag-system/
│── app.py                 # Streamlit UI
│── bedrock_rag.py         # AWS Bedrock + RAG logic
│── config.py              # Configuration settings
│── requirements.txt       # Dependencies
│── documents/             # Sample company docs
│── scripts/               # Deployment & setup scripts
````

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd enterprise-rag-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate      # Linux/Mac
myenv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configure AWS Credentials

Create a `.env` file:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 📌 How It Works

1. Upload enterprise documents
2. Files stored in Amazon S3
3. Bedrock Knowledge Base indexes documents
4. User asks question in chat UI
5. Relevant chunks retrieved
6. AI generates contextual answer with citations

---

## 💡 Example Questions

* What is company leave policy?
* What are office timings?
* Explain IT security rules.
* What data privacy rules are defined?

---

## 📈 Future Enhancements

* Multi-user login system
* Chat history storage
* PDF summarization
* Role-based access control
* Dashboard analytics

---

## 👨‍💻 Author

**Mahesh Bodhankar**
AI / ML / Data Science Enthusiast

---

## 📜 License

This project is for educational and portfolio purposes.

