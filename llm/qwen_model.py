import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from llm.prompts import SYSTEM_PROMPT

# === LOG: Device Info ===
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  [Qwen] Device: {device.upper()}")
if device == "cuda":
    print(f"🖥️  [Qwen] GPU: {torch.cuda.get_device_name(0)}")
print(f"🖥️  [Qwen] Model: {MODEL_NAME}")
print("=" * 50)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME, trust_remote_code=True
)

# Kiểm tra nếu model đã quantize sẵn (FP8, GPTQ, AWQ, etc.)
is_prequantized = any(x in MODEL_NAME.lower() for x in ['fp8', 'gptq', 'awq', 'gguf'])

if is_prequantized:
    # Model đã quantize sẵn - không cần load_in_4bit
    print(f"📦 [Qwen] Model pre-quantized, loading directly...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        trust_remote_code=True
    )
else:
    # Model chưa quantize - dùng 4-bit
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        load_in_4bit=True,
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

def correct_text(text: str) -> tuple[str, str]:
    """
    Sửa lỗi văn bản và trả về tuple (văn_bản_đã_sửa, giải_thích).
    """
    prompt = f"""{SYSTEM_PROMPT}

Đoạn văn gốc:
{text}

Trả lời theo format (CHỈ 1 LẦN, KHÔNG lặp lại):
[VĂN BẢN ĐÃ SỬA]
(viết đoạn văn đã sửa ở đây)

[GIẢI THÍCH]
(liệt kê các thay đổi ở đây)

Bắt đầu:
[VĂN BẢN ĐÃ SỬA]
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
            top_p=TOP_P,
            do_sample=True,
            repetition_penalty=1.2  # Ngăn lặp lại output
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Parse kết quả để tách văn bản và giải thích
    corrected_text = ""
    explanation = ""
    
    # Tìm TẤT CẢ các phần [VĂN BẢN ĐÃ SỬA] và lấy phần CUỐI CÙNG (sau "Bắt đầu:")
    # Regex bắt cả các biến thể sai chính tả: [GIẢI THỊCH], [GIẢI THITIES], etc.
    all_matches = list(re.finditer(
        r'\[VĂN BẢN ĐÃ SỬA\]\s*(.*?)(?=\[GIẢI TH[IÍỊ][ÊẾỆ]?[CT]H?\]|\[VĂN BẢN|```|$)', 
        result, re.DOTALL | re.IGNORECASE
    ))
    if all_matches:
        # Lấy match cuối cùng (kết quả thực tế, không phải template)
        corrected_text = all_matches[-1].group(1).strip()
    else:
        # Fallback: lấy phần sau "Đoạn văn đã sửa:" nếu model không tuân theo format
        parts = result.split("Đoạn văn đã sửa:")
        if len(parts) > 1:
            corrected_text = parts[-1].strip()
        else:
            corrected_text = text  # Giữ nguyên nếu không parse được
    
    # Tìm phần [GIẢI THÍCH] (bắt cả biến thể sai chính tả)
    explain_match = re.search(r'\[GIẢI TH[IÍỊ][ÊẾỆ]?[CT]H?\]\s*(.*?)$', result, re.DOTALL | re.IGNORECASE)
    if explain_match:
        explanation = explain_match.group(1).strip()
    
    # Làm sạch văn bản - loại bỏ phần giải thích nếu lọt vào
    corrected_text = re.sub(r'```.*?```', '', corrected_text, flags=re.DOTALL)
    corrected_text = re.sub(r'\[GIẢI TH.*', '', corrected_text, flags=re.DOTALL | re.IGNORECASE)  # Cắt từ [GIẢI TH...
    corrected_text = corrected_text.strip('` \n\t')
    
    # === LOG: Qwen Output ===
    print("📤 [Qwen2.5] OUTPUT:")
    print("-" * 50)
    print(f"Văn bản: {corrected_text[:100]}...")
    print(f"Giải thích: {explanation[:100]}..." if explanation else "Không có giải thích")
    print("=" * 50)

    return corrected_text, explanation

