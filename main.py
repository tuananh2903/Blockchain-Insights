import time
from datetime import datetime
import data_loader
import analyzer
import bot
import notion_writer

def job():
    print(f"\n🚀 --- BẮT ĐẦU: QUY TRÌNH TÁCH RIÊNG CONTENT ({datetime.now()}) ---")

    # 1. LẤY DỮ LIỆU
    print("📥 Bước 1: Lấy dữ liệu Market & News...")
    try:
        news_list = data_loader.get_market_news()
        market_data = data_loader.get_crypto_market_data()
        
        if market_data is None:
            print("🛑 Dừng: Không có dữ liệu.")
            return

        btc_price = market_data['market']['bitcoin']['price']
        print(f"   ✅ Data OK: BTC ${btc_price:,.0f}")
        
    except Exception as e:
        print(f"   ❌ Lỗi Bước 1: {e}")
        return

    # 2. AI LÀM VIỆC (Viết Full Báo cáo + Kịch bản)

    # ... (Code trên giữ nguyên)
    try:
        full_content = analyzer.analyze_market_data(news_list, market_data)
        
        # --- SỬA ĐOẠN NÀY ---
        if "Lỗi" in full_content:
            # In nguyên văn cái lỗi ra để biết đường sửa
            print(f"   ⚠️ CHI TIẾT LỖI TỪ GEMINI: {full_content}") 
            return
        # --------------------
            
        print("   ✅ Đã tạo xong nội dung.")
    except Exception as e:
    # ...
            
        print("   ✅ Đã tạo xong nội dung.")
    except Exception as e:
        print(f"   ❌ Lỗi Bước 2: {e}")
        return

    # --- XỬ LÝ TÁCH NỘI DUNG ---
    # Tìm từ khóa "### PHẦN 3" để cắt
    split_marker = "### PHẦN 3"
    
    if split_marker in full_content:
        # Tách làm đôi: [0] là Báo cáo, [1] là Kịch bản
        parts = full_content.split(split_marker)
        
        # Nội dung cho Discord: Chỉ lấy phần đầu (Bỏ kịch bản)
        discord_content = parts[0].strip()
        # Thêm một dòng footer nhỏ để biết kịch bản ở đâu
        discord_content += "\n\n*(Xem Kịch bản quay Video chi tiết trên Notion)*"
        
        print("   ✂️ Đã tách bỏ phần Kịch bản khỏi nội dung Discord.")
    else:
        # Nếu AI lỡ không viết đúng format, gửi nguyên văn
        discord_content = full_content

    # Tiêu đề báo cáo
    today_str = datetime.now().strftime("%d/%m/%Y")
    report_title = f"🎬 Script & Market Report - {today_str}"

    # 3. GỬI DISCORD (Chỉ nhận Báo cáo thị trường)
    print("📢 Bước 3: Gửi Discord (Bản rút gọn)...")
    try:
        bot.send_discord_alert(
            title=f"🔥 Market Insight - {today_str}",
            description=discord_content, # Chỉ gửi Phần 1 & 2
            color=None
        )
    except Exception as e:
        print(f"   ❌ Lỗi Discord: {e}")

    # 4. GHI NOTION (Lưu Full: Báo cáo + Kịch bản)
    print("📝 Bước 4: Lưu Full nội dung vào Notion...")
    try:
        notion_writer.create_notion_page(
            title=report_title,
            content_text=full_content # Gửi Full bao gồm cả kịch bản
        )
    except Exception as e:
        print(f"   ❌ Lỗi Notion: {e}")

    print("🏁 --- DONE ---")

if __name__ == "__main__":

    job()
