# app/__init__.py
import os
from flask import Flask

app = Flask(__name__, template_folder='templates')

# Définissez la configuration pour le dossier d'uploads et le dossier de sortie des images
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'uploads', 'output_frames')

# Importez le module d'extraction d'images
from app import video_extraction

# Importez les routes après l'initialisation de Flask
from app import routes