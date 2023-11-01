from flask import Flask
from flask_cors import CORS
import os
import importlib

app = Flask(__name__)
CORS(app)


def load_api_modules():
    api_folder_path = os.path.join(os.path.dirname(__file__), 'api')
    for folder in os.listdir(api_folder_path):
        folder_path = os.path.join(api_folder_path, folder)
        if os.path.isdir(folder_path):
            index_path = os.path.join(folder_path, 'index.py')
            if os.path.isfile(index_path):
                try:
                    module = importlib.import_module(f'api.{folder}.index')
                    app.register_blueprint(module.bp, url_prefix=f'/{folder}')
                    print(f'Dynamic route loaded: /{folder}')
                except ImportError as e:
                    print(f'Error loading index file for {folder}: {e}')
                    continue


if __name__ == '__main__':
    load_api_modules()
    app.run(debug=True)