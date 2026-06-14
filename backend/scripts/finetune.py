import os
import argparse
import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from peft import get_peft_model, LoraConfig, TaskType

# Recommended base model from AI4Bharat
MODEL_NAME = "ai4bharat/indictrans2-en-indic-1B"

def prepare_model_and_tokenizer():
    print(f"Loading tokenizer and model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME, 
        trust_remote_code=True,
        torch_dtype=torch.float16, # Use fp16 for faster training
        device_map="auto" # Distribute across GPUs if available
    )
    
    # Apply LoRA (Low-Rank Adaptation)
    # This freezes the base model and only trains a small adapter,
    # reducing memory usage by 90% and training time significantly.
    peft_config = LoraConfig(
        task_type=TaskType.SEQ_2_SEQ_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"]
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    return model, tokenizer

def preprocess_function(examples, tokenizer, target_lang_code):
    """
    Tokenizes the english source and target dialect.
    """
    inputs = [ex["en"] for ex in examples["translation"]]
    targets = [ex[target_lang_code] for ex in examples["translation"]]
    
    # IndicTrans2 specific prefixing
    inputs = [f"{target_lang_code}: " + text for text in inputs]

    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

    # Tokenize targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def train(dataset_path, output_dir, target_lang_code):
    print(f"Loading formatted dataset from {dataset_path}")
    dataset = load_from_disk(dataset_path)
    
    model, tokenizer = prepare_model_and_tokenizer()
    
    print("Tokenizing dataset...")
    tokenized_datasets = dataset.map(
        lambda x: preprocess_function(x, tokenizer, target_lang_code),
        batched=True,
        remove_columns=dataset["train"].column_names
    )
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-4,
        per_device_train_batch_size=8, # Adjust based on GPU VRAM
        per_device_eval_batch_size=8,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=5,
        predict_with_generate=True,
        fp16=True, # Critical for speed on modern GPUs
        push_to_hub=False,
    )
    
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    
    print("Starting LoRA Fine-Tuning...")
    trainer.train()
    
    print(f"Saving fine-tuned adapter to {output_dir}/final_model")
    trainer.model.save_pretrained(f"{output_dir}/final_adapter")
    tokenizer.save_pretrained(f"{output_dir}/final_adapter")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to HF DatasetDict (e.g. ../datasets/hf_format/bnd)")
    parser.add_argument("--output_dir", type=str, required=True, help="Where to save model weights")
    parser.add_argument("--lang_code", type=str, required=True, help="Target language code (e.g. bnd or bho)")
    args = parser.parse_args()
    
    train(args.dataset_path, args.output_dir, args.lang_code)
