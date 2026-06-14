import urllib.request
import os

font_url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf"
font_path = "NotoSansDevanagari-Regular.ttf"

if not os.path.exists(font_path):
    print("Downloading Noto Sans Devanagari...")
    try:
        urllib.request.urlretrieve(font_url, font_path)
        print("Downloaded successfully.")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Font already exists.")
