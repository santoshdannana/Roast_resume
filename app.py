from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
# import firebase_admin
# from firebase_admin import credentials, firestore
from gemini_helper import get_roast

# Load env and configure Gemini FIRST
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase-key.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()


app = Flask(__name__)

# ========= Helper Functions ==========

from docx import Document
import fitz  # PyMuPDF

def extract_resume_text(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()

    elif filename.endswith(".docx"):
        file.seek(0)  # Ensure pointer is at the beginning
        document = Document(file)
        text = "\n".join([para.text for para in document.paragraphs])
        return text.strip()

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or Word (.docx) document.")


def build_roast_prompt(resume_text, persona, intensity):
    # Persona definitions
    persona_filters = {
        "comedian": (
            "You are a sharp, sarcastic stand-up comedian who dissects resumes like they're part of your act. You roast every line with clever, observational humor and punchlines that make people laugh and wince at the same time."
        ),
        "grandma": (
            "You are a brutally honest but loving grandmother who’s seen it all. You speak your mind without a filter and poke fun with warmth and cutting one-liners. You call out exaggerations and resume fluff like you’re scolding your grandchild at dinner."
        ),
        "robot": (
            "You are a hyper-logical AI programmed to scan resumes and identify inconsistencies, repetition, overconfidence, and exaggerated skills. Your tone is dry and deadpan, but somehow sarcastic — and your roast lands like a performance review with attitude."
        ),
        "roommate": (
            "You’re their overly honest roommate who’s seen them work (or not). You mock the resume like you’ve watched them write it in their pajamas. You speak casually, with inside-joke energy and ruthless honesty."
        ),
        "teacher": (
            "You are a disappointed high school teacher who expected more. You tear through this resume like a red pen through a final essay. Your tone is sharp, disappointed, and sarcastically educational."
        ),
        "villain": (
            "You are a theatrical movie villain who tears people apart using wit, venom, and brilliant vocabulary. You don’t yell — you mock, and you do it with terrifying confidence and style."
        )
    }

    # Roast levels
    roast_levels = {
        "mild": (
            "Keep it light and playful. Be teasing and witty, like mocking a close friend — but never mean. Make gentle fun of resume clichés and overused phrases."
        ),
        "medium": (
            "Be confident and clever. Point out resume fluff, vague language, and inflated achievements with humor that stings a little — but still feels fair."
        ),
        "hot": (
            "Hit hard. Roast buzzwords, braggy lines, stacked skills, and try-hard project descriptions. Don’t hold back. Be funny, insightful, and cutting."
        ),
        "nuclear": (
            "Roast like you're trying to make the person *question their entire approach*. Tear through every line with ruthless creativity. Call out lies, fluff, and grandstanding. Be savage — but smart, and never cruel."
        )
    }

    # Final prompt
    prompt = f"""{persona_filters[persona]}

    Roast the following resume based on its *exact content*. Do not summarize or generalize — react directly to what you read. Your goal is to make it feel personal, like you're speaking to the person after reading every single line.

    Use {roast_levels[intensity]}

    🧨 Instructions:
    - DO NOT copy or repeat phrases from the resume. Instead, rephrase and mock them in your own words.
    - DO NOT include stage directions, scene descriptions, emojis, or formatting (bold/italics/lists).
    - Speak in paragraphs, like a real person ranting or roasting out loud.
    - Use *asterisks* only to emphasize words (like *this*).
    - Absolutely NO compliments at the end. This is not a feedback session — it’s a roast.

    Focus on anything that feels generic, exaggerated, too perfect, overloaded with buzzwords, or clearly there just to impress.

    Rip it apart. Make it sting. Make it smart.
    Assume the person reading this is from India or has an Indian background. Make cultural references that make sense to an Indian audience — like college ranking obsession, overused project buzzwords, common IT resume fluff, or typical phrases seen in Indian job applications.

    Avoid American pop culture references that won’t land. Instead, focus on resume habits common among Indian software developers.
 
    Based on the name and locations guess if the person is north indian or south indian and use those references and use movie references and political references also.
    If the resume has only United states in their work expereince location and name is like american name strictly use america references.
    If the resume mentions Indian cities, universities, or companies — roast them from that angle too. Keep it sharp, relatable, and relevant.
    Assume this resume is from someone based in India or trained in the Indian education system. Tailor your references and commentary accordingly.

    Here’s the resume:

    {resume_text}
    """
    return prompt




# ========== Routes ==========

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast():
    try:
        # Form inputs
        file = request.files['resume']
        persona = request.form['persona']
        intensity = request.form['intensity']
        allowed_extensions = ('.pdf', '.docx')
        if not file.filename.lower().endswith(allowed_extensions):
            return "Unsupported file type. Please upload a .pdf or .docx resume.", 400

        # Parse resume
        resume_text = extract_resume_text(file)

        # Build and send prompt
        prompt = build_roast_prompt(resume_text, persona, intensity)
        print(prompt)
        roast_raw = get_roast(prompt)
        roast_text = markdown_to_html(roast_raw)

        # doc_ref = db.collection("roasts").add({
        #     "resume_text": resume_text,
        #     "prompt": prompt,
        #     "roast": roast_text,
        #     "timestamp": firestore.SERVER_TIMESTAMP
        # })


    except Exception as e:
        roast_text = f"⚠️ Error generating roast: {e}"

    return render_template('result.html', roast=roast_text)

import re


def markdown_to_html(text):
    import re
    text = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', text)
    paragraphs = [f"<p>{para.strip()}</p>" for para in text.split("\n\n")]
    return "".join(paragraphs)

# ========== Run App ==========

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

