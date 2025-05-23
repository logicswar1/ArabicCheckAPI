from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

# Load and normalize words
with open('cleaned_arabic_words.txt', 'r', encoding='utf-8') as f:
    valid_words = set(word.strip() for word in f if len(word.strip()) > 2)

def normalize_arabic(text):
    text = re.sub(r'[إأآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    text = re.sub(r'\u0640', '', text)
    return text

@app.route('/validate', methods=['POST'])
def validate_word():
    data = request.get_json()
    word = data.get("word", "").strip()
    normalized = normalize_arabic(word)
    is_valid = normalized in valid_words
    return jsonify({"valid": is_valid})

# ✅ This should be at the very end
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
