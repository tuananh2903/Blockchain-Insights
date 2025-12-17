🤖 Crypto Market & Content Automation Bot
Automated Blockchain Analysis, Content Generation, and Multi-Platform Publishing Workflow.

📖 Overview
This project is a Python-based automation tool designed to streamline the workflow of crypto content creators and analysts. It automatically fetches real-time market data and news, uses AI to generate comprehensive insights and video scripts, and distributes the content to Discord (for team alerts) and Notion (for content archiving).

✨ Key Features
⚡ Automated Data Collection: Fetches the latest crypto market news and price data (e.g., Bitcoin) via data_loader.

🧠 AI-Powered Analysis: Uses an LLM (Large Language Model, specifically configured for Gemini) to analyze data and generate a structured "Market Report" and a "Video Filming Script".

✂️ Smart Content Splitting: Automatically separates the Market Insight from the Video Script using specific delimiters (### PHẦN 3).

📢 Discord Integration: Sends a concise Market Insight alert to a Discord channel via Webhooks.

📝 Notion Archiving: Saves the full content (Report + Script) into a specific Notion database for content management.

🛡️ Error Handling: Robust try/catch blocks to ensure the pipeline reports errors without crashing silently.

🔄 How It Works
The job() function executes the following pipeline:

Ingest: Aggregates Market News + Crypto Market Data.

Generate: AI analyzes the data and writes a long-form document containing:

Part 1 & 2: Market Analysis & Key Trends.

Part 3: A ready-to-use Video Script.

Process: The bot detects the marker ### PHẦN 3.

For Discord: It cuts off the script to keep the alert concise.

For Notion: It keeps the full text.

Publish:

Discord: Sends the "Market Insight" summary.

Notion: Creates a new page titled 🎬 Script & Market Report - DD/MM/YYYY.

🛠️ Project Structure
Plaintext

├── main.py             # Entry point (contains the job() function)
├── data_loader.py      # Module to fetch news and crypto prices
├── analyzer.py         # Module interacting with AI (Gemini) to generate text
├── bot.py              # Module handling Discord Webhook interactions
├── notion_writer.py    # Module handling Notion API interactions
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (API Keys)
🚀 Installation & Setup
1. Clone the repository
Bash

git clone https://github.com/yourusername/crypto-auto-bot.git
cd crypto-auto-bot
2. Install Dependencies
Ensure you have Python 3.8+ installed.

Bash

pip install -r requirements.txt
3. Environment Configuration
Create a .env file in the root directory and add your API keys:

Ini, TOML

# AI / LLM
GEMINI_API_KEY=your_gemini_api_key

# Discord
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# Notion
NOTION_TOKEN=your_integration_token
NOTION_DATABASE_ID=your_database_id

# Market Data (If required by data_loader)
COINGECKO_API_KEY=optional_key
NEWS_API_KEY=optional_key
🏃 Usage
You can run the bot manually or set it up as a Cron job (Linux) or Task Scheduler (Windows).

Manual Run:

Bash

python main.py
Expected Console Output:

Plaintext

🚀 --- BẮT ĐẦU: QUY TRÌNH TÁCH RIÊNG CONTENT (2023-10-27 08:00:00) ---
📥 Bước 1: Lấy dữ liệu Market & News...
   ✅ Data OK: BTC $67,500
   ✅ Đã tạo xong nội dung.
   ✂️ Đã tách bỏ phần Kịch bản khỏi nội dung Discord.
📢 Bước 3: Gửi Discord (Bản rút gọn)...
📝 Bước 4: Lưu Full nội dung vào Notion...
🏁 --- DONE ---
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
