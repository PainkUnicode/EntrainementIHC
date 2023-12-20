# app/__init__.py
import os
from flask import Flask
import boto3

aws_access_key_id = 'AKIA6PN5NTY2E67H2T56'
aws_secret_access_key = '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'
region_name = 'eu-central-1'

app = Flask(__name__, template_folder=os.getcwd())

# Définissez la configuration pour le dossier d'uploads et le dossier de sortie des images
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'app', 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'app', 'uploads', 'output_frames')
app.config['COLLAGE_FOLDER'] = os.path.join(os.getcwd(),'app','uploads', 'output_collage')
# Importez le module d'extraction d'images
from app import video_extraction

# Importez les routes après l'initialisation de Flask
from app import routes