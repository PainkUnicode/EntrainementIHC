# app/video_extraction.py
import cv2
import os
import random

def extract_frames(video_path, output_folder, num_frames=4):
    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    # Obtenir la fréquence d'images de la vidéo
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculer le nombre total de frames dans la vidéo
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Choisissez 4 instants de temps aléatoires
    frame_indices = random.sample(range(total_frames), num_frames)

    frame_paths = []

    for index in frame_indices:
        # Sauter à l'instant de temps choisi
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)

        # Lire la frame
        ret, frame = cap.read()

        if not ret:
            break

        # Enregistrez la frame
        frame_name = f"frame_{index}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)

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