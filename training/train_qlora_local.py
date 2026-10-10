"""
🎓 SAATHI AI - High-Potential Local QLoRA Fine-Tuning Pipeline
-------------------------------------------------------------------------
Optimized for NVIDIA GeForce RTX 4050 (6GB VRAM) & CUDA acceleration.
Uses 4-bit NormalFloat (NF4) quantization + Rank-64 LoRA over Attention & MLP layers.
-------------------------------------------------------------------------
"""
import os
import sys
import argparse
import json
import time

def train_saathi_model(
    base_model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
    data_path: str = "data/training_data/train.jsonl",
    output_adapter_dir: str = "training/saathi_lora_model",
    epochs: int = 15,
    batch_size: int = 1,
    gradient_accumulation_steps: int = 8,
    learning_rate: float = 2e-4,
    lora_rank: int = 64,
    lora_alpha: int = 128,
    dry_run: bool = False
):
    print("\n=======================================================")
    print("🚀 SAATHI AI - High-Potential Model Fine-Tuning (QLoRA)")
    print("=======================================================")
    print(f"Base Architecture: {base_model_name}")
    print(f"Training Dataset:  {data_path}")
    print(f"Output Directory:  {output_adapter_dir}")
    print(f"Epochs:            {epochs}")
    print(f"LoRA Capacity:     Rank r={lora_rank}, Alpha={lora_alpha}")
    print(f"Effective Batch:   {batch_size * gradient_accumulation_steps}")
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
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            Trainer,
            BitsAndBytesConfig
        )
        from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
        from datasets import load_dataset
    except ImportError as e:
        print(f"❌ Missing ML libraries: {e}")
        print("Please ensure torch, transformers, peft, bitsandbytes, and datasets are installed.")
        return

    print(f"💻 Checking Hardware & CUDA Capabilities...")
    has_cuda = torch.cuda.is_available()
    if has_cuda:
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        free_vram = torch.cuda.mem_get_info()[0] / (1024**3)
        print(f"✅ Active GPU:    {gpu_name}")
        print(f"   Total VRAM:    {vram_gb:.2f} GB")
        print(f"   Free VRAM:     {free_vram:.2f} GB")
        device_map = "auto"
    else:
        print("⚠️ No CUDA GPU detected, training will run on CPU.")
        device_map = "cpu"

    print(f"\n📥 Step 1: Loading Tokenizer for {base_model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"\n📥 Step 2: Loading Base Model with 4-bit Quantization (NF4)...")
    bnb_config = None
    if has_cuda:
        try:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16
            )
        except Exception:
            bnb_config = None

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config if has_cuda else None,
        torch_dtype=torch.float16 if has_cuda else torch.float32,
        device_map=device_map,
        trust_remote_code=True
    )

    if has_cuda:
        model = prepare_model_for_kbit_training(model)

    print(f"\n⚙️ Step 3: Configuring Maximum-Potential LoRA (Rank={lora_rank}, Alpha={lora_alpha})...")
    # Targets all attention projections AND feed-forward MLP projections
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_rank,
        lora_alpha=lora_alpha,
        lora_dropout=0.05,
        target_modules=target_modules,
        bias="none"
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    print(f"\n📊 Step 4: Tokenizing Instruction Dataset...")
    def format_prompts(example):
        formatted = f"<|im_start|>system\nYou are SAATHI AI, a safe evidence-gated public assistant for Indian citizens.<|im_end|>\n<|im_start|>user\n{example['instruction']}\n\nQuery: {example['input']}<|im_end|>\n<|im_start|>assistant\n{example['output']}<|im_end|>"
        tokens = tokenizer(formatted, max_length=512, truncation=True, padding="max_length")
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    raw_dataset = load_dataset("json", data_files={"train": data_path})
    tokenized_dataset = raw_dataset["train"].map(format_prompts)

    print(f"\n🏋️ Step 5: Executing GPU Training Loop ({epochs} Epochs on {base_model_name})...")
    training_args = TrainingArguments(
        output_dir=output_adapter_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        lr_scheduler_type="cosine",
        warmup_steps=5,
        fp16=has_cuda,
        gradient_checkpointing=True,
        logging_steps=5,
        save_strategy="epoch",
        save_total_limit=1,
        optim="paged_adamw_8bit" if has_cuda else "adamw_torch",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset
    )

    t_start = time.time()
    train_result = trainer.train()
    training_duration = time.time() - t_start

    print(f"\n💾 Step 6: Saving Fine-Tuned Model Weights & Metadata to {output_adapter_dir}...")
    model.save_pretrained(output_adapter_dir)
    tokenizer.save_pretrained(output_adapter_dir)

    # Save training metrics log
    metrics_path = os.path.join(output_adapter_dir, "training_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({
            "base_model": base_model_name,
            "epochs": epochs,
            "lora_rank": lora_rank,
            "lora_alpha": lora_alpha,
            "train_loss": train_result.training_loss,
            "training_duration_seconds": round(training_duration, 2),
            "device": gpu_name if has_cuda else "CPU",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, f, indent=2)

    print(f"\n=======================================================")
    print("🎉 FULL POTENTIAL TRAINING COMPLETED SUCCESSFULLY!")
    print(f"Final Training Loss: {train_result.training_loss:.4f}")
    print(f"Total Time Elapsed:  {training_duration:.1f} seconds")
    print(f"Adapter Saved To:    {output_adapter_dir}")
    print("=======================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SAATHI AI High-Potential Model Fine-Tuning")
    parser.add_argument("--dry-run", action="store_true", help="Validate dataset without training")
    parser.add_argument("--epochs", type=int, default=15, help="Number of training epochs")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-0.5B-Instruct", help="Base HuggingFace model")
    parser.add_argument("--rank", type=int, default=64, help="LoRA Rank capacity")
    args = parser.parse_args()

    train_saathi_model(
        base_model_name=args.model,
        epochs=args.epochs,
        lora_rank=args.rank,
        lora_alpha=args.rank * 2,
        dry_run=args.dry_run
    )
