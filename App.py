from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudscraper
import socket

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

def find_free_port(start_port=5000, end_port=6000):
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return None

if __name__ == '__main__':
    port = find_free_port()
    if port:
        print(f'✅ API شغال على المنفذ: {port}')
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        print('❌ ماكو منافذ متاحة من 5000 إلى 6000')
