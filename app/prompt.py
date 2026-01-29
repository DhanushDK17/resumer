def generate_prompt(job_description: str, resume_text: str) -> str:
    return f"""
        You are an expert resume writer specializing in creating ATS-optimized resumes.
        You will find the flavor of candidate that matches the job description provided.
        You will then rewrite the "Experience" section of the provided resume to better align with the job description.
        Given the following job description and resume, please generate a new "Experience" section for the resume that is tailored to the job description.
        The new "Experience" section should be ATS-friendly and highlight the most relevant skills and experiences based on the job description.
        Do not include any other sections from the resume. Only the "Experience" section. Follow the rules as belows.
        1. Do not copy the same text as already given in the resume.
        2. Use bullet points to list points under each experience
        3. Make sure to use action verbs and quantify achievements where possible.
        4. Keep the tone professional and concise.
        5. Ensure the formatting is suitable for a Word document.
        6. The output you generate should only be in the same format as the resume text provided to you
        7. You can make up responsibilities in the output based on the skills listed in the JD
        8. You will generate atleast 8 bullet points for each experience listed in the resume

        #####Job Description#####
        {job_description}

        #####Resume#####
        {resume_text}

        Please extract the experience section from the text you generate
        """