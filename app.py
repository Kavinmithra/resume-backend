from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Set up your OpenAI API key
ope= "YOUR_OPENAI_API_KEY"
openai.api_key = ope

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.json
    resume_content = data.get('resume')
    
    if not resume_content:
        return jsonify({'error': 'No resume content provided!'}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f'Analyze this resume: {resume_content}'}
            ]
        )
        analysis = response['choices'][0]['message']['content']
        return jsonify({'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)