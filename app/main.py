from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from database import create_resumes_table, insert_resume
from engine import generate_with_gemini
from resume import replace_section

import docx
import logging
import requests


app = FastAPI()

class Job(BaseModel):
    url: str

class Resume(BaseModel):
    file_path: str


def setup_logging():
    """Sets up logging to a file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler(),
        ],
    )

setup_logging()

def scrape_job_description(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")
        # This is a generic way to get text. It might need to be adjusted for specific websites.
        # We can try to find common tags for job descriptions like 'div' with id 'job-description' or class 'job-description'
        job_description = soup.find("div", id="job-description")
        if not job_description:
            job_description = soup.find("div", class_="job-description")

        if job_description:
            return job_description.get_text()
        else:
            # As a fallback, get all the text from the body
            if soup.body:
                return soup.body.get_text()
            else:
                logging.error("No body tag found in the HTML.")
                return ""
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping job description: {e}")
        return ""

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def sanitize_filename(url: str) -> str:
    """
    Sanitizes a URL to create a valid filename.
    """
    # Get the last part of the URL
    filename = url.split('/')[-1]
    # Remove invalid characters
    invalid_chars = ['?', '=', '&', ':', '/', '\\']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

@app.on_event("startup")
def on_startup():
    create_resumes_table()

@app.post("/generate-resume/", response_model=Resume)
async def generate_resume(job: Job):
    # 1. Scrape job description from job.url
    job_description = scrape_job_description(job.url)
    if not job_description:
        return {"error": "Could not scrape job description"}

    # 2. Load the source resume template
    try:
        source_resume_path = "/app/resume_templates/source_resume.docx"
        resume_text = read_docx(source_resume_path)
        doc = docx.Document(source_resume_path)
    except FileNotFoundError:
        return {"error": "Source resume not found"}

    # 3. Use Gemini to generate ATS-beating experience and skills
    new_experience = generate_with_gemini(job_description, resume_text)

    # 4. Modify the resume
    replace_section(doc, "WORK EXPERIENCE", new_experience)

    # 5. Save the new resume
    file_path = f"generated_resumes/resume_for_{sanitize_filename(job.url)}.docx"
    doc.save(file_path)

    # 6. Store information in the database
    insert_resume(job.url, file_path)
    return Resume(file_path=file_path)

@app.get("/")
async def root():
    return {"message": "Welcome to the Resumer API!"}
