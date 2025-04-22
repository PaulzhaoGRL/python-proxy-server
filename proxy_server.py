from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)
CORS(app)

@app.route('/fetch-html', methods=['GET'])
def fetch_html():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    html = asyncio.run(get_html(url))
    return jsonify({'html': html})

async def get_html(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            content = await page.content()
            await browser.close()
            return content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
