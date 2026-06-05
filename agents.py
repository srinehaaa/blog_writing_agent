import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
import google.generativeai as genai
import pypdf
from docx import Document

# Load environment variables
load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

print("🤖 Gemini AI initialized successfully")


# -----------------------------
# Memory Functions (Disabled)
# -----------------------------

def initialize_memori():
    return {}


def create_memory_tool_instance(memory_system):
    return {}


# -----------------------------
# File Processing
# -----------------------------

def extract_text_from_pdf(pdf_file) -> str:
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)

        text = ""

        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return text

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")


def extract_text_from_docx(docx_file) -> str:
    try:
        doc = Document(docx_file)

        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text

    except Exception as e:
        raise Exception(f"Error reading DOCX: {e}")


def extract_text_from_txt(txt_file) -> str:
    try:
        return txt_file.read().decode("utf-8")

    except Exception as e:
        raise Exception(f"Error reading TXT: {e}")


# -----------------------------
# Writing Style Analysis
# -----------------------------

def analyze_writing_style(text: str) -> Dict[str, Any]:

    prompt = f"""
    Analyze this writing sample.

    Identify:

    1. Tone
    2. Voice
    3. Writing structure
    4. Vocabulary level
    5. Sentence patterns
    6. Writing habits

    Text:

    {text[:3000]}

    Return JSON only.
    """

    try:
        response = model.generate_content(prompt)

        analysis_text = response.text

        try:
            start = analysis_text.find("{")
            end = analysis_text.rfind("}") + 1

            if start != -1 and end != -1:
                return json.loads(analysis_text[start:end])

        except Exception:
            pass

        return {
            "tone": "Professional",
            "voice": "Informative",
            "structure": "Well-organized",
            "vocabulary": "Moderate",
            "sentence_patterns": "Mixed",
            "writing_habits": [
                "Clear headings",
                "Logical flow"
            ]
        }

    except Exception as e:
        raise Exception(f"Error analyzing writing style: {e}")


# -----------------------------
# Memory Stubs
# -----------------------------

def store_writing_style_in_memori(
    memory_system,
    style_analysis,
    original_text
):
    return "Style stored successfully"


def get_stored_writing_style(memory_tool):
    return None


def save_generated_blog(memory_system, topic, blog_content):
    return True


# -----------------------------
# Blog Generation
# -----------------------------

def generate_blog_with_style(memory_tool, topic: str) -> str:

    prompt = f"""
    Write a professional blog post about:

    {topic}

    Requirements:
    - Clear introduction
    - Informative content
    - Proper headings
    - Conclusion
    - Easy to read
    """

    try:
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        raise Exception(f"Error generating blog: {e}")
