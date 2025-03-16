from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    if request.method == 'POST':
        url = request.form['url']
        video_id = extract_video_id(url)
        if video_id:
            try:
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = "\n".join([f"{item['start']}: {item['text']}" for item in transcript_data])
            except Exception as e:
                transcript = f"Error: {str(e)}"
        else:
            transcript = "Invalid YouTube URL."

    return render_template('index.html', transcript=transcript)

def extract_video_id(url):
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    return match.group(1) if match else None

if __name__ == '__main__':
    app.run(debug=True)
