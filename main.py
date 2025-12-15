from processor.docx_processor import process_docx

if __name__ == "__main__":
    process_docx(
        input_path="input.docx",
        output_path="output_corrected.docx"
    )

    print("✅ Hoàn thành sửa lỗi & tạo comment.")
