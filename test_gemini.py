import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import traceback

# 1. Load và Kiểm tra Key
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")
print(f"🔑 Key đang dùng: {api_key[:5]}...*****")

if not api_key:
    print("❌ LỖI: Không đọc được GEMINI_API_KEY trong file .env")
    exit()

# 2. Cấu hình Gemini
try:
    genai.configure(api_key=api_key)
    print("✅ Cấu hình SDK thành công.")
except Exception as e:
    print(f"❌ Lỗi cấu hình SDK: {e}")
    exit()

# 3. Test Liệt kê Model (Để xem Key có quyền truy cập không)
print("\n📡 Đang thử kết nối đến Google Server...")
try:
    print("--- Danh sách Model khả dụng ---")
    found_flash = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   - {m.name}")
            if "gemini-1.5-flash" in m.name:
                found_flash = True
    print("--------------------------------")
    
    if not found_flash:
        print("⚠️ CẢNH BÁO: Key này không thấy model 'gemini-1.5-flash'. Có thể do Region hoặc loại tài khoản.")
    else:
        print("✅ Đã thấy model 'gemini-1.5-flash'.")

except Exception as e:
    print(f"\n❌ LỖI KẾT NỐI (Quan trọng):")
    print(e)
    print("\n👉 Gợi ý: Kiểm tra lại xem API Key đã được 'Enable' trong Google AI Studio chưa? Hoặc mạng có chặn Google không?")
    exit()

# 4. Test Gửi Prompt đơn giản
print("\n🧠 Đang gửi thử câu lệnh 'Hello'...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Chào bạn, bạn có khỏe không?")
    
    print("\n📝 --- KẾT QUẢ TRẢ VỀ ---")
    print(response.text)
    print("✅ TEST THÀNH CÔNG! Gemini hoạt động tốt.")

except Exception as e:
    print(f"\n❌ LỖI KHI GỌI AI PHÂN TÍCH:")
    # In chi tiết lỗi để debug
    traceback.print_exc()
    
    # Gợi ý sửa lỗi phổ biến
    err_str = str(e)
    if "400" in err_str or "INVALID_ARGUMENT" in err_str:
        print("\n👉 Nguyên nhân: Key không hợp lệ hoặc Model không tồn tại.")
    elif "403" in err_str or "PERMISSION_DENIED" in err_str:
        print("\n👉 Nguyên nhân: API Key bị hạn chế IP hoặc chưa được kích hoạt Billing (nếu dùng bản trả phí).")
    elif "500" in err_str:
        print("\n👉 Nguyên nhân: Server Google đang lỗi, thử lại sau.")
    elif "ValueError" in err_str and "safety" in err_str:
        print("\n👉 Nguyên nhân: Bộ lọc an toàn (Safety Filter) chặn câu trả lời.")