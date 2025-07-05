from flask import Flask, request, jsonify
from bots.zoom.bot import list_meetings, download_transcript_and_recording

app = Flask(__name__)

@app.route('/meetings', methods=['GET'])
def get_meetings():
    meetings = list_meetings()
    return jsonify(meetings)

@app.route('/download/<meeting_id>', methods=['POST'])
def download_meeting(meeting_id):
    download_transcript_and_recording(meeting_id)
    return jsonify({"status": "Download triggered", "meeting_id": meeting_id})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
