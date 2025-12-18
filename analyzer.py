import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# --- CẤU HÌNH ---
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_market_data(news_list, onchain_data):
    """
    Phân tích Tin tức Công nghệ & Xu hướng giá đa khung thời gian
    """
    print("🧠 Gemini đang phân tích Nến & Công nghệ...")

    if not GEMINI_API_KEY:
        return "Lỗi: Thiếu API Key"

    # 1. Chuẩn bị dữ liệu Tin tức (Kèm tóm tắt để AI hiểu sâu hơn)
    news_text = ""
    if news_list:
        # Lọc bớt tin trùng lặp nếu có
        seen_titles = set()
        unique_news = []
        for n in news_list:
            if n['title'] not in seen_titles:
                unique_news.append(n)
                seen_titles.add(n['title'])
        
        news_text = "\n\n".join([f"Tiêu đề: {n['title']}\nTóm tắt: {n['summary']}\nLink: {n['link']}" for n in unique_news])
    
    # 2. Chuẩn bị dữ liệu Market (Đa khung thời gian)
    market = onchain_data.get('market', {})
    
    def fmt(val): # Hàm format màu sắc cho số
        return f"+{val:.2f}%" if val > 0 else f"{val:.2f}%"

    btc = market.get('bitcoin', {})
    eth = market.get('ethereum', {})
    
    market_text = f"""
    [BITCOIN - BTC]
    - Giá hiện tại: ${btc.get('price', 0):,.2f}
    - Xu hướng 1 Giờ (Nến H1): {fmt(btc.get('change_1h', 0))}
    - Xu hướng 24 Giờ (Nến D1): {fmt(btc.get('change_24h', 0))}
    - Xu hướng 7 Ngày (Nến W1): {fmt(btc.get('change_7d', 0))}

    [ETHEREUM - ETH]
    - Giá hiện tại: ${eth.get('price', 0):,.2f}
    - Xu hướng 1 Giờ: {fmt(eth.get('change_1h', 0))}
    - Xu hướng 24 Giờ: {fmt(eth.get('change_24h', 0))}
    - Xu hướng 7 Ngày: {fmt(eth.get('change_7d', 0))}
    - Gas Price: {onchain_data.get('safe_gas_gwei')} Wei (Số lớn > 50 gwei là đắt)
    """

    # 3. PROMPT "CHUYÊN GIA" (V3.0)
    prompt = f"""
    Bạn là Chuyên gia Phân tích Thị trường Crypto & Công nghệ Blockchain (Senior Analyst).
    Hãy viết báo cáo thị trường Tiếng Việt dựa trên dữ liệu sau:

    === DỮ LIỆU ĐẦU VÀO ===
    
    A. THÔNG SỐ KỸ THUẬT (Price Action):
    {market_text}

    B. TIN TỨC MỚI NHẤT:
    {news_text}

    === YÊU CẦU BÁO CÁO (Bắt buộc theo 2 phần sau) ===

    PHẦN 1: 📰 ĐIỂM TIN & CÔNG NGHỆ
    - Bình luận chi tiết & sâu sắc (insights) về tất cả các tin tức thu thập được.
    - ĐẶC BIỆT: Nếu có tin về **Công nghệ mới** (Update, Fork, Protocol, AI...), hãy giải thích cơ chế hoạt động của nó một cách chi tiết nhưng dễ hiểu cho người mới (giải thích "nó là gì" và "tại sao nó quan trọng").
    - Nhận xét tác động của tin tức đến tâm lý chung.

    PHẦN 2: 📈 PHÂN TÍCH THỊ TRƯỜNG & VĨ MÔ
    - **BTC & ETH:** Đưa ra giá hiện tại.
    - **Phân tích Xu hướng (Dựa trên dữ liệu % 1H, 24H, 7D ở trên):**
      + *Ngắn hạn (Short-term):* Dựa vào biến động 1H và 24H. Phe Mua hay Phe Bán đang kiểm soát?
      + *Dài hạn (Long-term):* Dựa vào biến động 7D và tình hình Kinh tế Vĩ mô (lạm phát, FED, dòng tiền...) mà bạn biết.
    - **Nhận định:** Bullish (Tăng) 🐂 hay Bearish (Giảm) 🐻? Vùng giá cần chú ý?

    Văn phong: Chuyên nghiệp, sâu sắc, khách quan. Dùng Markdown.

    ---
    ### PHẦN 3: 🎬 KỊCH BẢN VIDEO NGẮN (TikTok/Reels - Dưới 60s)
    *Yêu cầu: Giọng văn dồn dập, gây tò mò (Hook), phù hợp giới trẻ.*

    **Tiêu đề Video:** (Viết 1 tiêu đề giật tít)

    | Thời gian | Hình ảnh/Mô tả (Visual) | Lời thoại (Audio) |
    | :--- | :--- | :--- |
    | **00-03s** | (Mô tả cảnh mở đầu gây sốc hoặc biểu đồ đỏ/xanh lòe loẹt) | (Câu Hook cực mạnh về giá hoặc tin tức nóng nhất) |
    | **03-15s** | (Show chart hoặc hình ảnh minh họa tin tức) | (Giải thích ngắn gọn chuyện gì đang xảy ra. Ví dụ: "BTC vừa sập vì...", "Công nghệ mới này sẽ...") |
    | **15-45s** | (Cảnh chuyên gia phân tích hoặc meme hài hước) | (Phân tích tác động: Tốt hay xấu? Cơ hội là gì? Giải thích thuật ngữ khó bằng ngôn ngữ đời thường) |
    | **45-60s** | (Mặt người nói hoặc Logo kênh) | (Kêu gọi hành động: "Follow ngay để không lỡ kèo", "Ý kiến bạn thế nào? Comment nhé") |

    ---
    Lưu ý: Chỉ xuất ra nội dung, không rườm rà.
    """

    try:
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:

        return f"Lỗi phân tích AI: {e}"


