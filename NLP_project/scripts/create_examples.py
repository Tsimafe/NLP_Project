import os

TEXTS_DATA_DIR = "C:\\Users\\Uladzislau\\Desktop\\NLP_project\\data\\texts"
LABELS_DIR = "C:\\Users\\Uladzislau\\Desktop\\NLP_project\\data\\examples_for_trainer_web"

os.makedirs(LABELS_DIR, exist_ok=True)

# Функция для получения текста из файла
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Функция для сохранения размеченных данных
def save_labeled_data(file_name, entities, output_path):
    mode = 'a' if os.path.exists(output_path) else 'w'
    with open(output_path, mode, encoding='utf-8') as file:
        for entity in entities:
            file.write(f"{entity}\n")
    print(f"Размеченные данные сохранены в {output_path} (режим: {mode})")

# Обработка всех текстовых файлов
def process_texts_and_save_labels():
    text_files = [f for f in os.listdir(TEXTS_DATA_DIR) if f.endswith(".txt")]

    for text_file in text_files:
        text_path = os.path.join(TEXTS_DATA_DIR, text_file)
        text_content = read_text_from_file(text_path)

        print(f"Открыл файл {text_file}. Пожалуйста, вручную добавь товары.")
        print(f"Текст файла:\n{text_content}\n")

        entities = []

        while True:
            entity = input("Введите товар (или нажмите Enter для пропуска): ").strip()
            if entity == "":
                print(f"Пропускаем товар для файла {text_file}.")
                break
            else:
                entities.append(entity)

        labeled_file_path = os.path.join(LABELS_DIR, f"{text_file}_labels.txt")
        save_labeled_data(text_file, entities, labeled_file_path)


process_texts_and_save_labels()
