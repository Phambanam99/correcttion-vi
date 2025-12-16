# -*- coding: utf-8 -*-
"""
Flask API cho Vietnamese Text Corrector
Pipeline: [BartPho/Qwen/Vistral] -> ProtonX (với chunking)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.bartpho_model import correct_text as bartpho_correct, correct_text_chunked as bartpho_chunked
from llm.qwen_model import correct_text as qwen_correct
from protonx_layer.protonx_refine import refine_text_chunked
from processor.diff_utils import generate_change_note

# Load Vistral model (gated model, cần HF_TOKEN)
vistral_available = False
vistral_correct = None

try:
    from llm.vistral_model import correct_text as vistral_correct
    vistral_available = True
    print("✅ Vistral model loaded successfully")
except Exception as e:
    print(f"⚠️ Vistral model không khả dụng: {e}")
    vistral_available = False

app = Flask(__name__)
CORS(app)  # Enable CORS for web frontend

# Cấu hình
MAX_WORDS_PER_CHUNK = 100
AVAILABLE_MODELS = ["bartpho", "qwen", "vistral"]
DEFAULT_MODEL = "bartpho"



def correct_with_model(text: str, model: str = DEFAULT_MODEL) -> tuple:
    """
    Sửa lỗi văn bản với model được chọn.
    Returns: (corrected_text, explanation)
    """
    word_count = len(text.split())
    
    if model == "qwen":
        # Qwen trả về tuple (text, explanation)
        corrected, explanation = qwen_correct(text)
        return corrected, explanation
    elif model == "vistral":
        # Vistral model
        if vistral_available and vistral_correct:
            corrected, explanation = vistral_correct(text)
            return corrected, explanation
        else:
            # Fallback to BartPho nếu Vistral không available
            print("⚠️ Vistral không khả dụng, dùng BartPho thay thế")
            if word_count > MAX_WORDS_PER_CHUNK:
                corrected = bartpho_chunked(text, MAX_WORDS_PER_CHUNK)
            else:
                corrected = bartpho_correct(text)
            explanation = "⚠️ Vistral không khả dụng (cần HF_TOKEN). Đã dùng BartPho."
            return corrected, explanation
    else:
        # BartPho (default)
        if word_count > MAX_WORDS_PER_CHUNK:
            corrected = bartpho_chunked(text, MAX_WORDS_PER_CHUNK)
        else:
            corrected = bartpho_correct(text)
        explanation = generate_explanation(text, corrected)
        return corrected, explanation


def generate_explanation(original: str, corrected: str) -> str:
    """Tạo giải thích ngắn gọn về các thay đổi"""
    if original.strip() == corrected.strip():
        return "Không có thay đổi."
    
    original_words = set(original.lower().split())
    corrected_words = set(corrected.lower().split())
    
    added = corrected_words - original_words
    removed = original_words - corrected_words
    
    explanations = []
    if removed:
        explanations.append(f"Sửa: {', '.join(list(removed)[:5])}")
    if added:
        explanations.append(f"Thành: {', '.join(list(added)[:5])}")
    
    return " → ".join(explanations) if explanations else "Đã sửa dấu và định dạng."


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Vietnamese Text Corrector API is running",
        "available_models": AVAILABLE_MODELS,
        "default_model": DEFAULT_MODEL
    })


@app.route('/api/correct', methods=['POST'])
def correct_text():
    """
    Sửa lỗi văn bản
    
    Request body:
    {
        "text": "văn bản cần sửa"
    }
    
    Response:
    {
        "success": true,
        "original": "văn bản gốc",
        "corrected": "văn bản đã sửa",
        "bartpho_result": "kết quả từ BartPho",
        "explanation": "giải thích thay đổi",
        "note": "ghi chú chi tiết"
    }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field in request body"
            }), 400
        
        original = data['text'].strip()
        if not original:
            return jsonify({
                "success": False,
                "error": "Text cannot be empty"
            }), 400
        
        # Bước 1: BartPho sửa chính tả
        word_count = len(original.split())
        if word_count > MAX_WORDS_PER_CHUNK:
            bartpho_fixed = bartpho_chunked(original, MAX_WORDS_PER_CHUNK)
        else:
            bartpho_fixed = bartpho_correct(original)
        
        # Tạo explanation
        explanation = generate_explanation(original, bartpho_fixed)
        
        # Bước 2: ProtonX refine
        final_text = refine_text_chunked(bartpho_fixed, MAX_WORDS_PER_CHUNK)
        
        # Tạo ghi chú thay đổi
        note = generate_change_note(original, final_text)
        
        return jsonify({
            "success": True,
            "original": original,
            "corrected": final_text,
            "bartpho_result": bartpho_fixed,
            "explanation": explanation,
            "note": note or ""
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/correct-paragraphs', methods=['POST'])
def correct_paragraphs():
    """
    Sửa lỗi nhiều đoạn văn (tách bằng newline)
    
    Request body:
    {
        "text": "đoạn 1\nđoạn 2\nđoạn 3",
        "model": "bartpho" hoặc "qwen" (mặc định: bartpho)
    }
    
    Response:
    {
        "success": true,
        "model_used": "bartpho",
        "results": [...],
        "full_corrected": "toàn bộ văn bản đã sửa"
    }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field in request body"
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                "success": False,
                "error": "Text cannot be empty"
            }), 400
        
        # Lấy model được chọn (mặc định: bartpho)
        model = data.get('model', DEFAULT_MODEL).lower()
        if model not in AVAILABLE_MODELS:
            model = DEFAULT_MODEL
        
        # Chia thành các đoạn
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        results = []
        corrected_paragraphs = []
        
        for i, original in enumerate(paragraphs):
            # Bước 1: Sửa lỗi với model được chọn
            model_fixed, explanation = correct_with_model(original, model)
            
            # Bước 2: ProtonX refine
            final_text = refine_text_chunked(model_fixed, MAX_WORDS_PER_CHUNK)
            
            note = generate_change_note(original, final_text)
            
            results.append({
                "index": i,
                "original": original,
                "corrected": final_text,
                "model_result": model_fixed,
                "explanation": explanation,
                "note": note or "",
                "has_changes": original != final_text
            })
            
            corrected_paragraphs.append(final_text)
        
        return jsonify({
            "success": True,
            "model_used": model,
            "total_paragraphs": len(paragraphs),
            "results": results,
            "full_corrected": '\n\n'.join(corrected_paragraphs)
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/upload-docx', methods=['POST'])
def upload_docx():
    """
    Upload và đọc nội dung file DOCX
    
    Request: multipart/form-data với file 'file'
    
    Response:
    {
        "success": true,
        "filename": "document.docx",
        "text": "nội dung văn bản"
    }
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded"
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        if not file.filename.endswith('.docx'):
            return jsonify({
                "success": False,
                "error": "Only .docx files are supported"
            }), 400
        
        # Đọc file DOCX
        from docx import Document
        import io
        
        doc = Document(io.BytesIO(file.read()))
        
        # Lấy text từ tất cả paragraphs
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        text = '\n'.join(paragraphs)
        
        return jsonify({
            "success": True,
            "filename": file.filename,
            "text": text,
            "paragraph_count": len(paragraphs)
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/download-docx', methods=['POST'])
def download_docx():
    """
    Tạo file DOCX từ văn bản
    
    Request body:
    {
        "text": "văn bản đã sửa",
        "filename": "output.docx" (optional)
    }
    
    Response: File DOCX
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field"
            }), 400
        
        text = data['text'].strip()
        filename = data.get('filename', 'corrected_output.docx')
        
        if not text:
            return jsonify({
                "success": False,
                "error": "Text cannot be empty"
            }), 400
        
        # Tạo file DOCX
        from docx import Document
        from flask import send_file
        import io
        
        doc = Document()
        
        # Thêm các đoạn văn
        for para in text.split('\n\n'):
            if para.strip():
                doc.add_paragraph(para.strip())
        
        # Lưu vào memory buffer
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Vietnamese Text Corrector API...")
    print("📍 API running at: http://localhost:5000")
    print("📖 Endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/correct - Correct single text")
    print("   POST /api/correct-paragraphs - Correct multiple paragraphs")
    print("   POST /api/upload-docx - Upload DOCX file")
    print("   POST /api/download-docx - Download as DOCX")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
