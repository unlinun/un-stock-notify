# 🤖 投資早報機器人 (Stock Bot)

一個自動化的台股與美股投資早報機器人，整合多重數據來源，使用 AI 分析並發送至 Discord 頻道。

## ✨ 主要功能

### 📊 市場數據收集
- **美股指數**：道瓊指數 (^DJI)、標普500 (^GSPC)、VOO ETF 的即時收盤數據
- **台股池獲取**：多重備用方案確保穩定性
  - 方案1：從 MoneyDJ 自動抓取 0050 ETF 成分股
  - 方案2：Yahoo Finance 台股熱門清單 (市值前50大)
  - 方案3：內建備用台股清單 (60支精選標的)

### 🎯 智能選股篩選
- **價格篩選**：20-50 元價位區間
- **流動性篩選**：日均成交量 > 3000 張
- **自動批次處理**：支援大量股票同步分析

### 🧠 AI 投資分析
- **Google Gemini 2.0 Flash**：最新 AI 模型驅動
- **即時新聞整合**：Google Search 工具自動搜尋美股與台股新聞
- **專業報告生成**：
  - 美股收盤摘要
  - 美股新聞重點 (3則)
  - 台股新聞重點 (3則)
  - 精選潛力股推薦 (5支)

### 📱 Discord 自動推送
- **Webhook 整合**：無需 Bot Token，設定簡單
- **智能分割**：自動處理超過 2000 字元的長訊息
- **Rate Limit 防護**：避免 Discord API 限制
- **自訂機器人身份**：專屬頭像與名稱

## 🚀 快速開始

### 環境需求
- Python 3.8+
- pip 套件管理器

### 1. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 2. 環境變數設定
在系統環境中設定以下變數：

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

**取得方式：**
- **Discord Webhook URL**：
  1. 進入 Discord 伺服器設定
  2. 整合 → Webhook → 建立 Webhook
  3. 複製 Webhook URL

- **Gemini API Key**：
  1. 前往 [Google AI Studio](https://aistudio.google.com/)
  2. 建立新的 API 金鑰
  3. 複製 API Key

### 3. 執行機器人
```bash
python stock_bot.py
```

## 📋 輸出範例

```
🌅 投資早報 - 2024年1月8日

📈 美股收盤摘要
● 道瓊: 33845.73 (+0.45%)
● 標普500: 4378.41 (+0.32%)
● VOO: 401.23 (+0.28%)

📰 1. 美股新聞重點
● 聯準會利率決議符合預期，市場反應平穩
● 科技股財報季開跑，投資人關注 AI 相關營收
● 能源股受油價上漲帶動，板塊表現亮眼

📰 2. 台股新聞重點
● 台積電先進製程訂單滿載，第一季展望樂觀
● 電子股受惠 AI 伺服器需求，PCB 族群走強
● 金融股受升息環境影響，銀行獲利能力提升

🎯 3. 精選潛力股 (5支)
● 2330 台積電
理由：AI 晶片需求強勁，先進製程技術領先全球

● 2454 聯發科
理由：5G 晶片市占率提升，車用晶片業務成長

● 6505 台塑化
理由：原油價格回升，石化產品價差擴大

● 2317 鴻海
理由：iPhone 新機拉貨，AI 伺服器代工業務成長

● 2412 中華電
理由：5G 基建完善，企業客戶數位轉型商機

⚠️ 投資提醒
本報告僅供參考，投資有風險請謹慎評估。
```

## ⚙️ 技術架構

### 核心函式說明

| 函式名稱 | 功能說明 |
|---------|---------|
| `get_taiwan_stock_pool()` | 多重來源獲取台股清單，確保資料穩定性 |
| `get_market_data()` | 收集美股指數與台股篩選資料 |
| `generate_report_with_retry()` | 使用 Gemini AI 生成投資報告，含重試機制 |
| `send_discord_message()` | Discord Webhook 訊息發送與分割處理 |
| `main()` | 主程式流程控制 |

### 相依套件
```
yfinance==0.2.18      # Yahoo Finance 股價資料
pandas==2.0.3         # 資料處理與分析  
lxml==4.9.3          # HTML 表格解析
google-genai==0.3.0   # Google Gemini AI
requests==2.31.0      # HTTP 請求處理
```

## 🛡️ 錯誤處理機制

### 資料來源備援
- **三層備用方案**：確保台股清單獲取的穩定性
- **例外捕獲**：每個資料源失敗時自動切換到下一個方案

### API 呼叫保護
- **重試機制**：Gemini API 失敗時自動重試 3 次
- **指數退避**：重試間隔逐漸增加 (5秒、10秒、15秒)
- **降級模式**：AI 服務異常時提供基本市場數據

### Discord 發送優化
- **訊息分割**：超過 2000 字元自動分批發送
- **Rate Limit**：批次發送間加入延遲防護
- **狀態回傳**：詳細的成功/失敗狀態記錄

## 🔧 自訂設定

### 股票篩選條件調整
```python
# 修改 get_market_data() 中的篩選條件
if 20 <= price <= 50 and avg_vol > 3000000:  # 價格 20-50 元，量能 > 3000張
```

### AI 提示詞客製化
```python
# 修改 generate_report_with_retry() 中的 prompt 變數
# 可調整報告格式、分析重點、推薦數量等
```

### Discord 機器人設定
```python
# 修改 send_discord_message() 中的 payload
"username": "投資早報機器人",
"avatar_url": "YOUR_CUSTOM_AVATAR_URL"
```

## 📝 注意事項

### API 使用限制
- **Gemini API**：免費版每分鐘 60 次請求
- **Yahoo Finance**：建議避免過於頻繁的大量查詢
- **Discord Webhook**：無特殊限制，但建議合理使用

### 資料準確性
- 股價資料來自 Yahoo Finance，可能有 15-20 分鐘延遲
- 新聞資料由 AI 即時搜尋，建議搭配其他資訊來源驗證
- 投資建議僅供參考，請勿作為唯一投資依據

### 時區考量
- 程式預設使用系統時區
- 美股交易時間：台灣時間 22:30-05:00 (夏令時間 21:30-04:00)
- 建議在美股收盤後執行以獲得最新數據

## 🤝 貢獻指南

歡迎提交 Issue 或 Pull Request 來改善此專案：
- 新增更多資料來源
- 優化 AI 分析邏輯
- 改善錯誤處理機制
- 增加更多輸出格式支援

## 📄 授權條款

MIT License - 詳見 [LICENSE](LICENSE) 檔案

## ⭐ 支援

如果此專案對您有幫助，歡迎給個 Star ⭐

---

**免責聲明**：本工具僅供學習與研究用途，所提供的投資資訊不構成投資建議。投資有風險，請謹慎評估並自負盈虧責任。
