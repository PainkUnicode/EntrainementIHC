# app/video_extraction.py
import cv2
import os
import random
import boto3
from moviepy.editor import VideoFileClip
from app import app

def afficher_duree(titre_recherche):
    films = os.path.join('app', 'duree.txt')
    with open(films, 'r') as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            # Séparer le titre et la durée en utilisant la virgule comme séparateur
            titre, duree_en_secondes = ligne.strip().split(',')
            if titre.lower() == titre_recherche.lower():
                return duree_en_secondes


def extract_frames(selected_video, video_path, output_folder, num_frames=4):
    # Ouvrir la vidéo

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    #Obtenir la durée de la vidéo
    duration = int(afficher_duree(selected_video))
    print(f'duration : {duration}')

    # Choisissez 4 instants de temps aléatoires
    frame_indices = random.sample(range(duration), num_frames)
    print(f'Nombre de frames : {frame_indices}')
    frame_paths = []
    clip = VideoFileClip(video_path)
    f = 0
    for index in frame_indices:
        f = f + 1
        frame_name = f"frame_{f}.jpg"
        clip.save_frame(os.path.join(output_folder, frame_name), t=index)
        print(f'frame no {f} a été enregistrée')

    clip.close()
    return frame_paths

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

    # Enregistrer le collage final
    cv2.imwrite(collage_path, collage_final)
    print(f"Collage créé avec succès et enregistré sous {output_folder}.")

    return collage_path
