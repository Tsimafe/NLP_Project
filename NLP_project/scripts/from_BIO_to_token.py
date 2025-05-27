import json
import torch
from transformers import BertTokenizerFast

# Загружаем токенизатор BERT
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

# Маппинг меток BIO в числовые значения
label2id = {
    "O": 0,  # Outside
    "B-PRODUCT": 1,  # Beginning of Product Name
    "I-PRODUCT": 2,  # Inside Product Name
}

# Чтение данных из JSON
with open("ner_data_for_huggingface.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Списки для токенов и меток
input_ids = []
attention_masks = []
labels = []

# Обрабатываем данные
for item in data:
    tokens = item["tokens"]
    item_labels = item["labels"]

    # Преобразуем токены в их ID
    encoding = tokenizer(tokens, is_split_into_words=True, padding="max_length", truncation=True, max_length=512,
                         return_tensors="pt")

    input_ids.append(encoding["input_ids"].squeeze(0))
    attention_masks.append(encoding["attention_mask"].squeeze(0))

    # Преобразуем метки в числовые значения
    item_labels_numeric = [label2id[label] for label in item_labels]

    # Паддинг меток, если необходимо (до max_length)
    while len(item_labels_numeric) < 512:
        item_labels_numeric.append(label2id["O"])  # Добавляем паддинг для "O" (Outside)

    labels.append(torch.tensor(item_labels_numeric[:512]))  # Ограничиваем длину 512 токенами

# Преобразуем в тензоры PyTorch
input_ids_tensor = torch.stack(input_ids)
attention_masks_tensor = torch.stack(attention_masks)
labels_tensor = torch.stack(labels)

# ✅ Сохраняем в бинарном формате (PyTorch)
torch.save({
    "input_ids": input_ids_tensor,
    "attention_masks": attention_masks_tensor,
    "labels": labels_tensor
}, "tokenized_ner_data.pt")

# ✅ Сохраняем в читаемом JSON-формате
data_to_save = {
    "input_ids": input_ids_tensor.tolist(),
    "attention_masks": attention_masks_tensor.tolist(),
    "labels": labels_tensor.tolist()
}

with open("tokenized_ner_data.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=2)

print("Данные успешно сохранены в 'tokenized_ner_data.pt' и 'tokenized_ner_data.json'")
