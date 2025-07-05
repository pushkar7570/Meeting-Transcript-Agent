from flask import Flask, request

app = Flask(__name__)

# Simple in-memory transcript store for demo
transcript_data = []

@app.route('/api/v1/meet/transcript', methods=['POST'])
def receive_transcript():
    data = request.json
    text = data.get('text')
    timestamp = data.get('timestamp')
    if text:
        transcript_data.append({'text': text, 'timestamp': timestamp})
        print(f"[{timestamp}] {text}")
    return {"status": "success"}

if __name__ == '__main__':
    app.run(port=5001)
