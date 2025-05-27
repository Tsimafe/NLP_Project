import os
import re
from bs4 import BeautifulSoup


TEXTS_DATA_DIR = "../data/texts"
RAW_HTML_DIR = "../data/raw"


os.makedirs(TEXTS_DATA_DIR, exist_ok=True)



def extract_text_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    main_content = soup.find("main") or soup.find("article") or soup.find("body")
    if main_content:
        text = main_content.get_text(separator=" ", strip=True)
    else:
        text = soup.get_text(separator=" ", strip=True)

    return text



def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\sа-яА-ЯёЁ\-.,]', '', text)
    return text.strip()



def process_all_html():
    html_files = [f for f in os.listdir(RAW_HTML_DIR) if f.endswith(".html")]

    for html_file in html_files:
        html_path = os.path.join(RAW_HTML_DIR, html_file)
        try:
            text = extract_text_from_html(html_path)
            cleaned_text = clean_text(text)

            text_filename = os.path.splitext(html_file)[0] + ".txt"
            text_path = os.path.join(TEXTS_DATA_DIR, text_filename)

            with open(text_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Очищенный текст сохранён: {text_path}")
        except Exception as e:
            print(f"Ошибка при обработке {html_file}: {e}")



process_all_html()