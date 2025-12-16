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
    Refine văn bản dài bằng cách chia thành chunks theo CÂU.
    Đảm bảo không cắt giữa câu.
    """
    import re
    
    words = text.split()
    
    if len(words) <= max_words_per_chunk:
        return refine_text(text)
    
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
    
    print(f"📦 [ProtonX] Chia thành {len(chunks)} chunks (theo câu, max {max_words_per_chunk} từ/chunk)")
    
    # Xử lý từng chunk
    refined_chunks = []
    for idx, chunk in enumerate(chunks, 1):
        print(f"  🔷 ProtonX Chunk [{idx}/{len(chunks)}]: {len(chunk.split())} từ")
        refined_chunk = refine_text(chunk)
        refined_chunks.append(refined_chunk)
    
    # Ghép lại
    result = " ".join(refined_chunks)
    
    return result

