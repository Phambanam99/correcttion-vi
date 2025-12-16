# 📦 HƯỚNG DẪN TRIỂN KHAI OFFLINE
# Vietnamese Text Corrector - Chạy máy nội bộ không cần Internet

---

## 🎯 MỤC TIÊU
Copy toàn bộ ứng dụng sang máy Windows nội bộ và chạy mà KHÔNG cần tải gì từ Internet.

---

## 📋 CHUẨN BỊ TRÊN MÁY CÓ INTERNET

### Bước 1: Tải Models về máy

Models được cache trong thư mục HuggingFace:
```
C:\Users\<username>\.cache\huggingface\hub\
```

Các models cần copy:
- `models--Qwen--Qwen3-4B-Thinking-2507` (~8GB)
- `models--manhngvu--bartpho-autocorrect-demo-100k` (~1.5GB)
- `models--protonx-models--protonx-legal-tc` (~500MB)
- `models--Viet-Mistral--Vistral-7B-Chat` (~14GB, nếu cần)

**Tổng dung lượng: ~10-25GB**

### Bước 2: Export Python Environment

```powershell
# Vào environment vi-llm
conda activate vi-llm

# Export requirements
pip freeze > requirements_full.txt

# Hoặc download wheel files
pip download -r requirements_full.txt -d wheels/
```

### Bước 3: Tạo thư mục deploy

```
vi_text_corrector_offline/
├── app/                          # Code ứng dụng
│   ├── api/
│   ├── gui/
│   ├── llm/
│   ├── processor/
│   ├── protonx_layer/
│   ├── web/
│   ├── config.py
│   ├── main.py
│   └── ...
├── models/                       # HuggingFace models cache
│   ├── models--Qwen--Qwen3-4B-Thinking-2507/
│   ├── models--manhngvu--bartpho-autocorrect-demo-100k/
│   └── models--protonx-models--protonx-legal-tc/
├── python/                       # Có thể dùng embeddable Python
│   └── python-3.10.x-embed-amd64/
├── wheels/                       # Python packages (wheel files)
│   └── *.whl
├── install.bat                   # Script cài đặt
├── run_api.bat                   # Script chạy API
├── run_gui.bat                   # Script chạy GUI
└── README.txt                    # Hướng dẫn
```

---

## 🔧 SCRIPTS CHO MÁY OFFLINE

### install.bat
```batch
@echo off
echo === INSTALLING VIETNAMESE TEXT CORRECTOR ===

REM Set environment
set TRANSFORMERS_OFFLINE=1
set HF_DATASETS_OFFLINE=1
set HF_HOME=%~dp0models

REM Install from wheels (nếu chưa có Python env)
pip install --no-index --find-links=wheels -r requirements.txt

echo === INSTALLATION COMPLETE ===
pause
```

### run_api.bat
```batch
@echo off
echo === STARTING VIETNAMESE TEXT CORRECTOR API ===

REM Set offline mode
set TRANSFORMERS_OFFLINE=1
set HF_DATASETS_OFFLINE=1
set HF_HOME=%~dp0models

cd /d %~dp0app
python api/app.py

pause
```

### run_gui.bat  
```batch
@echo off
echo === STARTING VIETNAMESE TEXT CORRECTOR GUI ===

REM Set offline mode
set TRANSFORMERS_OFFLINE=1
set HF_DATASETS_OFFLINE=1
set HF_HOME=%~dp0models

cd /d %~dp0app
python main.py

pause
```

---

## 📁 COPY MODELS CACHE

### Từ máy có Internet, copy thư mục:

**Nguồn:**
```
C:\Users\NamP7\.cache\huggingface\hub\
```

**Đích (trên máy offline):**
```
D:\vi_text_corrector_offline\models\hub\
```

Hoặc set biến môi trường trỏ tới models:
```batch
set HF_HOME=D:\vi_text_corrector_offline\models
```

---

## 🚀 CÁCH CHẠY TRÊN MÁY OFFLINE

### Option 1: Dùng Conda (Recommended)

1. Copy folder Conda environment:
   ```
   C:\Users\NamP7\miniconda3\envs\vi-llm\
   ```

2. Set PATH và chạy:
   ```batch
   set PATH=D:\vi-llm\Scripts;D:\vi-llm;%PATH%
   python api/app.py
   ```

### Option 2: Dùng Python Embeddable + Wheels

1. Tải `python-3.10.x-embed-amd64.zip` từ python.org
2. Giải nén vào thư mục `python/`
3. Cài packages từ wheels:
   ```batch
   python\python.exe -m pip install --no-index --find-links=wheels torch transformers ...
   ```

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **CUDA/GPU**: Máy offline cần có NVIDIA GPU và driver phù hợp
   - Driver CUDA 11.8+ hoặc 12.x
   - cuDNN phù hợp

2. **Dung lượng**: Cần ít nhất 50GB trống
   - Models: ~25GB
   - Environment: ~15GB
   - App: ~100MB

3. **RAM**: Tối thiểu 16GB RAM

4. **Architecture**: Windows 64-bit, Python 3.10

---

## 📋 CHECKLIST TRƯỚC KHI COPY

- [ ] Copy thư mục `vi_text_corrector/` (code ứng dụng)
- [ ] Copy thư mục `.cache/huggingface/hub/` (models)
- [ ] Copy conda env `vi-llm/` hoặc wheels
- [ ] Tạo file .bat để chạy
- [ ] Test trên máy có Internet với TRANSFORMERS_OFFLINE=1 trước

---

## 🧪 TEST OFFLINE MODE

Trước khi copy sang máy offline, test trên máy hiện tại:

```powershell
# Set offline mode
$env:TRANSFORMERS_OFFLINE=1
$env:HF_DATASETS_OFFLINE=1

# Chạy API
python api/app.py
```

Nếu chạy được → Models đã được cache đầy đủ!

---

## 📞 TROUBLESHOOTING

### Lỗi "Can't find model"
→ Thiếu model trong cache. Copy thêm từ `.cache/huggingface/hub/`

### Lỗi CUDA
→ Cài NVIDIA driver và CUDA toolkit trên máy offline

### Lỗi thiếu package
→ Thêm wheel file vào thư mục wheels/ và cài lại
