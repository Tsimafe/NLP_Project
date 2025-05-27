import os
import json
import re
from transformers import BertTokenizerFast

TEXTS_DATA_DIR = "C:\\Users\\Uladzislau\\Desktop\\NLP_project\\data\\texts"
LABELS_DIR = "C:\\Users\\Uladzislau\\Desktop\\NLP_project\\data\\examples_for_trainer_web"

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")


def tag_product(text, product_name):

    # Получаем маппинг из токенов в исходный текст
    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = tokenizer.convert_ids_to_tokens(encoding["input_ids"])
    offsets = encoding["offset_mapping"]

    # Ищем все вхождения названия продукта в тексте
    matches = list(re.finditer(re.escape(product_name), text))
    if not matches:
        return tokens, ['O'] * len(tokens)

    labels = ['O'] * len(tokens)
    for match in matches:
        span_start, span_end = match.start(), match.end()

        inside = False
        for i, (token, (start, end)) in enumerate(zip(tokens, offsets)):
            if start >= span_start and end <= span_end:
                if not inside:
                    labels[i] = "B-PRODUCT"
                    inside = True
                else:
                    labels[i] = "I-PRODUCT"

    return tokens, labels


text_files = os.listdir(TEXTS_DATA_DIR)
labels_files = os.listdir(LABELS_DIR)

# Формирование и сохранение BIO-аннотированных данных
formatted_data = []
for text_file, label_file in zip(text_files, labels_files):
    with open(os.path.join(TEXTS_DATA_DIR, text_file), "r", encoding="utf-8") as f_text:
        text = f_text.read()

    with open(os.path.join(LABELS_DIR, label_file), "r", encoding="utf-8") as f_label:
        product_name = f_label.read().strip()

    # Обрабатываем каждый текст и соответствующее название
    tokens, labels = tag_product(text, product_name)

    formatted_data.append({
        "tokens": tokens,
        "labels": labels
    })

with open("ner_data_for_huggingface.json", "w", encoding="utf-8") as f:
    json.dump(formatted_data, f, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в файл 'ner_data_for_huggingface.json'.")
