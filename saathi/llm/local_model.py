"""
SAATHI AI - Local Fine-Tuned Model Inference Engine
Loads the local fine-tuned LoRA model (Qwen2.5-0.5B + SAATHI LoRA Adapter)
on the local NVIDIA GPU or CPU for 100% offline, privacy-first inference.
"""
import os
import sys
from typing import Optional

_LOCAL_MODEL_INSTANCE = None
_LOCAL_TOKENIZER_INSTANCE = None

class LocalFineTunedModel:
    @classmethod
    def is_available(cls, adapter_dir: str = "training/saathi_lora_adapter") -> bool:
        """Check if fine-tuned adapter weights exist."""
        return os.path.exists(os.path.join(adapter_dir, "adapter_model.safetensors"))

    @classmethod
    def load_model(
        cls,
        base_model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
        adapter_dir: str = "training/saathi_lora_adapter"
    ):
        global _LOCAL_MODEL_INSTANCE, _LOCAL_TOKENIZER_INSTANCE
        if _LOCAL_MODEL_INSTANCE is not None and _LOCAL_TOKENIZER_INSTANCE is not None:
            return _LOCAL_MODEL_INSTANCE, _LOCAL_TOKENIZER_INSTANCE

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel

        tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        model = PeftModel.from_pretrained(base_model, adapter_dir)
        model.eval()

        _LOCAL_MODEL_INSTANCE = model
        _LOCAL_TOKENIZER_INSTANCE = tokenizer
        return _LOCAL_MODEL_INSTANCE, _LOCAL_TOKENIZER_INSTANCE

    @classmethod
    def generate(
        cls,
        user_query: str,
        instruction: Optional[str] = None,
        max_new_tokens: int = 256,
        temperature: float = 0.2
    ) -> str:
        """Runs inference using the local fine-tuned model."""
        if not cls.is_available():
            raise FileNotFoundError("Local LoRA adapter not found. Please run training first.")

        import torch
        model, tokenizer = cls.load_model()

        inst = instruction or "You are SAATHI AI, a safe multilingual assistant for Indian daily life."
        prompt = f"<|im_start|>system\n{inst}<|im_end|>\n<|im_start|>user\n{user_query}<|im_end|>\n<|im_start|>assistant\n"

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature if temperature > 0 else None,
                do_sample=(temperature > 0)
            )
        generated_tokens = outputs[0][len(inputs["input_ids"][0]):]
        response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        return response
