# -*- coding: utf-8 -*-
"""
BartPho Autocorrect Model
Model được fine-tune đặc biệt cho sửa lỗi chính tả tiếng Việt
"""

import torch
from transformers import AutoTokenizer, MBartForConditionalGeneration

MODEL_NAME = "manhngvu/bartpho-autocorrect-demo-100k"

# === LOG: Device Info ===
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  [BartPho] Device: {device.upper()}")
if device == "cuda":
    print(f"🖥️  [BartPho] GPU: {torch.cuda.get_device_name(0)}")
print(f"🖥️  [BartPho] Model: {MODEL_NAME}")
print("=" * 50)

# Load tokenizer và model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = MBartForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
model = model.to(device)
model.eval()


def correct_text(text: str) -> str:
    """
    Sửa lỗi chính tả tiếng Việt bằng BartPho.
    Trả về văn bản đã sửa.
    """
    # === LOG: BartPho Input ===
    print("\n" + "=" * 50)
    print("📥 [BartPho] INPUT:")
    print("-" * 50)
    print(text[:200] + "..." if len(text) > 200 else text)
    print("-" * 50)

    # Tokenize
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    ).to(device)

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3
        )

    # Decode
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # === LOG: BartPho Output ===
    print("📤 [BartPho] OUTPUT:")
    print("-" * 50)
    print(result[:200] + "..." if len(result) > 200 else result)
    print("=" * 50)

    return result


def correct_text_chunked(text: str, max_words_per_chunk: int = 100) -> str:
    """
    Sửa lỗi văn bản dài bằng cách chia thành chunks.
    Mỗi chunk tối đa max_words_per_chunk từ.
    """
    words = text.split()
    
    if len(words) <= max_words_per_chunk:
        return correct_text(text)
    
    # Chia thành chunks
    chunks = []
    for i in range(0, len(words), max_words_per_chunk):
        chunk = " ".join(words[i:i + max_words_per_chunk])
        chunks.append(chunk)
    
    print(f"📦 [BartPho] Chia thành {len(chunks)} chunks ({max_words_per_chunk} từ/chunk)")
    
    # Xử lý từng chunk
    corrected_chunks = []
    for idx, chunk in enumerate(chunks, 1):
        print(f"  🔷 Chunk [{idx}/{len(chunks)}]")
        corrected_chunk = correct_text(chunk)
        corrected_chunks.append(corrected_chunk)
    
    # Ghép lại
    result = " ".join(corrected_chunks)
    
    return result
