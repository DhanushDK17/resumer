# Resumer

Resumer is an automated tool designed to tailor your resume for specific job applications. It scrapes job descriptions from provided URLs, leverages Google's Gemini AI to rewrite your professional experience to align with the job requirements, and generates a formatted DOCX resume.

## Features

- **Job Description Scraping:** Automatically extracts text from job posting URLs.
- **AI-Powered Customization:** Uses Google Gemini to rewrite resume bullet points, emphasizing relevant skills and keywords.
- **DOCX Formatting:** Updates an existing Word document template while maintaining styles (bolding, lists).
- **History Tracking:** Stores links between job postings and generated resumes in a PostgreSQL database.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL Database
- Google Cloud Project with Gemini API access

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd resumer
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn psycopg2-binary python-docx beautifulsoup4 requests google-genai pydantic
    ```

4.  **Configure Environment Variables:**
    Ensure the following environment variables are set (you can use `export` in your terminal):
    
    *   `GEMINI_API_KEY`: Your Google Gemini API key.
    *   `DATABASE_URL`: Connection string for your PostgreSQL database (e.g., `postgresql://user:password@localhost:5432/resumer_db`).

5.  **Prepare the Resume Template:**
    *   Create a directory `app/resume_templates/`.
    *   Place your base resume file named `source_resume.docx` inside it.
    *   *Note:* The code currently points to `/app/resume_templates/source_resume.docx`. For local development, you may need to update the `source_resume_path` in `app/main.py` to a relative path (e.g., `app/resume_templates/source_resume.docx`).

6.  **Database Initialization:**
    Make sure your PostgreSQL server is running. The application will automatically create the necessary table (`resumes`) on startup.

## Running the Application

Start the server using Uvicorn from the project root:

```bash
uvicorn main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`.

## Usage

To generate a tailored resume, send a POST request to the `/generate-resume/` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/generate-resume/" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/job-posting"}'
```

## Testing

Run the unit tests to verify the resume section replacement logic:

```bash
python app/test_main.py
```