from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS module
import requests
from collections import Counter
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to fetch page content
def get_page_content(url):
    response = requests.get(url)
    return response.text

# Function to calculate word frequencies
def get_most_frequent_words(text, n=10):
    words = re.findall(r'\b\w+\b', text.lower())
    counter = Counter(words)
    return counter.most_common(n)

@app.route('/get-word-frequencies', methods=['POST'])
def get_word_frequencies():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        page_content = get_page_content(url)
        soup = BeautifulSoup(page_content, 'html.parser')
        text = soup.get_text()
        word_frequencies = get_most_frequent_words(text)
        return jsonify(word_frequencies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
