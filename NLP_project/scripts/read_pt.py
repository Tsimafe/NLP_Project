import torch

data = torch.load("tokenized_ner_data.pt")

print("Ключи:", list(data.keys()))
print("Пример input_ids:", data["input_ids"][1][:10])  # первые 10 токенов первого примера
print("Пример attention_mask:", data["attention_masks"][0][:10])
print("Пример labels:", data["labels"][0][:10])
print("Количество примеров:", len(data["input_ids"]))
