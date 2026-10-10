"""
🎓 SAATHI AI - Student QLoRA Fine-Tuning Script
-------------------------------------------------------------------------
This script fine-tunes an open-source Large Language Model (e.g. Qwen-2.5-1.5B or TinyLlama)
using QLoRA (4-bit quantized Low-Rank Adaptation) on your local NVIDIA RTX 4050 (6GB VRAM)
or on a free Google Colab GPU.

Every single machine learning parameter is commented below for learning!
-------------------------------------------------------------------------
"""
import os
import sys
import argparse
import json

def train_saathi_model(
    base_model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
    data_path: str = "data/training_data/train.jsonl",
    output_adapter_dir: str = "training/saathi_lora_adapter",
    epochs: int = 3,
    batch_size: int = 2,
    gradient_accumulation_steps: int = 4,
    learning_rate: float = 2e-4,
    dry_run: bool = False
):
    print("\n=======================================================")
    print("🚀 SAATHI AI - Model Fine-Tuning Pipeline (QLoRA)")
    print("=======================================================")
    print(f"Base Model:       {base_model_name}")
    print(f"Training Dataset: {data_path}")
    print(f"Output Directory: {output_adapter_dir}")
    print(f"Epochs:           {epochs}")
    print(f"Effective Batch:  {batch_size * gradient_accumulation_steps}")
    print("=======================================================\n")

    if not os.path.exists(data_path):
        print(f"⚠️ Dataset {data_path} not found. Generating dataset now...")
        from training.prepare_training_data import generate_saathi_training_dataset
        generate_saathi_training_dataset()

    if dry_run:
        print("💡 DRY RUN MODE: Verifying dataset format and training pipeline simulation...")
        with open(data_path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f.readlines()]
        print(f"✅ Verified {len(lines)} training pairs.")
        print(f"Sample Instruction: {lines[0]['instruction'][:50]}...")
        print(f"Sample Input:       {lines[0]['input']}")
        print(f"Sample Output:      {lines[0]['output'][:50]}...")
        print("\n🎉 Dry run completed successfully! You can run real training with: python3 training/train_qlora_local.py")
        return

    # Real Training Imports
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
        from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
        from datasets import load_dataset
    except ImportError as e:
        print(f"❌ Missing ML libraries: {e}")
        print("Please ensure torch, transformers, peft, and datasets are installed in your venv.")
        return

    print(f"💻 Checking CUDA Device...")
    if torch.cuda.is_available():
        print(f"✅ CUDA GPU Detected: {torch.cuda.get_device_name(0)}")
        print(f"   VRAM Available:   {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
        device_map = "auto"
    else:
        print("⚠️ No CUDA GPU detected, training will run on CPU (slower).")
        device_map = "cpu"

    print(f"\n📥 Step 1: Loading Tokenizer for {base_model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"\n📥 Step 2: Loading Base Model in 4-bit (QLoRA) to save VRAM...")
    try:
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=device_map,
            trust_remote_code=True
        )
    except Exception as err:
        print(f"Note on downloading weights: {err}")
        print("Tip: If downloading is slow or offline, use Google Colab with free T4 GPU.")
        return

    print(f"\n⚙️ Step 3: Configuring LoRA (Low-Rank Adaptation) Parameters...")
    # LoRA config: r=16 (rank), lora_alpha=32 (scaling factor)
    # This modifies <1% of the model weights!
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    print(f"\n📊 Step 4: Formatting Dataset...")
    def format_prompts(example):
        formatted = f"<|im_start|>system\nYou are SAATHI AI, a safe multilingual assistant for Indian daily life.<|im_end|>\n<|im_start|>user\n{example['instruction']}\n\nContext/Input: {example['input']}<|im_end|>\n<|im_start|>assistant\n{example['output']}<|im_end|>"
        tokens = tokenizer(formatted, max_length=512, truncation=True, padding="max_length")
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    raw_dataset = load_dataset("json", data_files={"train": data_path})
    tokenized_dataset = raw_dataset["train"].map(format_prompts)

    print(f"\n🏋️ Step 5: Starting Model Training (Gradient Descent & Loss Optimization)...")
    training_args = TrainingArguments(
        output_dir=output_adapter_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        fp16=torch.cuda.is_available(),
        logging_steps=5,
        save_strategy="epoch",
        save_total_limit=1,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset
    )

    trainer.train()

    print(f"\n💾 Step 6: Saving Fine-Tuned LoRA Adapter to {output_adapter_dir}...")
    model.save_pretrained(output_adapter_dir)
    tokenizer.save_pretrained(output_adapter_dir)

    print("\n🎉 CONGRATULATIONS! You have successfully fine-tuned your first AI model!")
    print(f"The LoRA adapter is saved at: {output_adapter_dir}")
    print("You can now test it with: python3 training/test_fine_tuned_model.py\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SAATHI AI Model Fine-Tuning")
    parser.add_argument("--dry-run", action="store_true", help="Validate dataset and pipeline without downloading weights")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-1.5B-Instruct", help="Base HuggingFace model")
    args = parser.parse_args()

    train_saathi_model(base_model_name=args.model, epochs=args.epochs, dry_run=args.dry_run)
