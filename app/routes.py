# app/routes.py
from flask import render_template, request, send_from_directory
from app import app, video_extraction
import os
import random
import shutil

@app.route('/')
def index():
    return render_template('index.html')

def video_generator(video_folder):
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    random.shuffle(video_files)
    while video_files:
        yield video_files.pop()

@app.route('/process_video', methods=['POST'])
@app.route('/process_video', methods=['POST', 'GET'])
def process_video():
    if request.method == 'GET':
        # Si la méthode est GET, cela signifie que l'utilisateur a cliqué sur le bouton de rechargement
        return render_template('result.html', result_images=[])

    video_folder = 'app/films'  # Remplacez par le chemin de votre dossier vidéo
    output_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'output_frames')

    os.makedirs(output_folder, exist_ok=True)

    # Effacez le contenu du dossier de sortie au début du processus
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)
    
    result_images = []

    # Effectuer le processus 10 fois
    for _ in range(1):
        video_gen = video_generator(video_folder)
        selected_video = next(video_gen, None)

        if not selected_video:
            break  # Si la liste est vide, sortez de la boucle

        video_path = os.path.join(video_folder, selected_video)

        # Appel du script d'extraction d'images
        frame_images = video_extraction.extract_frames(video_path, output_folder)

        # Préparez les chemins complets des images
        full_frame_paths = [os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(image)) for image in frame_images]

        # Appel du script pour coller les images en une seule
        result_image_path = video_extraction.create_collage(full_frame_paths, output_folder)
        result_images.append(result_image_path)

    return render_template('result.html', result_images=result_images, os=os)

@app.route('/output_frames/<path:filename>')
def serve_output_frames(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
