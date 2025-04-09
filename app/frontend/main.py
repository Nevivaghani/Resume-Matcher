import streamlit as st
import requests
import json

st.set_page_config(page_title="Resume Matcher", layout="wide")

st.title("🤖 AI-Powered Resume Matcher")
st.markdown("Upload your resume and paste your job description JSON below.")

with st.form("job_form"):
    jd_json = st.text_area("Paste Job Description JSON", height=250)
    uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
    submitted = st.form_submit_button("Match Resume")

if submitted and uploaded_file:
    try:
        job_dict = json.loads(jd_json)
        files = {
            "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
        }

        data = {
            "job_data": json.dumps(job_dict)  # Send as single form field
        }

        with st.spinner("Analyzing resume... Please wait"):
            response = requests.post("http://localhost:8000/upload-resume", files=files, data=data)

        if response.status_code == 200:
            data = response.json()
            if not data.get("top_matched_jobs"):
                st.warning("No suitable matches found.")
            else:
                st.success("Top Job Match:")

                for idx, job in enumerate(data["top_matched_jobs"], start=1):
                    with st.expander(f"🔹 {idx}. {job['job_title']} (Score: {job['final_score']:.2f}%)", expanded=True):
                        st.subheader("🧠 Extracted Skills")
                        col1, col2, col3 = st.columns(3)
                        col1.markdown("**Primary Skills:**")
                        col1.write(job["extracted_skills"].get("primary_skills", []))

                        col2.markdown("**Secondary Skills:**")
                        col2.write(job["extracted_skills"].get("secondary_skills", []))

                        col3.markdown("**Project Skills:**")
                        col3.write(job["extracted_skills"].get("project_skills", []))

                        st.subheader("📊 Score Breakdown")
                        st.markdown("**Overall Score:**", unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='font-size: 28px; font-weight: bold; color: #4CAF50;'>{job['final_score']}%</div>",
                            unsafe_allow_html=True
                        )
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        st.error("Invalid JSON. Please check your input.")
    except requests.exceptions.ConnectionError:
        st.error("Backend server not available. Please make sure FastAPI is running.")
elif submitted and not uploaded_file:
    st.warning("Please upload a resume before submitting.")
