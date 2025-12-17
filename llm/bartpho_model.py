# -*- coding: utf-8 -*-
"""
BartPho Autocorrect Model
Model được fine-tune đặc biệt cho sửa lỗi chính tả tiếng Việt
"""

import torch
from transformers import AutoTokenizer, MBartForConditionalGeneration

MODEL_NAME = "bmd1905/vietnamese-correction-v2"

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
    Sửa lỗi văn bản dài bằng cách chia thành chunks theo CÂU.
    Đảm bảo không cắt giữa câu.
    """
    import re
    
    words = text.split()
    
    if len(words) <= max_words_per_chunk:
        return correct_text(text)
    
    # Chia theo câu (dấu . ! ? kết thúc)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Gom câu thành chunks, mỗi chunk không quá max_words_per_chunk từ
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_word_count = len(sentence.split())
        
        # Nếu 1 câu đã quá dài → xử lý riêng
        if sentence_word_count > max_words_per_chunk:
            # Lưu chunk hiện tại trước
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
            # Thêm câu dài như 1 chunk riêng
            chunks.append(sentence)
        # Nếu thêm câu này vẫn trong giới hạn
        elif current_word_count + sentence_word_count <= max_words_per_chunk:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        # Nếu thêm câu này vượt giới hạn → tạo chunk mới
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_word_count
    
    # Thêm chunk cuối cùng
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    print(f"📦 [BartPho] Chia thành {len(chunks)} chunks (theo câu, max {max_words_per_chunk} từ/chunk)")
    
    # Xử lý từng chunk
    corrected_chunks = []
    for idx, chunk in enumerate(chunks, 1):
        print(f"  🔷 Chunk [{idx}/{len(chunks)}]: {len(chunk.split())} từ")
        corrected_chunk = correct_text(chunk)
        corrected_chunks.append(corrected_chunk)
    
    # Ghép lại
    result = " ".join(corrected_chunks)
    
    return result
