from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.async_api import async_playwright
from playwright_stealth import stealth_sync  # ← 新增這行

import asyncio

app = Flask(__name__)
CORS(app)

@app.route("/fetch-html")
def fetch_html():
    url = request.args.get("url")

    async def run():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()

            page = await context.new_page()

            # 🕵️ 啟用 stealth 模式
            stealth_sync(page)

            await page.goto(url, timeout=60000)
            content = await page.content()
            await browser.close()
            return content

    try:
        html = asyncio.run(run())
        return jsonify({"html": html})
    except Exception as e:
        return jsonify({"html": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
