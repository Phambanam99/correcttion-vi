import difflib

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
