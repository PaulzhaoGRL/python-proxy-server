from flask import Flask, request, jsonify
from flask_cors import CORS
from requests_html import HTMLSession
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/fetch-html')
def fetch_html():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        session = HTMLSession()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = session.get(url, headers=headers)

        # 🧠 修正：建立事件迴圈
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response.html.render(timeout=20)

        return jsonify({'html': response.html.html})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
