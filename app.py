from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
import json

app = Flask(__name__)

API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    response_content = ""
    
    if request.method == 'POST':
        url = request.form['url']
        video_id = extract_video_id(url)
        
        if video_id:
            try:
                # Fetch the transcript
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = "\n".join([item['text'] for item in transcript_data])
                
                # Prepare the request to the Google API
                prompt = f"Extract and explain the content in the following transcript:\n{transcript}"
                response_content = generate_content(prompt)
                
            except Exception as e:
                transcript = f"Error: {str(e)}"
        else:
            transcript = "Invalid YouTube URL."

    return render_template('index.html', transcript=transcript, response_content=response_content)

def extract_video_id(url):
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    return match.group(1) if match else None

def generate_content(prompt):
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(API_URL, headers=headers, params={'key': API_KEY}, json=data)
    
    if response.status_code == 200:
        return response.json()  # Return the entire JSON response
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == '__main__':
    app.run(debug=True)
