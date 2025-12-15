import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from llm.prompts import SYSTEM_PROMPT

# === LOG: Device Info ===
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  [Qwen2.5] Device: {device.upper()}")
if device == "cuda":
    print(f"🖥️  [Qwen2.5] GPU: {torch.cuda.get_device_name(0)}")
print(f"🖥️  [Qwen2.5] Model: {MODEL_NAME}")
print("=" * 50)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME, trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.float16,
    trust_remote_code=True
)

def correct_text(text: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

Đoạn văn:
{text}

Đoạn văn đã sửa:
"""
    # === LOG: Qwen Input ===
    print("\n" + "=" * 50)
    print("📥 [Qwen2.5] INPUT:")
    print("-" * 50)
    print(text)
    print("-" * 50)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    corrected = result.split("Đoạn văn đã sửa:")[-1].strip()

    # === LOG: Qwen Output ===
    print("📤 [Qwen2.5] OUTPUT:")
    print("-" * 50)
    print(corrected)
    print("=" * 50)

    return corrected
