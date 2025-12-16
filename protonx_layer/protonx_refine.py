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


def refine_text_chunked(text: str, max_words_per_chunk: int = 100) -> str:
    """
    Refine văn bản dài bằng cách chia thành chunks.
    Mỗi chunk tối đa max_words_per_chunk từ.
    """
    words = text.split()
    
    if len(words) <= max_words_per_chunk:
        return refine_text(text)
    
    # Chia thành chunks
    chunks = []
    for i in range(0, len(words), max_words_per_chunk):
        chunk = " ".join(words[i:i + max_words_per_chunk])
        chunks.append(chunk)
    
    print(f"📦 [ProtonX] Chia thành {len(chunks)} chunks ({max_words_per_chunk} từ/chunk)")
    
    # Xử lý từng chunk
    refined_chunks = []
    for idx, chunk in enumerate(chunks, 1):
        print(f"  🔷 ProtonX Chunk [{idx}/{len(chunks)}]")
        refined_chunk = refine_text(chunk)
        refined_chunks.append(refined_chunk)
    
    # Ghép lại
    result = " ".join(refined_chunks)
    
    return result
