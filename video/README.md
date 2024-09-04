# Video Processing and Subtitle Search Platform

This project is a Django-based web application that allows users to upload videos, process them to extract subtitles using `ccextractor`, store the videos on AWS S3, and store the extracted subtitles in AWS DynamoDB. Users can search for specific phrases within the subtitles and receive the corresponding video segments.

## Features

- **Video Upload:** Users can upload video files via a simple web interface.
- **Subtitle Extraction:** Subtitles are automatically extracted from the uploaded videos using the `ccextractor` binary.
- **AWS S3 Integration:** Processed videos are stored securely in AWS S3.
- **AWS DynamoDB Integration:** Extracted subtitles and their timestamps are stored in DynamoDB, allowing efficient keyword searches.
- **Search Functionality:** Users can search for specific phrases within the subtitles, and the application returns the relevant time segments.

## Technologies Used

- **Django:** Backend web framework for building the application.
- **Celery:** Distributed task queue for handling background video processing tasks.
- **Redis:** Message broker for Celery tasks.
- **ccextractor:** Tool for extracting subtitles from video files.
- **AWS S3:** Cloud storage for storing processed videos.
- **AWS DynamoDB:** NoSQL database for storing and searching subtitle data.

## Getting Started

### Prerequisites

- Python 3.x
- Redis (for Celery)
- AWS account with S3 and DynamoDB setup
- `ccextractor` binary installed on your system

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Pratibhakakad/video_upload_search
   cd video

**Create a virtual environment and activate it:**
python3 -m venv venv
source venv/bin/activate

**Install the required Python packages:**
pip install -r requirements.txt

**Configure environment variables: Create a .env file in the project root with the following content:**
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
AWS_S3_REGION_NAME=your_s3_region_name
AWS_DYNAMODB_TABLE_NAME=Subtitles

**Run database migrations:**
python manage.py migrate

**Start Redis:**
redis-server

**Start Celery workers:**
celery -A video_app worker --loglevel=info

**Start the Django development server:**
python manage.py runserver

**Uploading a Video: Navigate to http://127.0.0.1:8000/upload/ and upload a video file. The video will be processed in the background to extract subtitles.**
**Searching Subtitles: Navigate to http://127.0.0.1:8000/search/ and enter a keyword to search for specific phrases in the subtitles. The search results will include the time segments where the keyword appears in the video.**
**AWS Setup**
S3 Bucket: Create an S3 bucket in your AWS account for storing videos.
DynamoDB Table: Create a DynamoDB table with the name specified in your .env file (default: Subtitles). The table should have the following structure:
Partition key: video_id (string)
Sort key: timestamp (string)
Additional attributes: phrase (string)
