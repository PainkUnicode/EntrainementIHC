import boto3
from moviepy.editor import VideoFileClip
from botocore.exceptions import NoCredentialsError
import random
import numpy as np

# Configurer les informations d'identification AWS
aws_access_key_id = 'AKIA6PN5NTY2E67H2T56'
aws_secret_access_key = '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'
region_name = 'eu-central-1'
bucket_name = 'films2023'
video_key = 'Metropolis.mp4'


# Configurer la connexion à AWS S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Obtenir l'URL signée de l'objet S3 (pour accéder au fichier sans téléchargement)
url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': video_key}, ExpiresIn=3600)
print(f'L"URL est{url}')

# Récupérer les métadonnées de la vidéo (y compris la durée)
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
# Obtenir la durée de la vidéo
video_duration = get_video_duration(url)

if video_duration is not None:
    print(f"Durée de la vidéo : {video_duration} secondes")
else:
    print("Impossible de récupérer la durée de la vidéo.")

timecode = random_time_code(video_duration)
clip = VideoFileClip(url)
clip.save_frame(t=timecode, filename="frame.jpg")
print(f'timecode is : {timecode}')