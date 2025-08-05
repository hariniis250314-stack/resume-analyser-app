import streamlit as st
import PyPDF2
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import re

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

st.title("📄 Resume Analyzer + Job Match App")

# --- Step 1: Upload Resume ---
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type="pdf")

# --- Step 2: Choose Job Role ---
job_roles = {
    "Data Analyst": ["python", "excel", "sql", "data analysis", "power bi", "statistics"],
    "Machine Learning Engineer": ["python", "tensorflow", "scikit-learn", "deep learning", "pandas", "numpy"],
    "Business Analyst": ["business analysis", "excel", "requirement gathering", "stakeholder management", "data visualization"],
    "Project Manager": ["agile", "scrum", "jira", "project planning", "communication", "risk management"]
}
job_title = st.selectbox("Select a Job Role to Match", list(job_roles.keys()))

if uploaded_file and job_title:
    # --- Step 3: Extract Text ---
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    # Clean and tokenize
    resume_text = resume_text.lower()
    resume_text = re.sub(r'[^\w\s]', '', resume_text)  # Remove punctuation
    resume_tokens = [word for word in resume_text.split() if word not in stop_words]

    # --- Step 4: Analyze ---
    required_skills = job_roles[job_title]
    found_skills = [skill for skill in required_skills if skill in resume_tokens]
    missing_skills = list(set(required_skills) - set(found_skills))
    match_score = int(len(found_skills) / len(required_skills) * 100)

    # --- Step 5: Display Results ---
    st.subheader("✅ Match Score:")
    st.progress(match_score)
    st.write(f"🎯 **{match_score}% match** for the role of **{job_title}**")

    st.subheader("✅ Skills Found in Resume:")
    st.write(found_skills if found_skills else "No relevant skills found.")

    st.subheader("❌ Skills Missing:")
    st.write(missing_skills if missing_skills else "Great! All skills matched.")

    if missing_skills:
        st.subheader("📘 Suggestions to Improve:")
        for skill in missing_skills:
            st.write(f"➡️ Add experience or mention projects involving **{skill}**")
