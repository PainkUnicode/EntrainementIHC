# app/video_extraction.py
import cv2
import os
import random
import boto3
from moviepy.editor import VideoFileClip

def extract_frames(video_path, output_folder, num_frames=4):
    # Ouvrir la vidéo

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    #Obtenir la durée de la vidéo
    clip = VideoFileClip(video_path)
    duration = int(clip.duration)
    clip.close()
    # Choisissez 4 instants de temps aléatoires
    frame_indices = random.sample(range(duration), num_frames)
    print(f'Nombre de frames : {frame_indices}')
    frame_paths = []
    clip = VideoFileClip(video_path)

    for index in frame_indices:
        frame_name = f"frame_{index}.jpg"
        clip.save_frame(os.path.join(output_folder, frame_name), t=duration)

    clip.close()

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