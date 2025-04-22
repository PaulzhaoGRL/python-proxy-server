#!/bin/bash

# 安裝 Python 套件
pip install -r requirements.txt

# 安裝 Playwright
pip install playwright

# 安裝 Chromium 瀏覽器
python -m playwright install chromium
