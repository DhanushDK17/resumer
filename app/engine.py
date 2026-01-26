from google import genai
import logging
from prompt import generate_prompt
from models import Experience, ExperienceSection

client = genai.Client()

def generate_with_gemini(job_description: str, resume_text: str) -> ExperienceSection:
    prompt = generate_prompt(job_description, resume_text)
    model = "gemini-2.5-flash"
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ExperienceSection.model_json_schema()
        }
    )

    if response.text:
        experiences = ExperienceSection.model_validate_json(response.text)
        return experiences
    else:
        logging.error("No response text from Gemini.")
        return ExperienceSection(experiences=[])