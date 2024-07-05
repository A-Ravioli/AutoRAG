import dspy
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from datasets import load_dataset

def fine_tune_model(model_name: str, data_path: str):
    # Load the pre-trained model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Load and preprocess the data
    train_dataset = load_dataset(data_path, split="train")
    train_dataset = preprocess_data(train_dataset, tokenizer)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
    )

    # Create Trainer instance
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    # Start fine-tuning
    trainer.train()

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")

    return "./fine_tuned_model"

def load_dataset(data_path: str, split: str):
    # Load dataset from a CSV file
    dataset = load_dataset('csv', data_files=data_path, split=split)
    return dataset

def preprocess_data(dataset, tokenizer):
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    return tokenized_dataset