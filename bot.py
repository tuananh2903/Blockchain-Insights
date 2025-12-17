import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# --- CẤU HÌNH ---
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def split_text_smart(text, limit=1900):
    """
    Hàm chia nhỏ văn bản thông minh:
    - Không cắt giữa từ.
    - Ưu tiên cắt ở dấu xuống dòng (\n) để giữ trọn vẹn đoạn văn.
    - Nếu không có \n thì cắt ở dấu cách gần nhất.
    """
    chunks = []
    current_text = text.strip()

    while len(current_text) > limit:
        # 1. Tìm dấu xuống dòng (\n) gần nhất trong khoảng limit
        # rfind tìm từ phải sang trái (từ vị trí limit lùi về 0)
        split_index = current_text.rfind('\n', 0, limit)

        # 2. Nếu không tìm thấy xuống dòng, tìm dấu cách ( )
        if split_index == -1:
            split_index = current_text.rfind(' ', 0, limit)

        # 3. Trường hợp hiếm: 1 từ dài hơn cả limit (ví dụ chuỗi mã hóa) -> Cắt cứng
        if split_index == -1:
            split_index = limit

        # Cắt đoạn văn ra
        chunk = current_text[:split_index]
        chunks.append(chunk)

        # Cập nhật phần văn bản còn lại (bỏ qua ký tự phân cách và khoảng trắng thừa)
        current_text = current_text[split_index:].strip()

    # Thêm phần còn lại cuối cùng
    if current_text:
        chunks.append(current_text)

    return chunks

def send_discord_alert(title, description, fields=None, color=None):
    """
    Gửi tin nhắn Discord với thuật toán cắt chữ thông minh.
    """
    if not DISCORD_WEBHOOK_URL:
        print("❌ Lỗi: Không tìm thấy DISCORD_WEBHOOK_URL")
        return

    # Sử dụng hàm cắt thông minh
    chunks = split_text_smart(description, limit=1900)
    total_parts = len(chunks)

    print(f"   ✂️ Nội dung dài, đã chia thành {total_parts} phần liền mạch.")

    for i, chunk_text in enumerate(chunks):
        # Tạo tiêu đề
        if total_parts > 1:
            if i == 0:
                # Tin đầu tiên: Tiêu đề to + (Phần 1/x)
                msg_content = f"**{title} (Phần {i+1}/{total_parts})**\n\n{chunk_text}"
            else:
                # Các tin sau: Chỉ để (Phần x/x) nhỏ hoặc không cần tiêu đề để đọc liền mạch
                msg_content = f"*(Tiếp theo - Phần {i+1}/{total_parts})*\n{chunk_text}"
        else:
            msg_content = f"**{title}**\n\n{chunk_text}"

        data = {
            "content": msg_content
        }

        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data)
            if response.status_code not in [200, 204]:
                print(f"❌ Lỗi gửi phần {i+1}: {response.text}")
            
        except Exception as e:
            print(f"❌ Exception: {e}")