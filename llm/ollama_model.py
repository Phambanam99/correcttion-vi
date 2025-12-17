# -*- coding: utf-8 -*-
"""
Ollama Online Model for Vietnamese Text Correction
Calls external Ollama API service for text correction
Models are fetched dynamically from the API
"""

import requests
import re
from config import OLLAMA_API_URL, DEFAULT_OLLAMA_MODEL, MAX_NEW_TOKENS, TEMPERATURE
from llm.prompts import SYSTEM_PROMPT

print(f"🌐 [Ollama] API URL: {OLLAMA_API_URL}")
print("=" * 50)

# Cache for available models
_cached_models = None


def fetch_available_models() -> list:
    """
    Fetch available models from Ollama API dynamically.
    Returns list of model names.
    """
    global _cached_models
    
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        models = []
        for model in data.get("models", []):
            name = model.get("name", "")
            if name:
                models.append(name)
        
        _cached_models = models
        print(f"🌐 [Ollama] Fetched {len(models)} models: {models}")
        return models
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ [Ollama] Cannot fetch models: {e}")
        return _cached_models or []


def get_available_models() -> list:
    """Return available Ollama models (cached or fetch new)"""
    if _cached_models is None:
        return fetch_available_models()
    return _cached_models


def correct_text(text: str, model_key: str = None) -> tuple[str, str]:
    """
    Sửa lỗi văn bản bằng Ollama API.
    Returns: (văn_bản_đã_sửa, giải_thích)
    
    Args:
        text: Văn bản cần sửa
        model_key: Tên model (có thể là tên đầy đủ từ API)
    """
    # Get model name - use directly if provided, otherwise use default
    if model_key is None:
        model_key = DEFAULT_OLLAMA_MODEL
    
    # Model name is used directly (fetched from API)
    model_name = model_key
    
    # Build prompt
    user_prompt = f"""Đoạn văn gốc:
{text}

Trả lời theo format (CHỈ 1 LẦN, KHÔNG lặp lại):
[VĂN BẢN ĐÃ SỬA]
(viết đoạn văn đã sửa ở đây)

[GIẢI THÍCH]
(liệt kê các thay đổi ở đây một cách ngắn gọn nhất)

Bắt đầu:
[VĂN BẢN ĐÃ SỬA]
"""
    
    # === LOG: Ollama Input ===
    print("\n" + "=" * 50)
    print(f"📥 [Ollama - {model_name}] INPUT:")
    print("-" * 50)
    print(text[:200] + "..." if len(text) > 200 else text)
    print("-" * 50)
    
    try:
        # Call Ollama API
        response = requests.post(
            f"{OLLAMA_API_URL}/api/chat",
            json={
                "model": model_name,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": TEMPERATURE,
                    "num_predict": MAX_NEW_TOKENS
                }
            },
            timeout=120  # 2 minute timeout
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Extract result from response
        result = data.get("message", {}).get("content", "")
        
        if not result:
            print("⚠️ [Ollama] Empty response from API")
            return text, "Không nhận được phản hồi từ Ollama API"
        
    except requests.exceptions.RequestException as e:
        print(f"❌ [Ollama] API Error: {e}")
        return text, f"Lỗi kết nối Ollama API: {str(e)}"
    
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
    
    # === LOG: Ollama Output ===
    print(f"📤 [Ollama - {model_name}] OUTPUT:")
    print("-" * 50)
    print(f"Văn bản: {corrected_text[:100]}...")
    print(f"Giải thích: {explanation[:100]}..." if explanation else "Không có giải thích")
    print("=" * 50)

    return corrected_text, explanation


def check_ollama_health() -> bool:
    """Check if Ollama API is reachable"""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False
