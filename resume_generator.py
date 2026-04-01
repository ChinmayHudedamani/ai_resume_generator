import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")

api_key = get_api_key()

if not api_key:
    raise ValueError(
        "OpenAI API key not found. Set OPENAI_API_KEY in .env for local use "
        "or in Streamlit secrets for deployment."
    )

client = OpenAI(api_key=api_key)

def generate_resume(name, email, phone, job_description, summary, skills, education, projects, experience, template_style):
    style_instructions = {
        "Classic": """
Use a traditional professional resume style.
Keep the tone formal, structured, and concise.
Focus on clarity and professionalism.
""",
        "Modern": """
Use a modern professional resume style.
Make the summary and project descriptions slightly more impactful.
Highlight achievements, technical strengths, and practical value.
""",
        "Student/Fresher": """
Use a student/fresher-friendly resume style.
Emphasize education, academic projects, certifications, technical skills, and potential.
Make the profile suitable for internships and entry-level roles.
"""
    }

    selected_style_instruction = style_instructions.get(template_style, style_instructions["Classic"])

    prompt = f"""
Create a professional ATS-friendly resume tailored specifically to the following job description.

Resume Template Style:
{template_style}

Style Guidance:
{selected_style_instruction}

Job Description:
{job_description}

Candidate Information:
Name: {name}
Email: {email}
Phone: {phone}

Professional Summary:
{summary}

Skills:
{skills}

Education:
{education}

Projects:
{projects}

Experience:
{experience}

Instructions:
1. Tailor the resume to match the job description.
2. Highlight the most relevant technical skills, projects, and experience.
3. Use ATS-friendly keywords naturally from the job description.
4. Keep the tone professional and concise.
5. Structure the resume with clear sections:
   - Contact Information
   - Professional Summary
   - Skills
   - Education
   - Projects
   - Experience / Certifications
6. Do not invent fake achievements.
7. Follow the selected template style carefully.
8. Return only the final resume content.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume writer and ATS optimization specialist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


def generate_cover_letter(name, email, phone, job_description, summary, skills, education, projects, experience):
    prompt = f"""
Write a professional, concise, and tailored cover letter for the following candidate.

Job Description:
{job_description}

Candidate Information:
Name: {name}
Email: {email}
Phone: {phone}

Professional Summary:
{summary}

Skills:
{skills}

Education:
{education}

Projects:
{projects}

Experience:
{experience}

Instructions:
1. Write a formal cover letter tailored to the job description.
2. Highlight the candidate's most relevant skills, education, and projects.
3. Keep it concise and professional.
4. Do not invent fake achievements or fake experience.
5. The tone should be confident but natural.
6. Return only the cover letter content.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert career coach and cover letter writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return response.choices[0].message.content


def analyze_ats_match(job_description, resume_text):
    prompt = f"""
Analyze how well the following resume matches the given job description.

Job Description:
{job_description}

Resume:
{resume_text}

Instructions:
1. Give an ATS match score out of 100.
2. List the matched keywords.
3. List the missing or weak keywords.
4. Give 3 to 5 specific suggestions to improve the resume.
5. Keep the output clear and structured.
6. Return only the analysis.

Format:
ATS Match Score: <score>%

Matched Keywords:
- keyword 1
- keyword 2

Missing Keywords:
- keyword 1
- keyword 2

Suggestions:
1. suggestion 1
2. suggestion 2
3. suggestion 3
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert ATS resume evaluator and career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content