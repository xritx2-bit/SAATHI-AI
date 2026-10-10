"""
SAATHI AI - Test Your Fine-Tuned Model
Loads the trained LoRA adapter and compares output before and after fine-tuning.
"""
import os
import sys
import argparse

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_model(
    base_model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
    adapter_dir: str = "training/saathi_lora_adapter"
):
    print("\n=======================================================")
    print("🧪 Testing Fine-Tuned SAATHI Model")
    print("=======================================================")

    test_queries = [
        "Mera bijli ka bill bahut jyada aaya hai meter kharab lagta hai",
        "PM kisan ka 2000 rupaye nahi aaya, land seeding NO dikha raha hai, kya karein?",
        "Flipkart ke khilaf complaint draft karo refund nahi mila"
    ]

    if not os.path.exists(adapter_dir):
        print(f"⚠️ Adapter directory '{adapter_dir}' not found.")
        print("💡 Have you run the training script yet? Run:")
        print("   python3 training/train_qlora_local.py --dry-run (for quick check)")
        print("   python3 training/train_qlora_local.py           (for full training)")
        print("\nShowing sample expected outputs from SAATHI Controller:")
        from saathi.controller.engine import SaathiController
        controller = SaathiController()
        for q in test_queries:
            res = controller.process_query(q)
            print(f"\nQuery:    {q}")
            print(f"Decision: {res.decision}")
            print(f"Response: {res.response_text[:150]}...")
        return

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel

        print(f"Loading Base Model: {base_model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        print(f"Applying Fine-Tuned LoRA Adapter from {adapter_dir}...")
        model = PeftModel.from_pretrained(base_model, adapter_dir)

        print("\n✨ Ready! Running Test Inferences:\n")
        for q in test_queries:
            prompt = f"<|im_start|>system\nYou are SAATHI AI, a safe multilingual assistant for Indian daily life.<|im_end|>\n<|im_start|>user\n{q}<|im_end|>\n<|im_start|>assistant\n"
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.3)
            response = tokenizer.decode(outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=True)
            print(f"❓ User:   {q}")
            print(f"🤖 SAATHI: {response.strip()}\n" + "-"*50)

    except Exception as e:
        print(f"Error testing model: {e}")

if __name__ == "__main__":
    test_model()
