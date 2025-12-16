from PyQt5.QtCore import QThread, pyqtSignal
from llm.bartpho_model import correct_text as bartpho_correct
from protonx_layer.protonx_refine import refine_text_chunked
from processor.diff_utils import generate_change_note


class CorrectionWorker(QThread):
    """
    Worker thread để chạy quá trình sửa lỗi văn bản ở background.
    Pipeline: BartPho (sửa chính tả) -> ProtonX (refine với chunking)
    """
    
    # Signals để communicate với main thread
    progress = pyqtSignal(str)           # Cập nhật progress message
    # index, original, bartpho_result, final, note, explanation
    paragraph_done = pyqtSignal(int, str, str, str, str, str)
    finished = pyqtSignal(str)            # Toàn bộ text đã sửa xong
    error = pyqtSignal(str)               # Nếu có lỗi
    
    # Cấu hình chunking
    MAX_WORDS_PER_CHUNK = 100  # Số từ tối đa mỗi chunk cho ProtonX
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self._is_cancelled = False
    
    def run(self):
        try:
            paragraphs = [p.strip() for p in self.text.split('\n') if p.strip()]
            total = len(paragraphs)
            
            self.progress.emit(f"📊 Bắt đầu xử lý {total} đoạn văn...")
            self.progress.emit(f"🔧 Pipeline: BartPho → ProtonX (chunk {self.MAX_WORDS_PER_CHUNK} từ)")
            
            results = []
            
            for i, original in enumerate(paragraphs):
                if self._is_cancelled:
                    self.progress.emit("⏹️ Đã hủy xử lý")
                    return
                
                self.progress.emit(f"\n🔷 Đoạn [{i+1}/{total}]")
                
                # Bước 1: BartPho sửa chính tả (model chuyên biệt, nhanh)
                self.progress.emit("  📝 Bước 1: BartPho sửa chính tả...")
                bartpho_fixed = bartpho_correct(original)
                
                # Tạo explanation từ sự khác biệt
                explanation = self._generate_explanation(original, bartpho_fixed)
                
                # Bước 2: ProtonX refine (với chunking nếu text dài)
                self.progress.emit("  🔧 Bước 2: ProtonX refine...")
                word_count = len(bartpho_fixed.split())
                
                if word_count > self.MAX_WORDS_PER_CHUNK:
                    self.progress.emit(f"    📦 Text dài ({word_count} từ), chia chunks...")
                    final_text = refine_text_chunked(bartpho_fixed, self.MAX_WORDS_PER_CHUNK)
                else:
                    final_text = refine_text_chunked(bartpho_fixed, self.MAX_WORDS_PER_CHUNK)
                
                # Bước 3: Tạo ghi chú thay đổi
                note = generate_change_note(original, final_text)
                
                # Emit kết quả của đoạn này
                self.paragraph_done.emit(i, original, bartpho_fixed, final_text, note or "", explanation)
                
                results.append(final_text)
            
            # Hoàn thành
            full_result = '\n\n'.join(results)
            self.finished.emit(full_result)
            
        except Exception as e:
            import traceback
            self.error.emit(f"❌ Lỗi: {str(e)}\n{traceback.format_exc()}")
    
    def _generate_explanation(self, original: str, corrected: str) -> str:
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
    
    def cancel(self):
        self._is_cancelled = True
