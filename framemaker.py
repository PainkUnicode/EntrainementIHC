import cv2
import os
import tkinter as tk
from tkinter import filedialog

def extract_frames(video_path, output_folder, frame_interval):
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Charger la vidéo
    cap = cv2.VideoCapture(video_path)

    # Obtenir la fréquence d'images de la vidéo
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Lire la vidéo et extraire les frames avec l'intervalle spécifié
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Sauvegarder la frame dans le dossier de sortie
        frame_filename = f"{output_folder}/frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)

        # Passer à la frame suivante en utilisant l'intervalle spécifié
        frame_count += frame_interval

        # Passer à la frame suivante dans la vidéo
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

    # Libérer la vidéo
    cap.release()

def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    video_entry.delete(0, tk.END)
    video_entry.insert(0, file_path)

def process_video():
    video_path = video_entry.get()
    frame_interval = int(frame_interval_entry.get())

    if not video_path:
        tk.messagebox.showerror("Erreur", "Veuillez sélectionner un fichier vidéo.")
        return

    if frame_interval <= 0:
        tk.messagebox.showerror("Erreur", "L'intervalle de frames doit être supérieur à zéro.")
        return

    # Extraire le nom du fichier sans extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Créer un dossier pour les frames
    output_folder = f"{video_name}"

    # Extraire les frames de la vidéo avec l'intervalle spécifié
    extract_frames(video_path, output_folder, frame_interval)

    tk.messagebox.showinfo("Terminé", f"Frames extraites avec succès dans le dossier : {output_folder}")

# Créer la fenêtre principale
window = tk.Tk()
window.title("Extracteur de Frames")

# Ajouter des composants à la fenêtre
tk.Label(window, text="Sélectionnez le fichier vidéo :").pack(pady=10)
video_entry = tk.Entry(window, width=50)
video_entry.pack(pady=10)
tk.Button(window, text="Parcourir", command=select_video_file).pack(pady=10)

tk.Label(window, text="Intervalle de frames à enregistrer :").pack(pady=10)
frame_interval_entry = tk.Entry(window)
frame_interval_entry.pack(pady=10)

tk.Button(window, text="Extraire Frames", command=process_video).pack(pady=20)

# Lancer la boucle principale de l'interface graphique
window.mainloop()
