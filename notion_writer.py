import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# --- CẤU HÌNH ---
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path, override=True)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def create_notion_page(title, content_text):
    """
    Tạo một trang mới trong Notion Database với nội dung báo cáo
    """
    if not NOTION_TOKEN or not DATABASE_ID:
        print("❌ Lỗi: Thiếu cấu hình Notion trong file .env")
        return

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28" # Version ổn định
    }

    # Xử lý nội dung: Notion API yêu cầu body là các "Block".
    # Chúng ta sẽ chia báo cáo thành các đoạn văn (Paragraphs) dựa trên xuống dòng.
    children_blocks = []
    
    # Chia nhỏ văn bản để không bị lỗi giới hạn ký tự (2000 char/block)
    lines = content_text.split('\n')
    for line in lines:
        if line.strip(): # Bỏ qua dòng trống
            # Cắt ngắn nếu dòng quá dài (Notion limit)
            safe_content = line[:2000] 
            children_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": safe_content}
                        }
                    ]
                }
            })

    # Cấu trúc Payload gửi đi
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            # "Name" là tên mặc định của cột Title trong Notion
            # Nếu bác đổi tên cột này trong Notion thì phải đổi chữ "Name" ở dưới
            "Name": {
                "title": [
                    {"text": {"content": title}}
                ]
            },
            # Cột Date (Nếu bác đã tạo cột tên "Date" trong Notion)
            # Nếu chưa tạo thì comment dòng dưới lại để tránh lỗi
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            }
        },
        # Nội dung trang
        "children": children_blocks
    }

    try:
        response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
        
        if response.status_code == 200:
            print(f"✅ Đã ghi vào Notion thành công: {title}")
        else:
            print(f"❌ Lỗi Notion ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"❌ Exception Notion: {e}")

# --- TEST ĐỘC LẬP ---
if __name__ == "__main__":
    print("📝 Đang test ghi vào Notion...")
    create_notion_page(
        title="Test Report from Python",
        content_text="Dòng 1: Hello World\nDòng 2: Đây là bot tự động.\nDòng 3: Kết thúc."
    )