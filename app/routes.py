# app/routes.py
from flask import render_template, request, send_from_directory
from app import app, video_extraction
import os
import random

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    video_folder = 'app/films'  # Remplacez par le chemin de votre dossier vidéo
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

    if not video_files:
        return "Aucun fichier vidéo trouvé dans le dossier"

    # Choisissez aléatoirement un fichier vidéo du dossier
    selected_video = random.choice(video_files)
    video_path = os.path.join(video_folder, selected_video)
    output_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'output_frames')

    os.makedirs(output_folder, exist_ok=True)

    # Appel du script d'extraction d'images
    frame_images = video_extraction.extract_frames(video_path, output_folder)

    # Préparez les chemins complets des images
    full_frame_paths = [os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(image)) for image in frame_images]

    # Appel du script pour coller les images en une seule
    result_image_path = video_extraction.create_collage(full_frame_paths, output_folder)

    return render_template('result.html', result_image=result_image_path, os=os)

    return "Format de fichier non pris en charge"

@app.route('/output_frames/<path:filename>')
def serve_output_frames(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
