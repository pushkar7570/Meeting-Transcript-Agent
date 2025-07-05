import os
import time
import jwt
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ZOOM_API_KEY")
API_SECRET = os.getenv("ZOOM_API_SECRET")
USER_ID = os.getenv("ZOOM_USER_ID")  # your Zoom email or user ID

def generate_jwt():
    payload = {
        'iss': API_KEY,
        'exp': time.time() + 3600
    }
    token = jwt.encode(payload, API_SECRET, algorithm='HS256')
    return token if isinstance(token, str) else token.decode("utf-8")

def get_headers():
    return {
        "authorization": f"Bearer {generate_jwt()}",
        "content-type": "application/json"
    }

def list_meetings():
    url = f"https://api.zoom.us/v2/users/{USER_ID}/meetings"
    response = requests.get(url, headers=get_headers())
    return response.json()

def list_recordings(meeting_id):
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
    response = requests.get(url, headers=get_headers())
    return response.json()

def download_file(download_url, file_path):
    headers = {"authorization": f"Bearer {generate_jwt()}"}
    with requests.get(download_url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {file_path}")

def download_transcript_and_recording(meeting_id, output_dir="backend/data"):
    rec_data = list_recordings(meeting_id)
    if "recording_files" not in rec_data:
        print("No recordings found!")
        return

    os.makedirs(output_dir, exist_ok=True)
    for file in rec_data["recording_files"]:
        file_type = file.get("file_type")
        download_url = file.get("download_url")
        if not download_url:
            continue

        filename = f"{meeting_id}_{file_type}.{file_type.lower()}"
        file_path = os.path.join(output_dir, filename)
        download_file(download_url, file_path)
    print("All files downloaded.")

if __name__ == "__main__":
    meetings = list_meetings()
    print("Upcoming meetings:", meetings)
    # Uncomment to download for a specific meeting
    # download_transcript_and_recording("your_meeting_id")
