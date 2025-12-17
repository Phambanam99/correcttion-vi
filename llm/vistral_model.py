# -*- coding: utf-8 -*-
"""
Vistral-7B-Chat Model
Model tiếng Việt dựa trên Mistral, fine-tuned cho chat

NOTE: Đây là gated model, cần đăng nhập HuggingFace.
Cách 1: Set biến môi trường HF_TOKEN
Cách 2: Chạy `huggingface-cli login` trong terminal
"""

import torch
import re
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from llm.prompts import SYSTEM_PROMPT

MODEL_NAME = "Viet-Mistral/Vistral-7B-Chat"

# === HuggingFace Login ===
HF_TOKEN = os.environ.get("HF_TOKEN", None)
if HF_TOKEN:
    print("🔑 [Vistral] Đang đăng nhập HuggingFace...")
    login(token=HF_TOKEN)
    print("✅ [Vistral] Đăng nhập thành công!")
else:
    print("⚠️ [Vistral] Không tìm thấy HF_TOKEN. Thử login từ cache...")

# === LOG: Device Info ===
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  [Vistral] Device: {device.upper()}")
if device == "cuda":
    print(f"🖥️  [Vistral] GPU: {torch.cuda.get_device_name(0)}")
print(f"🖥️  [Vistral] Model: {MODEL_NAME}")
print("=" * 50)

# Load tokenizer và model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True, token=HF_TOKEN)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.float16,
    trust_remote_code=True,
    token=HF_TOKEN
)


def correct_text(text: str) -> tuple[str, str]:
    """
    Sửa lỗi văn bản tiếng Việt bằng Vistral.
    Trả về tuple (văn_bản_đã_sửa, giải_thích).
    """
    # Format theo Mistral chat template
    prompt = f"""<s>[INST] {SYSTEM_PROMPT}

Đoạn văn gốc:
{text}

Trả lời theo format (CHỈ 1 LẦN, KHÔNG lặp lại):
[VĂN BẢN ĐÃ SỬA]
(viết đoạn văn đã sửa ở đây)

[GIẢI THÍCH]
(liệt kê các thay đổi ở đây một cách ngắn gọn nhất)

Bắt đầu:
[VĂN BẢN ĐÃ SỬA]
[/INST]"""

    # === LOG: Vistral Input ===
    print("\n" + "=" * 50)
    print("📥 [Vistral] INPUT:")
    print("-" * 50)
    print(text[:200] + "..." if len(text) > 200 else text)
    print("-" * 50)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Parse kết quả để tách văn bản và giải thích
    corrected_text = ""
    explanation = ""
    
    # Tìm TẤT CẢ các phần [VĂN BẢN ĐÃ SỬA] và lấy phần CUỐI CÙNG
    all_matches = list(re.finditer(
        r'\[VĂN BẢN ĐÃ SỬA\]\s*(.*?)(?=\[GIẢI TH[IÍỊ][ÊẾỆ]?[CT]H?\]|\[VĂN BẢN|```|$)', 
        result, re.DOTALL | re.IGNORECASE
    ))
    if all_matches:
        corrected_text = all_matches[-1].group(1).strip()
    else:
        # Fallback: lấy phần sau [/INST]
        parts = result.split("[/INST]")
        if len(parts) > 1:
            corrected_text = parts[-1].strip()
        else:
            corrected_text = text  # Giữ nguyên nếu không parse được
    
    # Tìm phần [GIẢI THÍCH]
    explain_match = re.search(r'\[GIẢI TH[IÍỊ][ÊẾỆ]?[CT]H?\]\s*(.*?)$', result, re.DOTALL | re.IGNORECASE)
    if explain_match:
        explanation = explain_match.group(1).strip()
    
    # Làm sạch văn bản
    corrected_text = re.sub(r'```.*?```', '', corrected_text, flags=re.DOTALL)
    corrected_text = re.sub(r'\[GIẢI TH.*', '', corrected_text, flags=re.DOTALL | re.IGNORECASE)
    corrected_text = corrected_text.strip('` \n\t')
    
    # === LOG: Vistral Output ===
    print("📤 [Vistral] OUTPUT:")
    print("-" * 50)
    print(f"Văn bản: {corrected_text[:100]}..." if len(corrected_text) > 100 else f"Văn bản: {corrected_text}")
    print(f"Giải thích: {explanation[:100]}..." if explanation and len(explanation) > 100 else f"Giải thích: {explanation}" if explanation else "Không có giải thích")
    print("=" * 50)

    return corrected_text, explanation
