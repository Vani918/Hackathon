import os
from flask import Flask, render_template, request
import pdfplumber
import docx
from werkzeug.utils import secure_filename
import google.generativeai as genai

# Set your API key
os.environ["AIzaSyC9rVrHV6Ji9k5T9PwrPjr4ncGymVqSycw"] = "AIzaSyC9rVrHV6Ji9k5T9PwrPjr4ncGymVqSycw"
genai.configure(api_key=os.environ["AIzaSyC9rVrHV6Ji9k5T9PwrPjr4ncGymVqSycw"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text
    elif ext == 'docx':
        doc = docx.Document(file_path)
        text = ' '.join([para.text for para in doc.paragraphs])
        return text
    elif ext == 'txt':
        with open(file_path, 'r') as file:
            return file.read()
    return None

def generate_speech(input_text, speech_type):
    prompt = f"""
    You are an AI assistant generating a {speech_type} on the following topic:
    '{input_text}'
    Please structure the speech with:
    - An engaging introduction
    - Well-organized main points
    - A strong conclusion
    Ensure clarity, coherence, and a smooth flow of ideas.
    """
    response = model.generate_content(prompt).text.strip()
    return response

def save_speech_to_file(speech, filename):
    results_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    with open(results_path, 'w') as f:
        f.write(speech)
    return results_path

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/generate', methods=['POST'])
def generate_speech_route():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        text = extract_text_from_file(file_path)

        if text:
            speech_type = request.form['speech_type']
            speech = generate_speech(text, speech_type)

            txt_filename = f"generated_speech_{filename.rsplit('.', 1)[0]}.txt"
            save_speech_to_file(speech, txt_filename)

        return render_template('result.html', speech=speech, txt_filename=txt_filename)
    return "Invalid file format"

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['RESULTS_FOLDER']):
        os.makedirs(app.config['RESULTS_FOLDER'])
    app.run(debug=True)
