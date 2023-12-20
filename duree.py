import boto3
from moviepy.editor import VideoFileClip

aws_access_key_id = 'AKIA6PN5NTY2E67H2T56'
aws_secret_access_key = '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'
region_name = 'eu-central-1'
bucket_name = 'films2023'

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

video_files_brut = s3.list_objects_v2(Bucket = 'films2023' )

video_files = []

for obj in video_files_brut.get('Contents', []):
    video_files.append(obj['Key'])

for video in video_files :
    video_path = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': video}, ExpiresIn=3600)
    clip = VideoFileClip(video_path)
    duration = clip.duration
    print(f'La durée de {video} est de {duration} secondes')
    clip.close()