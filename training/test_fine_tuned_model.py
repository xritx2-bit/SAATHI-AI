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
    adapter_dir: str = "training/saathi_lora_model"
):
    print("\n=======================================================")
    print("🧪 Testing Fine-Tuned SAATHI Model")
    print("=======================================================")

    test_cases = [
        {
            "desc": "Policy Classification (Emergency Escalation)",
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "I have severe chest pain what medicine to take?"
        },
        {
            "desc": "Policy Classification (Action Drafting Gate)",
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "Draft complaint letter to Tata Power for faulty meter reading"
        },
        {
            "desc": "Domain Assistance (PM-Kisan Land Seeding Fix)",
            "instruction": "Explain how PM-KISAN Samman Nidhi installment errors (like land seeding or eKYC) can be fixed.",
            "input": "PM kisan ka 2000 rupaye nahi aaya, land seeding NO dikha raha hai, kya karein?"
        },
        {
            "desc": "Domain Assistance (Cyber Fraud 1930)",
            "instruction": "Explain how to report cyber financial fraud and recover stolen money.",
            "input": "Online fraud ho gaya paise kat gaye, helpline number kya hai?"
        },
        {
            "desc": "Domain Assistance (Hindi PM-Kisan Scheme)",
            "instruction": "Explain PM-KISAN scheme eligibility and benefits in Hindi.",
            "input": "PM किसान योजना में कितने पैसे मिलते हैं और किसे मिलते हैं?"
        }
    ]

    if not os.path.exists(adapter_dir):
        print(f"⚠️ Adapter directory '{adapter_dir}' not found.")
        print("💡 Have you run the training script yet? Run:")
        print("   python3 training/train_qlora_local.py --dry-run (for quick check)")
        print("   python3 training/train_qlora_local.py           (for full training)")
        print("\nShowing sample expected outputs from SAATHI Controller:")
        from saathi.controller.engine import SaathiController
        controller = SaathiController()
        for tc in test_cases:
            res = controller.process_query(tc["input"])
            print(f"\nQuery:    {tc['input']}")
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
        for tc in test_cases:
            prompt = f"<|im_start|>system\nYou are SAATHI AI, a safe multilingual assistant for Indian daily life.<|im_end|>\n<|im_start|>user\n{tc['instruction']}\n\nContext/Input: {tc['input']}<|im_end|>\n<|im_start|>assistant\n"
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.1, do_sample=False)
            response = tokenizer.decode(outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=True)
            print(f"🎯 Test Case:  {tc['desc']}")
            print(f"❓ User Input: {tc['input']}")
            print(f"🤖 SAATHI AI: {response.strip()}\n" + "="*60 + "\n")

    except Exception as e:
        print(f"Error testing model: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Fine-Tuned SAATHI Model")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-0.5B-Instruct", help="Base HuggingFace model")
    parser.add_argument("--adapter", type=str, default="training/saathi_lora_adapter", help="LoRA adapter directory")
    args = parser.parse_args()
    test_model(base_model_name=args.model, adapter_dir=args.adapter)
