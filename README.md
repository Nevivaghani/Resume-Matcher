
# Project Title

A brief description of what this project does and who it's for

# 🤖 AI-Powered Resume Matcher

This project is an AI-based Resume Matcher that analyzes a candidate’s resume, extracts skills using LLMs (e.g., OpenAI/GPT), and compares them to a provided Job Description (JD) to compute a skill match score.



## 🧰 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI Engine**: LangChain + LLM (e.g., OpenAI, HuggingFace)
- **Parsing**: PDF/Text resume loader
- **Database**: MongoDB (via `matches_collection`)
- **Embedding Model**: HuggingFace (MiniLM-L6-v2 for FAISS-based RAG – optional)
- **Prompt Engineering**: Custom prompt with context injection

---

## 🔧 Features

- Upload a resume (PDF or TXT)
- Paste a structured JSON Job Description
- Extract & categorize skills using an LLM
- Score match across:
  - Primary Skills
  - Secondary Skills
  - Project Skills
- Return total and category-wise matching score
- Simple UI built with Streamlit

---


## 🚀 How It Works

1. User uploads a resume
2. User provides a JD as a structured JSON like:


```json
{
  "job_title": "AI/ML Engineer",
  "primarySkills": ["Python", "Machine Learning"],
  "secondarySkills": ["Scikit-learn", "Keras"],
  "projectSkills": ["CNN", "LSTM", "Data Preprocessing"]
}

```

💻 Setup Instructions
1. Clone the repo

git clone https://github.com/Nevivaghani/Resume-Matcher.git
cd resume-matcher

2. Install backend dependencies

poetry install

3. Start FastAPI backend

poetry run uvicorn app.main:app --reload     

4. Run Streamlit frontend

poetry run streamlit run app/frontend/main.py

## Screenshots


![App Screenshot][def]

![App Screenshot][def2]



[def]: ./assets/resume_matcher1.png
[def2]: ./assets/resume_matcher2.png