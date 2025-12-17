import feedparser
import requests
import time

def get_market_news():
    """
    Lấy tin tức từ CoinTelegraph (Market + Tech)
    """
    urls = [
        "https://cointelegraph.com/rss/category/market-analysis",
        "https://cointelegraph.com/rss/tag/blockchain"
    ]
    
    news_list = []
    print(f"📡 Đang quét tin tức thị trường & công nghệ...")

    # Giả lập trình duyệt để tránh bị chặn RSS
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in urls:
        try:
            # Dùng requests để tải RSS trước (tránh lỗi 403 Forbidden)
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    for entry in feed.entries[:2]:
                        news_list.append({
                            "title": entry.title,
                            "link": entry.link,
                            "summary": entry.summary[:250] if hasattr(entry, 'summary') else "",
                            "published": entry.published if hasattr(entry, 'published') else "Mới cập nhật"
                        })
        except Exception as e:
            print(f"⚠️ Lỗi đọc RSS {url}: {e}")
            continue
    
    return news_list

def get_crypto_market_data():
    """
    Lấy dữ liệu giá chi tiết (1h, 24h, 7d) từ Endpoint /coins/markets (Chính xác hơn)
    """
    print("📊 Đang lấy dữ liệu biến động (1H - 24H - 7D)...")
    
    # URL MỚI: Dùng endpoint /coins/markets để lấy full data
    market_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "1h,24h,7d" # Yêu cầu trả về đủ 3 khung giờ
    }
    
    gas_url = "https://beaconcha.in/api/v1/execution/gasnow"

    try:
        # 1. CALL API MARKET (CoinGecko)
        # Thêm header User-Agent để tránh bị CoinGecko chặn request từ Python
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        market_res = requests.get(market_url, params=params, headers=headers, timeout=10)
        market_data = {}
        
        if market_res.status_code == 200:
            data_list = market_res.json()
            
            for coin in data_list:
                # API trả về list, ta chuyển thành dict theo id để dễ truy xuất
                # Key trả về của endpoint này khác với /simple/price, cần map đúng
                coin_id = coin['id'] # 'bitcoin' hoặc 'ethereum'
                
                market_data[coin_id] = {
                    'price': coin.get('current_price', 0),
                    # Lưu ý: Key của endpoint này là 'price_change_percentage_Xh_in_currency'
                    'change_1h': coin.get('price_change_percentage_1h_in_currency', 0),
                    'change_24h': coin.get('price_change_percentage_24h_in_currency', 0),
                    'change_7d': coin.get('price_change_percentage_7d_in_currency', 0)
                }
        else:
            print(f"⚠️ Lỗi CoinGecko: {market_res.status_code}")
            return None

        # 2. CALL API GAS
        gas_res = requests.get(gas_url, timeout=10)
        standard_gas = "N/A"
        if gas_res.status_code == 200:
            data = gas_res.json().get('data', {})
            standard_gas = data.get('standard', 'N/A')

        # Kiểm tra xem có lấy được đủ data không
        if 'bitcoin' not in market_data:
            print("❌ Không tìm thấy dữ liệu Bitcoin.")
            return None

        return {
            "market": market_data,
            "safe_gas_gwei": standard_gas,
            "source": "CoinGecko Markets API"
        }

    except Exception as e:
        print(f"❌ Lỗi lấy dữ liệu market: {e}")
        return None

# --- TEST ---
if __name__ == "__main__":
    data = get_crypto_market_data()
    if data:
        btc = data['market']['bitcoin']
        print(f"BTC Price: ${btc['price']}")
        print(f"1H: {btc['change_1h']}%")   # Phải ra số khác 0
        print(f"24H: {btc['change_24h']}%")
        print(f"7D: {btc['change_7d']}%")