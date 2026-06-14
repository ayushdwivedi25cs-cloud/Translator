import json
import os
import argparse
from datasets import Dataset, DatasetDict

def load_json_dataset(file_path, target_lang):
    """
    Loads our custom JSON structure and converts it into a format 
    suitable for HuggingFace datasets (translation format).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    formatted_data = {"translation": []}
    
    # Map the short code to the JSON key
    key_map = {"bnd": "bundelkhandi", "bho": "bhojpuri"}
    json_key = key_map.get(target_lang, target_lang)
    
    for item in data:
        # Build the HuggingFace translation pair dict
        pair = {
            "en": item["english"],
            target_lang: item.get(json_key)
        }
        
        # Ensure neither side is empty
        if pair["en"] and pair[target_lang]:
            formatted_data["translation"].append(pair)
            
    return formatted_data

def prepare_huggingface_dataset(json_dir, output_dir):
    """
    Reads the raw json datasets, splits them into train/val/test, 
    and saves them as huggingface DatasetDicts on disk.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    languages = [("bundelkhandi.json", "bnd"), ("bhojpuri.json", "bho")]
    
    for filename, lang_code in languages:
        file_path = os.path.join(json_dir, filename)
        if not os.path.exists(file_path):
            print(f"Skipping {filename} - file not found.")
            continue
            
        print(f"Processing {filename}...")
        formatted_data = load_json_dataset(file_path, lang_code)
        
        # Create HuggingFace Dataset object
        dataset = Dataset.from_dict(formatted_data)
        
        # Split: 90% train, 5% val, 5% test (Only if enough data exists)
        if len(dataset) < 10:
            print(f"Dataset too small ({len(dataset)} rows) for full splitting. Putting all in train.")
            hf_dataset = DatasetDict({
                'train': dataset,
                'validation': dataset, # Duplicate just to satisfy trainer requirements
                'test': dataset
            })
        else:
            train_testval = dataset.train_test_split(test_size=0.1, seed=42)
            test_val = train_testval['test'].train_test_split(test_size=0.5, seed=42)
            
            hf_dataset = DatasetDict({
                'train': train_testval['train'],
                'validation': test_val['train'],
                'test': test_val['test']
            })
        
        # Save to disk
        save_path = os.path.join(output_dir, lang_code)
        hf_dataset.save_to_disk(save_path)
        print(f"Saved {lang_code} dataset to {save_path}")
        print(f"Train: {len(hf_dataset['train'])} | Val: {len(hf_dataset['validation'])} | Test: {len(hf_dataset['test'])}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare custom datasets for HuggingFace training")
    parser.add_argument("--json_dir", type=str, default="../datasets", help="Directory containing raw JSON files")
    parser.add_argument("--output_dir", type=str, default="../datasets/hf_format", help="Output directory for HF datasets")
    args = parser.parse_args()
    
    prepare_huggingface_dataset(args.json_dir, args.output_dir)
