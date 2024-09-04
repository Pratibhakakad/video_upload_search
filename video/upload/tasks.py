import subprocess
import boto3
import os
from celery import shared_task
from .models import Video
from django.conf import settings

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    local_path = video.file.path

    # Extract subtitles using ccextractor
    subtitle_file = f'{local_path}.srt'
    subprocess.run(['ccextractor', local_path, '-o', subtitle_file])

    # Upload video to S3
    s3 = boto3.client('s3')
    s3.upload_file(local_path, settings.AWS_STORAGE_BUCKET_NAME, video.file.name)

    # Parse subtitles and store in DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_S3_REGION_NAME)
    table = dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)

    with open(subtitle_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if '-->' in line:
                timestamp = line.strip()
                phrase = lines[i + 1].strip()
                table.put_item(
                    Item={
                        'video_id': video.id,
                        'timestamp': timestamp,
                        'phrase': phrase
                    }
                )

    # Mark the video as processed
    video.processed = True
    video.save()

    # Clean up local files
    os.remove(local_path)
    os.remove(subtitle_file)
