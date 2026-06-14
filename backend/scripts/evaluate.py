import argparse
import torch
from datasets import load_from_disk
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from peft import PeftModel
import evaluate # HuggingFace evaluate library

MODEL_NAME = "ai4bharat/indictrans2-en-indic-1B"

def load_models(adapter_path):
    print("Loading base tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    
    print("Loading base model...")
    base_model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME, 
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    print(f"Loading LoRA adapter from {adapter_path}...")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model.eval()
    
    return model, tokenizer

def run_evaluation(dataset_path, adapter_path, target_lang_code):
    model, tokenizer = load_models(adapter_path)
    
    print("Loading test dataset...")
    dataset = load_from_disk(dataset_path)
    test_data = dataset["test"]
    
    sacrebleu = evaluate.load("sacrebleu")
    chrf = evaluate.load("chrf")
    
    predictions = []
    references = []
    
    print(f"Evaluating on {len(test_data)} examples...")
    for idx, item in enumerate(test_data):
        en_text = item["translation"]["en"]
        target_text = item["translation"][target_lang_code]
        
        # Format input for IndicTrans2
        input_text = f"{target_lang_code}: " + en_text
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=128).to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=128)
            
        pred_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        predictions.append(pred_text)
        references.append([target_text])
        
        if idx < 5:
            print(f"\n--- Example {idx+1} ---")
            print(f"English: {en_text}")
            print(f"Target : {target_text}")
            print(f"Pred   : {pred_text}")
            
    # Compute sacreBLEU
    bleu_score = sacrebleu.compute(predictions=predictions, references=references)
    
    # Compute chrF++ (word_order=2) which is significantly better for highly inflected Indian languages
    chrf_score = chrf.compute(predictions=predictions, references=references, word_order=2)
    
    # Compute Exact Match Ratio
    exact_matches = sum(1 for p, r in zip(predictions, references) if p.strip() == r[0].strip())
    exact_match_ratio = (exact_matches / len(predictions)) * 100 if predictions else 0
    
    print("\n" + "="*40)
    print("FINAL EVALUATION METRICS")
    print("="*40)
    print(f"SacreBLEU Score : {bleu_score['score']:.2f} (Standard lexical match)")
    print(f"chrF++ Score    : {chrf_score['score']:.2f} (Preferred for Indic morphology)")
    print(f"Exact Match     : {exact_match_ratio:.2f}% ({exact_matches}/{len(predictions)})")
    
    print("\n[NOTE] For production benchmarking, consider integrating COMET or BERTScore for semantic similarity, as literal n-gram matches often penalize perfectly valid dialect synonyms.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, required=True)
    parser.add_argument("--adapter_path", type=str, required=True)
    parser.add_argument("--lang_code", type=str, required=True)
    args = parser.parse_args()
    
    run_evaluation(args.dataset_path, args.adapter_path, args.lang_code)
