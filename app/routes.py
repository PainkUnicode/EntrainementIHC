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
import cv2

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def select_random_folder(s3, bucket_name):
    # Liste tous les dossiers dans le bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

    # Extrait la liste des dossiers
    folders = [common_prefix['Prefix'] for common_prefix in response.get('CommonPrefixes', [])]

    # Sélectionne un dossier aléatoire
    selected_folder = random.choice(folders)

    return selected_folder

def download_random_images(s3, bucket_name, folder_path, download_path, num_images=4):

    # Liste tous les objets dans le dossier
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

    # Extrait la liste des objets (fichiers) dans le dossier
    objects = response.get('Contents', [])

    # Sélectionne num_images objets aléatoires
    selected_objects = random.sample(objects, min(num_images, len(objects)))

    # Télécharge les objets sélectionnés dans le dossier de téléchargement
    for obj in selected_objects:
        key = obj['Key']
        file_name = os.path.join(download_path, os.path.basename(key))
        s3.download_file(bucket_name, key, file_name)
        print(f"Image téléchargée : {file_name}")

def create_collage():
    output_folder = app.config['COLLAGE_FOLDER']
    frame_folder = app.config['OUTPUT_FOLDER']
    os.makedirs(output_folder, exist_ok=True)
    print(output_folder)
    if not os.path.exists(output_folder):
        print(f"Le dossier {output_folder} n'existe pas.")
        return
    
    # Lister les fichiers dans le dossier
    files = os.listdir(frame_folder)
    print(files)
    # Vérifier s'il y a au moins 4 fichiers dans le dossier
    if len(files) < 4:
        print(f"Le dossier doit contenir au moins 4 images.")
        return

    # Charger les 4 premières images
    images = [cv2.imread(os.path.join(frame_folder, files[i])) for i in range(4)]

    # Créer un collage horizontal des images
    collage_horizontal = cv2.hconcat(images[:2])
    collage_horizontal_bottom = cv2.hconcat(images[2:])
    
    # Créer un collage vertical des deux collages horizontaux
    collage_final = cv2.vconcat([collage_horizontal, collage_horizontal_bottom])
    collage_path = os.path.join(output_folder, "collage.jpg")
    print(collage_path)
    # Enregistrer le collage final
    cv2.imwrite(collage_path, collage_final)
    print(f"Collage créé avec succès et enregistré sous {output_folder}.")

    return collage_path

def read_film_text(selected_folder):
    text_folder = 'app/textes'  # Remplacez par le chemin de votre dossier de textes
    selected_folder = selected_folder.rstrip(os.path.sep)
    base_name = os.path.splitext(selected_folder)[0]
    text_file_path = os.path.join(text_folder, base_name + '.txt')

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
    bucket_name = 'frames2023'
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

       random_folder = select_random_folder(s3, bucket_name)
       result = download_random_images(s3, bucket_name, random_folder, output_folder)
       collage_path = create_collage()
       film_text = read_film_text(random_folder)
       result_data.append({'image_path': collage_path, 'film_text': film_text})

    return render_template('result.html', result_data=result_data, os=os)

@app.route('/output_frames/<path:filename>')
def serve_output_frames(filename):
    return send_from_directory(app.config['COLLAGE_FOLDER'], filename)
