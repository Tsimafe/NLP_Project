import os
import requests

# Папка для хранения скачанных HTML
RAW_DATA_DIR = "../data/raw"

# Читаем список URL из файла
with open("../data/urls.txt", "r") as file:
    urls = file.readlines()

# Убираем возможные пустые строки
urls = [url.strip() for url in urls if url.strip()]


# Функция для скачивания и сохранения HTML
def download_html(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус ответа (200 — успешный)

        # Проверяем, что страница не пустая
        if not response.text.strip():
            print(f"Страница пустая: {url}")
            return

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Скачано: {url}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании {url}: {e}")
    except Exception as e:
        print(f"Ошибка: {e} при скачивании {url}")


# Создаём директорию, если она не существует
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Скачиваем HTML-страницы
for idx, url in enumerate(urls, 1):
    save_path = os.path.join(RAW_DATA_DIR, f"{idx:03}.html")
    download_html(url, save_path)
