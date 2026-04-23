from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
    flask
flask-cors
google-generativeai
python-dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re

app = Flask(__name__)
CORS(app)

# ✅ Use environment variable (IMPORTANT)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')


def extract_json(text):
    """Extract JSON from AI response safely"""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        resume = data.get('resume')
        job_desc = data.get('jobDescription')

        # ✅ Basic validation
        if not resume or not job_desc:
            return jsonify({"error": "Missing input"}), 400

        prompt = f"""
        Compare this Resume to the Job Description.

        Resume:
        {resume}

        Job Description:
        {job_desc}

        Return ONLY valid JSON in this format:
        {{
          "matchScore": number (0-100),
          "missingSkills": ["skill1", "skill2"],
          "matchingSkills": ["skill1", "skill2"],
          "advice": "short improvement advice"
        }}
        """

        response = model.generate_content(prompt)

        # ✅ Extract JSON safely
        parsed = extract_json(response.text)

        if not parsed:
            return jsonify({"error": "AI response parsing failed"}), 500

        return jsonify(parsed)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Server error"}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
