# Vietnamese Text Corrector

Phần mềm sửa lỗi văn bản tiếng Việt sử dụng AI (Qwen2.5 + ProtonX).

## 🚀 Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| **📝 Dán văn bản** | Paste nội dung text trực tiếp |
| **📂 Mở file DOCX** | Load file Word từ máy tính |
| **💾 Lưu kết quả** | Export file đã sửa |
| **🔄 So sánh thay đổi** | Bảng hiển thị từ/cụm từ trước và sau khi sửa |
| **📋 Log realtime** | Theo dõi tiến trình xử lý |

## 📦 Cài đặt

```bash
# Clone repo và cài đặt dependencies
pip install -r requirements.txt
```

## 🖥️ Hướng dẫn sử dụng

### Khởi động ứng dụng
```bash
python main.py
```

### Các bước sử dụng

1. **Nhập văn bản**:
   - Cách 1: **Paste** (Ctrl+V) văn bản vào ô "VĂN BẢN GỐC"
   - Cách 2: Click **"📂 Mở File DOCX"** để chọn file Word

2. **Sửa lỗi**:
   - Click **"▶️ Sửa lỗi"** để bắt đầu xử lý
   - Theo dõi tiến trình trong panel **LOG**
   - Xem các thay đổi trong bảng **CÁC THAY ĐỔI**

3. **Lưu kết quả**:
   - Kết quả hiển thị trong ô **"ĐÃ CHỈNH SỬA"**
   - Click **"💾 Lưu kết quả"** để xuất file DOCX

4. **Xóa nội dung**:
   - Click **"🗑️ Xóa"** để reset toàn bộ

## ⚙️ Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|---------|
| GPU VRAM | ≥ 8GB |
| RAM | ≥ 16GB |
| OS | Windows 10/11 |
| Python | ≥ 3.10 |

## 🔧 Công nghệ sử dụng

- **Qwen2.5-7B** (4-bit quantized) - Sửa lỗi ngữ cảnh
- **ProtonX Legal TC** - Text correction
- **PyQt5** - Giao diện Desktop
- **python-docx** - Đọc/ghi file DOCX

## 📸 Giao diện

```
┌─────────────────────────────────────────────────────┐
│  📝 Vietnamese Text Corrector                       │
├─────────────────────────────────────────────────────┤
│  [Mở File] [Sửa lỗi] [Lưu kết quả] [Xóa]           │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐      │
│  │  📥 VĂN BẢN GỐC   │  │  📤 ĐÃ CHỈNH SỬA  │      │
│  └───────────────────┘  └───────────────────┘      │
├─────────────────────────────────────────────────────┤
│  🔄 CÁC THAY ĐỔI                                    │
│  ┌────────────────────┬────────────────────┐       │
│  │  ❌ TRƯỚC          │  ✅ SAU             │       │
│  └────────────────────┴────────────────────┘       │
├─────────────────────────────────────────────────────┤
│  📋 LOG                                             │
└─────────────────────────────────────────────────────┘
```
