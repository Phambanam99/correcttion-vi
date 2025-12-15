import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "protonx-models/protonx-legal-tc"

# === LOG: Device Info ===
device = "cpu"  # ProtonX chạy trên CPU
print(f"🖥️  [ProtonX] Device: {device.upper()}")
print(f"🖥️  [ProtonX] Model: {MODEL_NAME}")
print("=" * 50)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    device_map="cpu",      # RẤT QUAN TRỌNG
    torch_dtype=torch.float32
)

model.eval()

def refine_text(text: str) -> str:
    # === LOG: ProtonX Input ===
    print("\n" + "=" * 50)
    print("📥 [ProtonX] INPUT:")
    print("-" * 50)
    print(text)
    print("-" * 50)

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            num_beams=4,
            early_stopping=True
        )

    result = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    # === LOG: ProtonX Output ===
    print("📤 [ProtonX] OUTPUT:")
    print("-" * 50)
    print(result)
    print("=" * 50)

    return result
