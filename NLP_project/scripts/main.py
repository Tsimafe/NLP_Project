from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from transformers import DistilBertForTokenClassification, DistilBertTokenizerFast
import torch
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🔥 ЗАПУСК main.py")

# Модель
model_path = "C:/Users/Uladzislau/Desktop/NLP_project/scripts/my_bert_ner"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path, local_files_only=True)
model = DistilBertForTokenClassification.from_pretrained(model_path)
model.eval()

class URLRequest(BaseModel):
    url: str

def extract_product_names(text: str):
    max_length = 512
    stride = 50
    product_names = []

    # Разделим текст на чанки по max_length символов
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i + max_length]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
        i += max_length - stride

    for chunk in chunks:
        tokens = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True, max_length=max_length)
        with torch.no_grad():
            output = model(**tokens)
        logits = output.logits
        predictions = torch.argmax(logits, dim=2)
        predicted_ids = predictions[0].numpy()
        token_ids = tokens["input_ids"][0]
        tokens_text = tokenizer.convert_ids_to_tokens(token_ids)
        labels = model.config.id2label

        current_product = ""
        for token, label_id in zip(tokens_text, predicted_ids):
            label = labels[label_id]
            if label.startswith("B-"):
                if current_product:
                    product_names.append(current_product.strip())
                current_product = token.replace("##", "")
            elif label.startswith("I-") and current_product:
                current_product += " " + token.replace("##", "")
            else:
                if current_product:
                    product_names.append(current_product.strip())
                    current_product = ""

        if current_product:
            product_names.append(current_product.strip())

    return list(set(product_names))


@app.post("/extract")
def extract_products(request: URLRequest):
    try:
        response = requests.get(request.url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=400, detail="Ошибка при запросе страницы. Проверьте правильность URL.")

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()

    products = extract_product_names(page_text)

    print("👉 Извлеченные товары:", products)  # Вывод в любом случае

    if not products:
        return {"products": [], "message": "❌ Товары не найдены."}

    return {
        "products": products,
        "message": f"✅ Найдено {len(products)} товара(ов)."
    }
