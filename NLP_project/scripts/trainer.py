import torch
from transformers import DistilBertForTokenClassification, DistilBertTokenizerFast, Trainer, TrainingArguments
from datasets import Dataset
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

# Загружаем токенизатор и модель distilbert-base-uncased
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
model = DistilBertForTokenClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=3,
    id2label={0: "O", 1: "B-PRODUCT", 2: "I-PRODUCT"},
    label2id={"O": 0, "B-PRODUCT": 1, "I-PRODUCT": 2}
)

# Загружаем токенизированные данные
train_data = torch.load("tokenized_ner_data.pth")

# Создание Dataset для PyTorch
train_dataset = Dataset.from_dict({
    "input_ids": train_data["input_ids"],
    "attention_mask": train_data["attention_masks"],
    "labels": train_data["labels"]
})

# Функция для вычисления метрик
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    # Фильтруем метки и предсказания, убираем паддинг (-100)
    true_labels = [[label for label in label_list if label != -100] for label_list in labels]
    true_predictions = [
        [prediction for prediction, label in zip(prediction_list, label_list) if label != -100]
        for prediction_list, label_list in zip(predictions, labels)
    ]

    # Получаем точность
    accuracy = np.sum(np.array(true_predictions) == np.array(true_labels)) / float(np.sum([len(x) for x in true_labels]))

    # Получаем precision, recall, f1
    flat_true_labels = [label for sublist in true_labels for label in sublist]
    flat_true_predictions = [prediction for sublist in true_predictions for prediction in sublist]

    # Рассчитываем precision, recall и f1
    precision, recall, f1, _ = precision_recall_fscore_support(flat_true_labels, flat_true_predictions, average='weighted')

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

# Параметры тренировки
training_args = TrainingArguments(
    output_dir="./results",  # Output directory
    num_train_epochs=7,  # Number of training epochs
    per_device_train_batch_size=8,  # Batch size for training
    per_device_eval_batch_size=16,  # Batch size for evaluation
    warmup_steps=500,  # Number of warmup steps for learning rate scheduler
    weight_decay=0.01,  # Strength of weight decay
    logging_dir="./logs",  # Directory for storing logs
    logging_steps=10,
    use_cpu=True,  # Отключаем использование CUDA
)


# Создание Trainer
trainer = Trainer(
    model=model,  # The model to be trained
    args=training_args,  # Training arguments
    train_dataset=train_dataset,  # Training dataset
    compute_metrics=compute_metrics,  # Metrics for evaluation
    tokenizer=tokenizer,  # Tokenizer
)

for epoch in range(training_args.num_train_epochs):
    print(f"Training epoch {epoch+1}/{training_args.num_train_epochs}")
    trainer.train()  # Обучение на каждой эпохе
    print(f"Evaluating epoch {epoch+1}/{training_args.num_train_epochs}")
    trainer.evaluate()  # Оценка после каждой эпохи

trainer.train()

trainer.save_model("./my_bert_ner")
tokenizer.save_pretrained("./my_bert_ner")