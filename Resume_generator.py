import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

GOOGLE_API_KEY = "AIzaSyBohMYbSlqO6eAlRmj2HGFNiPZ1zZ4CNnA"
genai.configure(api_key=GOOGLE_API_KEY)

def generate_resume_section(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

def create_pdf(name, email, phone, purpose, summary, skills, experience, education, template):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=20)
    pdf.cell(200, 10, name, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Email: {email} | Phone: {phone}", ln=True, align='C')
    pdf.ln(10)

    def safe_text(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    sections = [
        ("Career Objective", purpose),
        ("Summary", summary),
        ("Skills", skills),
        ("Experience", experience),
        ("Education", education)
    ]

    for title, content in sections:
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, safe_text(content))
        pdf.ln(5)

    return pdf

st.title("🚀 AI-Powered Resume Builder (Google Gemini)")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")

purpose = st.text_area("Career Objective / Purpose", "E.g., Seeking a software engineering role in a fast-paced environment.")
skills = st.text_area("Skills (comma-separated)", "E.g., Python, React, AWS, Agile, SQL")
experience = st.text_area("Experience", "E.g., Worked as a Software Engineer at ABC Corp for 3 years.")
education = st.text_area("Education", "E.g., B.Sc. in Computer Science, Stanford University, 2020")

template_choice = st.selectbox("Choose a Resume Template", ["Modern", "Classic"])

if st.button("Generate Resume"):
    with st.spinner("Generating AI-powered resume..."):
        summary = generate_resume_section(f"Create a professional summary for {name} based on their skills: {skills} and experience: {experience}")
        enhanced_skills = generate_resume_section(f"Format these skills professionally for a resume: {skills}")
        enhanced_experience = generate_resume_section(f"Refine this experience section for a resume: {experience}")
        enhanced_education = generate_resume_section(f"Enhance this education section: {education}")

        st.subheader("Generated Resume")
        st.text_area("Summary", summary, height=100)
        st.text_area("Skills", enhanced_skills, height=100)
        st.text_area("Experience", enhanced_experience, height=150)
        st.text_area("Education", enhanced_education, height=100)

        pdf = create_pdf(name, email, phone, purpose, summary, enhanced_skills, enhanced_experience, enhanced_education, template_choice)
        pdf_file = "resume.pdf"
        pdf.output(pdf_file)

        with open(pdf_file, "rb") as file:
            st.download_button("📥 Download Resume as PDF", file, file_name="resume.pdf", mime="application/pdf")

st.info("Fill in the details and click 'Generate Resume' to create your AI-powered resume!")
