# 🚀 NetSense AI

### AI-Based Internet Connection Quality Analyzer using AI/LLM (LangChain) + Fuzzy Logic

**NetSense AI** is a web-based application that analyzes Internet connection quality using **Latency, Jitter, and Packet Loss**. It combines **Fuzzy Logic** with **AI/LLM using LangChain and Google Gemini** to provide a quality score, connection analysis, and recommendations.

## 🌐 Live Demo

🚀 **Try NetSense AI Online:**

https://ai-internet-quality-analyzer.streamlit.app/

> The application is deployed using **Streamlit Community Cloud**.

## ✨ Features

- 📡 Latency, Jitter & Packet Loss analysis
- 🧠 Fuzzy Logic based quality scoring
- 🤖 AI/LLM analysis using LangChain + Gemini
- 🎮 Gaming analysis
- 🎥 Video Conferencing analysis
- 📺 Streaming analysis
- 🌐 General Browsing analysis
- 📊 Interactive results dashboard
- 📈 Fuzzy membership visualization
- 💡 AI-generated recommendations

## 🛠️ Technologies

- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Streamlit Interface:** Python, Streamlit
- **Backend:** Python, FastAPI, Uvicorn
- **Fuzzy Logic:** scikit-fuzzy, NumPy, SciPy
- **AI/LLM:** LangChain, Google Gemini
- **Network Testing:** ICMP Ping
- **Development:** VS Code, Git, GitHub
- **Deployment:** Streamlit Community Cloud

## 🧠 How It Works

```text
Internet Connection
        ↓
Latency + Jitter + Packet Loss
        ↓
     Fuzzy Logic
        ↓
Quality Score + Category
        ↓
   LangChain + Gemini
        ↓
AI Analysis + Recommendations
````

## 📁 Project Structure

```text
AI-Internet-Quality-Analyzer/
│
├── backend/
│   ├── ai_analyzer.py
│   ├── fuzzy_logic.py
│   ├── main.py
│   ├── network_test.py
│   └── test_fuzzy.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── streamlit_app.py
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Run Locally

### 1. Clone

```bash
git clone https://github.com/Jeyasuriya-pillai/AI-Internet-Quality-Analyzer.git
cd AI-Internet-Quality-Analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Streamlit Application

```bash
python -m streamlit run streamlit_app.py
```

The application will open locally at:

```text
http://localhost:8501
```

### 6. Run Original FastAPI Version

```bash
cd backend
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

The original HTML frontend can be opened using **VS Code Live Server**.

## 🔑 Gemini API Key

The application allows the user to enter their own Gemini API key for AI analysis.

**Never upload API keys, `.env`, `venv/`, or `__pycache__/` to GitHub.**

## 🚧 Project Status

**Active Development**

Current features include:

* ✅ Network Testing
* ✅ Fuzzy Logic
* ✅ Quality Score
* ✅ LangChain Integration
* ✅ Gemini AI Analysis
* ✅ Use Case Analysis
* ✅ AI Recommendations
* ✅ Streamlit Web Application
* ✅ Public Deployment
* 🚧 Historical Monitoring
* 🚧 Download/Upload Speed Testing

## 👨‍💻 Developer

**Jeyasuriya**
B.Sc. Information Technology

### Project

**AI-Based Internet Connection Quality Analyzer using AI/LLM (LangChain) + Fuzzy Logic**

---

⭐ **NetSense AI — Making Internet Quality Easier to Understand.**
