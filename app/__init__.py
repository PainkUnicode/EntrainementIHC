# app/__init__.py
import os
from flask import Flask
import boto3
aws_access_key_id = 'AKIA6PN5NTY2E67H2T56'
aws_secret_access_key = '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'
region_name = 'eu-central-1'

app = Flask(__name__, template_folder='templates')

# Définissez la configuration pour le dossier d'uploads et le dossier de sortie des images
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'uploads', 'output_frames')
app.config['S3'] = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Importez le module d'extraction d'images
from app import video_extraction

# Importez les routes après l'initialisation de Flask
from app import routes