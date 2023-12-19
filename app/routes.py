# app/routes.py
from flask import render_template, request, send_from_directory
from app import app, video_extraction
import os
import random
import shutil
import boto3
import numpy as np
from moviepy.editor import VideoFileClip

@app.route('/')
def index():
    return render_template('index.html')

def get_video_duration(video_url):
    try:
        clip = VideoFileClip(video_url)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Erreur lors de la récupération des métadonnées de la vidéo : {e}")
        return None

def random_time_code(video_duration) : 
    timecode = round(np.random.uniform(0, video_duration),2)
    return timecode

def video_generator(video_folder):
    video_files_brut = video_folder.list_objects_v2(Bucket = 'films2023' )
    video_files = []
    for obj in video_files_brut.get('Contents', []):
        print(obj['Key'])
        video_files.append(obj['Key'])
    print(video_files)
    random.shuffle(video_files)
    while video_files:
        yield video_files.pop()

def read_film_text(selected_video):
    text_folder = 'app_s3/textes'  # Remplacez par le chemin de votre dossier de textes
    text_file_path = os.path.join(text_folder, os.path.splitext(selected_video)[0] + '.txt')

    # Lire le texte du fichier correspondant au film
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        film_text = text_file.read()

    return film_text

@app.route('/process_video', methods=['POST', 'GET'])
def process_video():
    
    aws_access_key_id = 'AKIA6PN5NTY2E67H2T56'
    aws_secret_access_key = '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'
    region_name = 'eu-central-1'
    bucket_name = 'films2023'
    output_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'output_frames')

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    # Effacez le contenu du dossier de sortie au début du processus
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    result_data = []

    if request.method == 'GET':
        # Si la méthode est GET, cela signifie que l'utilisateur a cliqué sur le bouton de rechargement
        return render_template('result.html', result_data=[])

    # Effectuer le processus 10 fois
    for _ in range(1):
        video_gen = video_generator(s3)
        selected_video = next(video_gen, None)

        if not selected_video:
            break  # Si la liste est vide, sortez de la boucle

        video_path = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': selected_video}, ExpiresIn=3600)

        # Appel du script d'extraction d'images
        frame_images = video_extraction.extract_frames(video_path, output_folder)

        # Préparez les chemins complets des images
        full_frame_paths = [os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(image)) for image in frame_images]

        # Appel du script pour coller les images en une seule
        result_image_path = video_extraction.create_collage(full_frame_paths, output_folder)

        # Lire le texte du fichier correspondant au film
        film_text = read_film_text(selected_video)

        result_data.append({'image_path': result_image_path, 'film_text': film_text})

    return render_template('result.html', result_data=result_data, os=os)

@app.route('/output_frames/<path:filename>')
def serve_output_frames(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
