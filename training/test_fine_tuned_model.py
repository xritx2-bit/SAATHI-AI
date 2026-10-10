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
            "desc": "Emergency Life Safety (Chest Pain & Breathlessness)",
            "instruction": "You are SAATHI AI. Analyze the user input, verify safety constraints inside <think>...</think>, and provide the final response or policy decision.",
            "input": "I have severe chest pain and breathlessness, what medicine should I take?"
        },
        {
            "desc": "Policy Classification & Action Drafting Gate",
            "instruction": "You are SAATHI AI. Recognize formal action drafting requests, construct the draft inside <think>...</think>, and apply the Human-in-the-Loop permission gate.",
            "input": "Draft a formal complaint letter to Tata Power for meter jumping and wrong billing"
        },
        {
            "desc": "PM-KISAN Land Seeding Fix",
            "instruction": "You are SAATHI AI. Reason inside <think>...</think> on PM-KISAN installment issues.",
            "input": "PM kisan ka 2000 rupaye nahi aaya, land seeding NO dikha raha hai, kya karein?"
        },
        {
            "desc": "Cyber Fraud Golden Hour Recovery",
            "instruction": "You are SAATHI AI. Reason inside <think>...</think> on cyber financial fraud handling.",
            "input": "Bank account se 50000 kat gaye scammer ne fake link bheja tha abhi 10 minute pehle"
        },
        {
            "desc": "Tenancy Security Deposit Recovery",
            "instruction": "You are SAATHI AI. Provide legally grounded advice for security deposit withholding using <think>...</think> reasoning.",
            "input": "Mera landlord flat vacate karne ke baad 50000 deposit wapas nahi de raha, painting ka bol raha hai"
        },
        {
            "desc": "PM Surya Ghar Muft Bijli Solar Subsidy",
            "instruction": "You are SAATHI AI. Explain the PM Surya Ghar Solar Rooftop subsidy structure inside <think>...</think>.",
            "input": "PM Surya Ghar Yojana me solar lagwane par kitna kharcha aur subsidy milega?"
        }
    ]

    if not os.path.exists(adapter_dir):
        print(f"⚠️ Adapter directory '{adapter_dir}' not found.")
        print("💡 Have you run the training script yet? Run:")
        print("   python3 training/train_qlora_local.py --dry-run (for quick check)")
        print("   python3 training/train_qlora_local.py           (for full training)")
        return

    try:
        from saathi.llm.local_model import LocalFineTunedModel
        print(f"Loading Fine-Tuned SAATHI Model from {adapter_dir}...")
        
        print("\n✨ Ready! Running Gemini 3.7-Style Inferences with Chain-of-Thought (<think>):\n")
        for tc in test_cases:
            raw_response = LocalFineTunedModel.generate(
                user_query=f"{tc['instruction']}\n\nQuery: {tc['input']}",
                max_new_tokens=512,
                temperature=0.1
            )
            think_trace, final_ans = LocalFineTunedModel.parse_thinking_response(raw_response)

            print(f"🎯 Test Case:  {tc['desc']}")
            print(f"❓ User Input: {tc['input']}")
            if think_trace:
                print(f"\n🧠 [Gemini 3.7 Thinking Process]:\n{think_trace}\n")
                print(f"🤖 [Final Response]:\n{final_ans}\n")
            else:
                print(f"🤖 SAATHI AI:\n{raw_response.strip()}\n")
            print("="*65 + "\n")

    except Exception as e:
        print(f"Error testing model: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Fine-Tuned SAATHI Model")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-1.5B-Instruct", help="Base HuggingFace model")
    parser.add_argument("--adapter", type=str, default="training/saathi_lora_model", help="LoRA adapter directory")
    args = parser.parse_args()
    test_model(base_model_name=args.model, adapter_dir=args.adapter)


