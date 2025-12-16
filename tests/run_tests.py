# -*- coding: utf-8 -*-
"""
Script chạy test tự động cho Vietnamese Text Corrector
So sánh output thực tế với expected output
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_data import SENTENCES, PARAGRAPHS, ESSAYS, get_test_summary
from difflib import SequenceMatcher


def similarity_score(a: str, b: str) -> float:
    """Tính độ tương đồng giữa 2 chuỗi (0.0 - 1.0)"""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def run_single_test(correct_func, item: dict, category: str) -> dict:
    """Chạy test cho 1 item"""
    input_text = item["input"]
    expected = item["expected"]
    
    try:
        # Gọi hàm sửa lỗi
        actual, explanation = correct_func(input_text)
        
        # Tính độ tương đồng
        score = similarity_score(actual, expected)
        passed = score >= 0.90  # Pass nếu >= 90% giống nhau
        
        return {
            "id": item["id"],
            "category": category,
            "input": input_text[:50] + "..." if len(input_text) > 50 else input_text,
            "expected": expected[:50] + "..." if len(expected) > 50 else expected,
            "actual": actual[:50] + "..." if len(actual) > 50 else actual,
            "similarity": round(score * 100, 1),
            "passed": passed,
            "explanation": explanation[:100] if explanation else ""
        }
    except Exception as e:
        return {
            "id": item["id"],
            "category": category,
            "input": input_text[:50] + "...",
            "expected": expected[:50] + "...",
            "actual": f"ERROR: {str(e)}",
            "similarity": 0,
            "passed": False,
            "explanation": ""
        }


def run_all_tests(correct_func, verbose=True):
    """Chạy tất cả test"""
    results = {
        "sentences": [],
        "paragraphs": [],
        "essays": []
    }
    
    summary = get_test_summary()
    total_passed = 0
    total_tests = 0
    
    print("=" * 60)
    print("🧪 BẮT ĐẦU CHẠY TEST VIETNAMESE TEXT CORRECTOR")
    print("=" * 60)
    
    # Test câu đơn
    print("\n📝 TESTING SENTENCES...")
    for item in SENTENCES:
        result = run_single_test(correct_func, item, "sentence")
        results["sentences"].append(result)
        total_tests += 1
        if result["passed"]:
            total_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        if verbose:
            print(f"  [{result['id']}] {status} ({result['similarity']}%)")
    
    # Test đoạn văn
    print("\n📄 TESTING PARAGRAPHS...")
    for item in PARAGRAPHS:
        result = run_single_test(correct_func, item, "paragraph")
        results["paragraphs"].append(result)
        total_tests += 1
        if result["passed"]:
            total_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        if verbose:
            print(f"  [{result['id']}] {status} ({result['similarity']}%)")
    
    # Test bài văn
    print("\n📚 TESTING ESSAYS...")
    for item in ESSAYS:
        result = run_single_test(correct_func, item, "essay")
        results["essays"].append(result)
        total_tests += 1
        if result["passed"]:
            total_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        if verbose:
            title = item.get("title", f"Essay {item['id']}")
            print(f"  [{result['id']}] {title}: {status} ({result['similarity']}%)")
    
    # In tổng kết
    pass_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ TỔNG HỢP")
    print("=" * 60)
    print(f"  📝 Sentences: {sum(1 for r in results['sentences'] if r['passed'])}/{len(results['sentences'])}")
    print(f"  📄 Paragraphs: {sum(1 for r in results['paragraphs'] if r['passed'])}/{len(results['paragraphs'])}")
    print(f"  📚 Essays: {sum(1 for r in results['essays'] if r['passed'])}/{len(results['essays'])}")
    print("-" * 60)
    print(f"  🎯 TỔNG: {total_passed}/{total_tests} ({pass_rate:.1f}%)")
    print("=" * 60)
    
    if pass_rate >= 90:
        print("🎉 TUYỆT VỜI! Model hoạt động rất tốt!")
    elif pass_rate >= 70:
        print("👍 TỐT! Cần cải thiện thêm một chút.")
    elif pass_rate >= 50:
        print("⚠️ CẦN CẢI THIỆN! Model cần được fine-tune thêm.")
    else:
        print("❌ CẦN XEM XÉT! Prompt hoặc model có vấn đề.")
    
    return {
        "results": results,
        "total_passed": total_passed,
        "total_tests": total_tests,
        "pass_rate": pass_rate
    }


def print_failed_tests(test_results: dict):
    """In chi tiết các test bị fail"""
    print("\n" + "=" * 60)
    print("❌ CHI TIẾT CÁC TEST BỊ FAIL")
    print("=" * 60)
    
    failed_count = 0
    for category in ["sentences", "paragraphs", "essays"]:
        for result in test_results["results"][category]:
            if not result["passed"]:
                failed_count += 1
                print(f"\n[{result['category'].upper()} #{result['id']}]")
                print(f"  📥 Input: {result['input']}")
                print(f"  ✅ Expected: {result['expected']}")
                print(f"  ❌ Actual: {result['actual']}")
                print(f"  📊 Similarity: {result['similarity']}%")
    
    if failed_count == 0:
        print("  🎉 Không có test nào bị fail!")


if __name__ == "__main__":
    # Import model
    try:
        from llm.qwen_model import correct_text
        
        # Chạy test
        results = run_all_tests(correct_text, verbose=True)
        
        # In chi tiết failed tests
        if results["total_passed"] < results["total_tests"]:
            print_failed_tests(results)
            
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("Hãy chạy từ thư mục gốc: python tests/run_tests.py")
