import streamlit as st
from resume_generator import generate_resume, generate_cover_letter, analyze_ats_match
from pdf_utils import save_resume_as_pdf, save_resume_as_docx

st.set_page_config(page_title="AI Career Assistant", page_icon="📄", layout="wide")

# Session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "cover_letter_text" not in st.session_state:
    st.session_state.cover_letter_text = ""

if "ats_analysis" not in st.session_state:
    st.session_state.ats_analysis = ""

# Sidebar
with st.sidebar:
    st.header("📌 Instructions")
    st.write("""
    1. Enter your details carefully.
    2. Paste the job description.
    3. Choose a resume template style.
    4. Generate a tailored resume.
    5. Generate a cover letter and ATS analysis.
    """)

    st.header("💡 Tips")
    st.write("""
    - Use real skills and projects only
    - Keep summary short and professional
    - Paste the full job description
    - Choose Student/Fresher for internship roles
    """)

# Title
st.title("📄 AI Resume + Cover Letter + ATS Analyzer")
st.write("Create job-specific application documents with AI.")

# Template selector
st.subheader("🎨 Resume Template")
template_style = st.selectbox(
    "Choose Resume Style",
    ["Classic", "Modern", "Student/Fresher"]
)

# Layout for inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    st.subheader("🧠 Professional Profile")
    summary = st.text_area("Professional Summary", height=120)
    skills = st.text_area(
        "Skills",
        height=120,
        placeholder="Python, Machine Learning, SQL, Streamlit, TensorFlow"
    )

with col2:
    st.subheader("🎓 Academic / Career Details")
    education = st.text_area("Education", height=120)
    projects = st.text_area("Projects", height=150)
    experience = st.text_area("Experience / Internships / Certifications", height=150)

st.subheader("💼 Job Description")
job_description = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder="Paste the full internship or job description here"
)

# Buttons row
st.subheader("⚙️ Actions")
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    generate_resume_btn = st.button("Generate Resume", use_container_width=True)

with btn_col2:
    generate_cover_letter_btn = st.button("Generate Cover Letter", use_container_width=True)

with btn_col3:
    analyze_ats_btn = st.button("Analyze ATS Match", use_container_width=True)

required_fields_filled = all([
    name, email, phone, job_description, skills, education, projects
])

# Resume generation
if generate_resume_btn:
    if required_fields_filled:
        with st.spinner("Generating your tailored resume..."):
            st.session_state.resume_text = generate_resume(
                name,
                email,
                phone,
                job_description,
                summary,
                skills,
                education,
                projects,
                experience,
                template_style
            )
        st.success("Resume generated successfully.")
    else:
        st.warning("Please fill in all important fields before generating the resume.")

# Cover letter generation
if generate_cover_letter_btn:
    if required_fields_filled:
        with st.spinner("Generating your tailored cover letter..."):
            st.session_state.cover_letter_text = generate_cover_letter(
                name, email, phone, job_description, summary, skills, education, projects, experience
            )
        st.success("Cover letter generated successfully.")
    else:
        st.warning("Please fill in all important fields before generating the cover letter.")

# ATS analysis
if analyze_ats_btn:
    if job_description and st.session_state.resume_text:
        with st.spinner("Analyzing ATS match..."):
            st.session_state.ats_analysis = analyze_ats_match(
                job_description, st.session_state.resume_text
            )
        st.success("ATS analysis completed.")
    else:
        st.warning("Please generate a resume first and make sure the job description is filled.")

# Output tabs
st.subheader("📂 Output")
tab1, tab2, tab3 = st.tabs(["Resume", "Cover Letter", "ATS Analysis"])

with tab1:
    if st.session_state.resume_text:
        st.text_area("Generated Resume", st.session_state.resume_text, height=500)

        pdf_file = save_resume_as_pdf(st.session_state.resume_text)
        docx_file = save_resume_as_docx(st.session_state.resume_text)

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Download Resume as PDF",
                    data=file,
                    file_name="generated_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        with download_col2:
            with open(docx_file, "rb") as file:
                st.download_button(
                    label="Download Resume as DOCX",
                    data=file,
                    file_name="generated_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
    else:
        st.info("Your generated resume will appear here.")

with tab2:
    if st.session_state.cover_letter_text:
        st.text_area("Generated Cover Letter", st.session_state.cover_letter_text, height=450)
    else:
        st.info("Your generated cover letter will appear here.")

with tab3:
    if st.session_state.ats_analysis:
        st.text_area("ATS Match Analysis", st.session_state.ats_analysis, height=400)
    else:
        st.info("Your ATS analysis will appear here.")