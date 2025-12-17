# -*- coding: utf-8 -*-
"""
Qwen Model for Vietnamese Text Correction
Supports dynamic model selection from config
"""

import torch
import re
import threading
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import QWEN_MODELS, DEFAULT_QWEN_MODEL, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from llm.prompts import SYSTEM_PROMPT

# === Device Info ===
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  [Qwen] Device: {device.upper()}")
if device == "cuda":
    print(f"🖥️  [Qwen] GPU: {torch.cuda.get_device_name(0)}")
print(f"🖥️  [Qwen] Available models: {list(QWEN_MODELS.keys())}")
print("=" * 50)

# === Global Model Cache ===
_loaded_model = None
_loaded_tokenizer = None
_loaded_model_key = None
_model_lock = threading.Lock()  # Thread-safe lock for model access


def get_model_and_tokenizer(model_key: str = None):
    """
    Load model dynamically with caching.
    Returns (model, tokenizer) tuple.
    """
    global _loaded_model, _loaded_tokenizer, _loaded_model_key
    
    if model_key is None:
        model_key = DEFAULT_QWEN_MODEL
    
    # Validate model key
    if model_key not in QWEN_MODELS:
        print(f"⚠️ Model '{model_key}' không tồn tại, dùng mặc định: {DEFAULT_QWEN_MODEL}")
        model_key = DEFAULT_QWEN_MODEL
    
    with _model_lock:
        # Return cached if same model
        if _loaded_model is not None and _loaded_model_key == model_key:
            return _loaded_model, _loaded_tokenizer
    
    # Load new model
    model_name = QWEN_MODELS[model_key]
    print(f"📦 [Qwen] Loading model: {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, trust_remote_code=True
    )
    
    # Check if pre-quantized
    is_prequantized = any(x in model_name.lower() for x in ['fp8', 'gptq', 'awq', 'gguf'])
    
    if is_prequantized:
        print(f"📦 [Qwen] Model pre-quantized, loading directly...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            trust_remote_code=True
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            load_in_4bit=True,
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
    
        # Update cache
        _loaded_model = model
        _loaded_tokenizer = tokenizer
        _loaded_model_key = model_key
        
        print(f"✅ [Qwen] Model '{model_key}' loaded successfully!")
        
        return model, tokenizer


# Load default model on import
model, tokenizer = get_model_and_tokenizer(DEFAULT_QWEN_MODEL)


def correct_text(text: str, model_key: str = None) -> tuple[str, str]:
    """
    Sửa lỗi văn bản và trả về tuple (văn_bản_đã_sửa, giải_thích).
    
    Args:
        text: Văn bản cần sửa
        model_key: Key của model trong QWEN_MODELS (optional)
    """
    # Log requested model
    print(f"\n🔍 [Qwen] Requested model_key: {model_key}")
    
    # Get model
    current_model, current_tokenizer = get_model_and_tokenizer(model_key)
    
    prompt = f"""{SYSTEM_PROMPT}

Đoạn văn gốc:
{text}

Trả lời theo format (CHỈ 1 LẦN, KHÔNG lặp lại):
[VĂN BẢN ĐÃ SỬA]
(viết đoạn văn đã sửa ở đây)

[GIẢI THÍCH]
(liệt kê các thay đổi ở đây một cách ngắn gọn nhất)

Bắt đầu:
[VĂN BẢN ĐÃ SỬA]
"""
    # === LOG: Qwen Input ===
    print("\n" + "=" * 50)
    print(f"📥 [Qwen - {_loaded_model_key}] INPUT:")
    print("-" * 50)
    print(text)
    print("-" * 50)

    inputs = current_tokenizer(prompt, return_tensors="pt").to(current_model.device)

    # Thread-safe inference
    with _model_lock:
        with torch.no_grad():
            outputs = current_model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                do_sample=True,
                repetition_penalty=1.2
            )

    result = current_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
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
        parts = result.split("Đoạn văn đã sửa:")
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
    
    # === LOG: Qwen Output ===
    print(f"📤 [Qwen - {_loaded_model_key}] OUTPUT:")
    print("-" * 50)
    print(f"Văn bản: {corrected_text[:100]}...")
    print(f"Giải thích: {explanation[:100]}..." if explanation else "Không có giải thích")
    print("=" * 50)

    return corrected_text, explanation


def get_available_models() -> dict:
    """Return available Qwen models"""
    return QWEN_MODELS.copy()


def get_current_model() -> str:
    """Return currently loaded model key"""
    return _loaded_model_key
