from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudscraper

app = Flask(__name__)
CORS(app)

scraper = cloudscraper.create_scraper()

@app.route('/')
def home():
    return jsonify({'status': 'online', 'api': 'TikTok API', 'developer': 'ابن العراق'})

@app.route('/info-tiktok.json')
def get_info():
    user = request.args.get('user')
    if not user:
        return jsonify({'error': 'Missing username'}), 400
    
    url = f'https://www.tiktok.com/node/share/user/@{user}'
    response = scraper.get(url)
    
    if response.status_code == 200:
        return jsonify(response.json())
    
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
