from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
import json

app = Flask(__name__)
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel("gemini-2.5-flash")
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    current_year = datetime.now().year
    job_description = request.form["job_description"]

    prompt = f"""
Current Year: {current_year}
Assume today's date is June {current_year}.

Analyze this resume against the following Job Description.

Job Description:
{job_description}

Give:

1. ATS Score out of 100
2. Strengths
3. Weaknesses
4. Missing Skills
5. Suggestions

ATS Score should be displayed as:

<h2>ATS Score</h2>
<p>[ATS_SCORE]/100</p>

Give the analysis in clean HTML format.

Use exactly these sections:

<h2>ATS Score</h2>
<p>Score here</p>

<h2>Strengths</h2>
<ul>
<li>Point</li>
</ul>

<h2>Weaknesses</h2>
<ul>
<li>Point</li>
</ul>

<h2>Missing Skills</h2>
<ul>
<li>Point</li>
</ul>

<h2>Suggestions</h2>
<ul>
<li>Point</li>
</ul>

Important:
- Return only HTML.
- Do not use markdown.
- Do not use ** or ###.
- Keep points short and clear.

Resume:
{text}
"""
    print("Current Year =", current_year)
    response = model.generate_content(prompt)
    # data = json.loads(response.text)

    print(response.text)

    return render_template(
    "result.html",
    result=response.text
    )

if __name__ == "__main__":
    app.run(debug=True)
