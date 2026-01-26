from pydantic import BaseModel, Field
from typing import List, Optional

class TextSegment(BaseModel):
    """
    Represents a segment of text in a resume, with an option to make it bold.
    This allows for fine-grained control over text formatting, enabling specific
    words or phrases within a larger text block (like a bullet point) to be
    emphasized.
    """
    text: str = Field(..., description="The actual text content of the segment.")
    bold: bool = Field(default=False, description="Set to True to make the text bold.")

class Experience(BaseModel):
    """
    Defines the structure for a single experience entry in the resume. This includes
    details about the company, role, and duration of employment, along with a list

    of achievements or responsibilities presented as bullet points. Each bullet
    point can contain formatted text.
    """
    company: str = Field(..., description="The name of the company where the experience was gained.")
    role: str = Field(..., description="The title or role held at the company.")
    duration: str = Field(..., description="The time period of the employment (e.g., 'Jan 2020 - Dec 2022').")
    bullets: Optional[List[List[TextSegment]]] = Field(default=None, description="A list of bullet points. Each bullet is a list of text segments, allowing for mixed normal and bold text.")

class ExperienceSection(BaseModel):
    """
    Represents the entire experience section of a resume, which consists of multiple
    experience entries.
    """
    experiences: List[Experience] = Field(..., description="A list of experience entries in the resume.")

class Project(BaseModel):
    """
    Represents a single project entry, with support for formatted text in its description.
    """
    name: str = Field(..., description="The name or title of the project.")
    description: List[TextSegment] = Field(..., description="A description of the project, composed of text segments that can be normal or bold.")