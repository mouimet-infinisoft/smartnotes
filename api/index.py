from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from flask_cors import CORS 
import pytesseract
from PIL import Image
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_KEY')

@app.route('/smart', methods=['POST'])
def smart():
    file = request.files['image']
    if not file:
        return jsonify({'error': 'no file uploaded'}), 400

    image = Image.open(file)
    text = pytesseract.image_to_string(image)

    # Define the template for the report
    template = """
    Considérant les informations ci-dessous, tu va générer des notes structurées en français. Tu va formatter en utilisant du HTML et découper en section avec des paragraphes et des titres.

    Informations: 
    {processed_text}

    Titre: Notes d'observation
    
    """

    # Substitute the OCR processed text into the template
    report_text = template.format(processed_text=text)

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": report_text}
    ]
    )

    generated_report = completion.choices[0].message.content
    return jsonify({'report': generated_report})

if __name__ == '__main__':
    app.run(debug=True)
