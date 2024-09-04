from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Video
from .tasks import process_video
from .forms import VideoUploadForm
from django.conf import settings
import boto3

# Create your views here.


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            process_video.delay(video.id)
            return JsonResponse({'message': 'Video uploaded and processing started.'})
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})


def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_S3_REGION_NAME)
        table = dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)

        response = table.scan(
            FilterExpression='contains(phrase, :phrase)',
            ExpressionAttributeValues={':phrase': query}
        )

        results = response.get('Items', [])

    return render(request, 'search.html', {'results': results, 'query': query})

