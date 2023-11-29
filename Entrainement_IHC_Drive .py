import os
import cv2
import random
import shutil
import numpy as np

def extract_random_frames(video_path, output_folder, num_frames=4):
    # Ouvrir la vidéo en utilisant OpenCV
    cap = cv2.VideoCapture(video_path)

    # Obtenir la fréquence d'images (FPS) de la vidéo
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Obtenir le nombre total de frames dans la vidéo
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Sélectionner num_frames indices de frames aléatoires
    random_frame_indices = random.sample(range(total_frames), num_frames)

    # Lire les frames sélectionnées
    selected_frames = []
    for frame_index in random_frame_indices:
        # Définir la position actuelle de la vidéo sur le frame sélectionné
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Lire le frame actuel
        ret, frame = cap.read()

        if ret:
            # Ajouter le frame à la liste des frames sélectionnés
            selected_frames.append(frame)

    # Libérer la ressource vidéo
    cap.release()

    return selected_frames

def combine_frames_into_one_image(frames):
    # Concaténer les frames horizontalement (en une seule ligne)
    combined_image = np.hstack(frames)

    return combined_image

def clean_output_folder(output_folder):
    # Supprimer tous les fichiers dans le dossier de sortie
    for file_name in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression de {file_path}: {e}")

def get_unique_random_number():
    # Générer une liste d'entiers uniques de 0 à 10
    numbers = list(range(100))
    random.shuffle(numbers)
    return numbers.pop()

def main():
    # Spécifier le dossier contenant les fichiers vidéo
    video_folder = "/Users/yannvetter/Library/CloudStorage/OneDrive-UniversitédeLausanne/Ecole/Université/IHC - Intro à l'histoire du cinéma/Films IHC"

    # Liste des fichiers vidéo dans le dossier
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

    if not video_files:
        print("Aucun fichier vidéo trouvé dans le dossier.")
        return
    
    # Spécifier le dossier de sortie pour enregistrer les images
    output_folder = "/Users/yannvetter/Library/CloudStorage/OneDrive-UniversitédeLausanne/Ecole/Université/IHC - Intro à l'histoire du cinéma/Films IHC/Exos"

     # Assurer que le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Nettoyer le dossier de sortie avant chaque exécution
    clean_output_folder(output_folder)

    # Exécuter le processus 10 fois
    for _ in range(10):
        # Choisir aléatoirement un fichier vidéo parmi la liste
        selected_video = random.choice(video_files)

        # Construire le chemin complet du fichier vidéo sélectionné
        video_path = os.path.join(video_folder, selected_video)

        # Extraire les frames aléatoires du fichier vidéo sélectionné
        frames = extract_random_frames(video_path, output_folder)

        # Combiner les frames en une seule image
        combined_image = combine_frames_into_one_image(frames)

        # Obtenir un numéro aléatoire unique entre 0 et 10
        random_number = get_unique_random_number()

        # Construire le nom du fichier de sortie avec le nom de la vidéo d'origine
        output_filename = f"{random_number}_{os.path.splitext(selected_video)[0]}_combined_{_+1}.jpg"
        output_path = os.path.join(output_folder, output_filename)

        # Enregistrer l'image combinée dans le dossier de sortie
        cv2.imwrite(output_path, combined_image)
        print(f"Image combinée {_+1} enregistrée à {output_path}")

if __name__ == "__main__":
    main()