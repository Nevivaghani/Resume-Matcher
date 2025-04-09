import json
import re
import time
# import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.docstore.document import Document

from app.core.llm import llm
from app.core.db import matches_collection

# Updated prompt with RAG context
template = """
You are a highly intelligent assistant designed to extract, categorize, and compare specific information from resumes.
Use the context below to improve your understanding and responses.

### Context (Job Knowledge Base):
{context}

### Part 1: Extract Skills
1. Ignore the following sections completely:
- Languages

2. Extract skills only from these sections:
- Technical Skills
- Skills
- Work Experience
- Projects
- Courses
- Certifications
- Achievements
- Technologies
- Tools

3. Skills can be any specific tools, technologies, programming languages, methodologies, or frameworks mentioned in the context of what the candidate has worked on or achieved.

### Part 2: Categorize Skills
Use the following job description (in JSON format):
{job_desc}

Categorize the extracted skills into:
- Primary Skills: Skills that are most critical and frequently mentioned in the job description's primary skills section.
- Secondary Skills: Skills that are important but less than primary skills, frequently mentioned in the secondary skills section.
- Project Skills: Skills specifically related to projects, frequently mentioned in the project skills section.

### Part 3: Compare Skills and Calculate Matching Scores
Compare the categorized skills with the job description skills and calculate the matching scores for each category using a similarity method (e.g., cosine similarity). The scores should be between 0.00 and 100.00.

Also include how many skills matched in each category and why some may have been missed.

### Part 4: Output
Output the results in JSON format:

{{
  "job_title": "<job title here>",
  "extracted_skills": {{
    "primary_skills": [...],
    "secondary_skills": [...],
    "project_skills": [...]
  }},
  "score": {{
    "primary_skills_score": ...,
    "secondary_skills_score": ...,
    "project_skills_score": ...
  }},
  "final_score": ...
}}

Resume content:
{resume_text}
"""

prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

# Clean LLM response for valid JSON
def clean_llm_response(response: str) -> str:
    if response.strip().startswith("```"):
        response = response.strip().strip("```").strip("json").strip()

    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise ValueError("No valid JSON found in LLM response")

# FAISS index path for vector store
# FAISS_INDEX_PATH = "app/data/faiss_index"

# # Build vector store using user-provided job descriptions
# def build_vector_store(jobs):
#     if os.path.exists(FAISS_INDEX_PATH):
#         return FAISS.load_local(FAISS_INDEX_PATH, HuggingFaceEmbeddings(), allow_dangerous_deserialization=True)

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     docs = []

#     for job in jobs:
#         job_title = job.get("job_title", "")
#         jd_text = json.dumps(job)
#         chunks = text_splitter.split_text(jd_text)
#         for chunk in chunks:
#             docs.append(Document(page_content=chunk, metadata={"job_title": job_title}))

#     vector_store = FAISS.from_documents(docs, embedding=embeddings)
#     vector_store.save_local(FAISS_INDEX_PATH)
#     return vector_store

# Retrieve relevant job context using resume_text
# def retrieve_job_context(resume_text, vector_store, k=3):
#     embeddings = HuggingFaceEmbeddings()
#     return vector_store.similarity_search(resume_text, k=k)

# Main function to match a resume with job descriptions
def match_resume_with_job(resume_text, jobs):
    # Ensure jobs is a list of dicts
    if isinstance(jobs, str):
        try:
            jobs = json.loads(jobs)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string passed as job descriptions.")

    if not isinstance(jobs, list) or not all(isinstance(job, dict) for job in jobs):
        raise ValueError("Job descriptions must be a list of dictionaries.")

    results = []

    # Build vector store and get RAG context
    # vector_store = build_vector_store(jobs)
    # rag_context_docs = retrieve_job_context(resume_text, vector_store)
    # rag_context = "\n".join([doc.page_content for doc in rag_context_docs])
    rag_context = "\n\n".join([json.dumps(job, indent=2) for job in jobs])
    # print("🎯 Job Description Sent to LLM:", json.dumps(job, indent=2))
    for job in jobs:
        try:
            response = chain.run(
                resume_text=resume_text,
                job_desc=json.dumps(job),
                context=rag_context
            )

            time.sleep(3)
            print("Raw LLM response:", response)

            cleaned_response = clean_llm_response(response)
            parsed_response = json.loads(cleaned_response)

            parsed_response["job_title"] = job.get("job_title")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!Parsed response:", type(parsed_response))

            matches_collection.insert_one(parsed_response)

            results.append(parsed_response)

        except json.JSONDecodeError as e:
            print(f"JSON decode error for job '{job.get('title', 'N/A')}': {e}")
            print("Original response:", response)
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

    return sorted(results, key=lambda x: x['final_score'], reverse=True)
