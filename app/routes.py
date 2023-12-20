# app/routes.py
from flask import render_template, request, send_from_directory
from app import app, video_extraction
import os
import random
import shutil
import boto3
import numpy as np
import time
from moviepy.editor import VideoFileClip

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def video_generator(video_folder):
    video_files_brut = video_folder.list_objects_v2(Bucket = 'films2023' )
    video_files = []
    for obj in video_files_brut.get('Contents', []):
        video_files.append(obj['Key'])
    random.shuffle(video_files)
    while video_files:
        yield video_files.pop()

def read_film_text(selected_video):
    text_folder = 'app/textes'  # Remplacez par le chemin de votre dossier de textes
    text_file_path = os.path.join(text_folder, os.path.splitext(selected_video)[0] + '.txt')

    # Lire le texte du fichier correspondant au film
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        film_text = text_file.read()

    return film_text

@app.route('/process_video', methods=['POST', 'GET'])
def process_video():
    time_start = time.time()
    print(f'Time start : {time_start}')
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
    f = 0
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
        result = video_extraction.extract_frames(selected_video, video_path, output_folder, f)
        print(f'Frames Extraites : {result}')
        frame_list = os.listdir(app.config['OUTPUT_FOLDER'])


        # Préparez les chemins complets des images
        full_frame_paths = [os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(image)) for image in frame_list]

        # Appel du script pour coller les images en une seule
        result_image_path = video_extraction.create_collage()
        print(f'Selected Video : {selected_video}')
        # Lire le texte du fichier correspondant au film
        film_text = read_film_text(selected_video)

        result_data.append({'image_path': result_image_path, 'film_text': film_text})
        time_stop = time.time()
        print(f'time stop : {time_stop}')
        duree = time_stop - time_start
        print(f'Durée : {duree}')
    return render_template('result.html', result_data=result_data, os=os)

@app.route('/output_frames/<path:filename>')
def serve_output_frames(filename):
    return send_from_directory(app.config['COLLAGE_FOLDER'], filename)
