# app/video_extraction.py
import cv2
import os
import random

def extract_frames(video_path, output_folder):
    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    frame_paths = []

    # Lire les frames
    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Enregistrez la frame
        frame_name = f"frame_{frame_count}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)

        frame_count += 1

    # Fermer la vidéo
    cap.release()

    return frame_paths

def create_collage(frame_paths, output_folder):
    # Choisissez 4 images aléatoires parmi celles extraites
    selected_frames = random.sample(frame_paths, 4)

    # Chargez les images sélectionnées
    images = [cv2.imread(frame) for frame in selected_frames]

    # Créez une image en collant les 4 images ensemble
    collage = cv2.vconcat([cv2.hconcat(images[:2]), cv2.hconcat(images[2:])])

    # Enregistrez l'image de collage
    result_image_path = os.path.join(output_folder, 'collage.jpg')
    cv2.imwrite(result_image_path, collage)

    return result_image_path