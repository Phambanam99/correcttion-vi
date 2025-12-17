import difflib
import re


def is_meaningful_text(text: str, min_words: int = 3) -> bool:
    """
    Kiểm tra văn bản có đủ ý nghĩa để gửi đến AI xử lý hay không.
    
    Một đoạn văn tiếng Việt hợp lệ phải có ít nhất 1 câu,
    và một câu phải có ít nhất 3 từ có ý nghĩa.
    
    Args:
        text: Văn bản cần kiểm tra
        min_words: Số từ tối thiểu (mặc định: 3)
    
    Returns:
        True nếu văn bản có ý nghĩa, False nếu không
    """
    if not text or not text.strip():
        return False
    
    # Tìm các từ có chứa chữ cái (tiếng Việt hoặc Latin)
    # Pattern này match các từ có ít nhất 1 ký tự chữ (Unicode letter)
    words = re.findall(r'\b\w*[a-zA-ZÀ-ỹ]+\w*\b', text, re.UNICODE)
    
    return len(words) >= min_words


def generate_change_note(original: str, corrected: str):
    if original.strip() == corrected.strip():
        return None

    diff = difflib.ndiff(
        original.split(),
        corrected.split()
    )

    changes = []
    for d in diff:
        if d.startswith("- "):
            changes.append(f"Bỏ: {d[2:]}")
        elif d.startswith("+ "):
            changes.append(f"Thêm: {d[2:]}")

    note = (
        "AI đã chỉnh sửa đoạn văn.\n\n"
        f"Đoạn gốc:\n{original}\n\n"
        f"Đoạn sau khi sửa:\n{corrected}\n\n"
        "Chi tiết thay đổi:\n- " + "\n- ".join(changes[:20])
    )

    return note
