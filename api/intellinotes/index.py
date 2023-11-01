from flask import Blueprint, jsonify, request
import requests
from dotenv import load_dotenv
import os
import openai

bp = Blueprint('intellinotes', __name__)

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')
api_key = os.getenv('OCR_KEY')

def ocr_space_file(file, overlay=False, language='fre'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'filetype': file.content_type.split('/')[-1],
        'language': language
    }
    r = requests.post('https://api.ocr.space/parse/image',
                      files={'image': file},
                      data=payload
                      )
    t = r.json()

    return t["ParsedResults"][0]["ParsedText"]


@bp.route('/smart', methods=['POST'])
def smart():
    file = request.files['image']
    if not file:
        return jsonify({'error': 'no file uploaded'}), 400

    text = ocr_space_file(file)

    template = """
    Consider the information below, you will generate structured notes in English. You will format it using HTML and divide it into sections with paragraphs and headings.

    Information: 
    {processed_text}

    Title: Observation Notes
    
    """

    report_text = template.format(processed_text=text)

    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=report_text,
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None
    )

    generated_report = completion.choices[0].text.strip()
    return jsonify({'report': generated_report})