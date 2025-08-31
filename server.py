import os
from flask import Flask, request, jsonify
from gtts import gTTS
import io
import base64

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")
    lang = data.get("lang", "en")
    tld = data.get("tld", "com.au")
    slow = data.get("slow", False)

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # generate TTS in memory
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # convert to base64
    audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
    return jsonify({"audio_base64": audio_base64})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT if available
    app.run(host="0.0.0.0", port=port)