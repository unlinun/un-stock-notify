# 股票機器人 📈

智慧型股票市場分析和報告生成機器人，結合 AI 技術提供即時市場洞察。

## ✨ 功能特色

### 📊 市場數據分析
- **美股指數監控**：即時追蹤道瓊、標普500等主要指數
- **台股智慧篩選**：基於技術指標自動篩選優質標的
- **多重資料來源**：Yahoo Finance + Wikipedia 備援機制
- **歷史數據分析**：5日均線、成交量等技術指標

### 🤖 AI 智慧分析
- **Gemini AI 整合**：利用 Google Gemini 2.0 進行深度分析
- **市場趨勢解讀**：AI 自動解讀市場數據並產生洞察
- **個股評估**：結合基本面和技術面進行綜合評估

### 📱 多平台即時推播
- **LINE Bot 整合**：自動推送市場分析報告到 LINE
- **Discord Webhook**：支援 Discord 頻道通知
- **即時通知**：重要市場變化即時提醒
- **個人化服務**：根據使用者偏好客製化內容

## 🗂️ 檔案說明

- `stock_bot.py` - 主要機器人程式，包含所有核心功能
- `test_bot.py` - 簡化測試檔案，驗證核心功能正常運作
- `simple_test.py` - 基本功能測試，逐步檢查各模組
- `requirements.txt` - 專案相依套件列表

## 🛠️ 安裝指南

### 1. 環境需求
- Python 3.8 或更新版本
- 穩定的網路連線

### 2. 套件安裝
```bash
# 安裝相依套件
pip install -r requirements.txt
```

### 3. 環境變數設定
在系統中設定以下環境變數：

```bash
# 必要設定
export GEMINI_API_KEY="你的_Gemini_API_金鑰"

# 通知管道設定（至少選擇一個）
export LINE_ACCESS_TOKEN="你的_LINE_Bot_存取權杖"
export LINE_USER_ID="你的_LINE_使用者_ID"
export DISCORD_WEBHOOK_URL="你的_Discord_Webhook_網址"
```

**取得 API 金鑰方法：**
- **Gemini API**：前往 [Google AI Studio](https://aistudio.google.com/) 申請
- **LINE Bot**：在 [LINE Developers](https://developers.line.biz/) 建立應用程式
- **Discord Webhook**：在 Discord 伺服器設定中建立 Webhook

## 🧪 測試執行

```bash
# 執行完整功能測試
python test_bot.py

# 執行基本連線測試
python simple_test.py
```

**測試項目包含：**
- ✅ 環境變數檢查
- ✅ 資料來源連線測試
- ✅ 台股池獲取功能
- ✅ 市場數據處理能力
- ✅ Gemini AI 連線狀態
- ✅ Discord Webhook 連線

## 🚀 執行機器人

```bash
# 啟動股票機器人
python stock_bot.py
```

## 📋 使用流程

1. **環境檢查**：程式會自動檢查環境變數設定
2. **數據獲取**：從多個來源收集最新市場數據
3. **智慧分析**：使用 AI 分析市場趨勢和個股表現
4. **報告生成**：產生結構化的分析報告
5. **多平台推送**：透過 LINE 和/或 Discord 發送分析結果

## 🔧 設定說明

### 通知管道設定
- **LINE Bot**：適合個人使用，推送到手機
- **Discord Webhook**：適合團隊使用，推送到群組頻道
- **雙重推播**：可同時設定兩個管道確保不漏接

### 股票池設定
- 預設包含台股熱門標的 50 支
- 支援自動篩選符合條件的股票
- 可依據成交量、價格變化等條件調整

### AI 分析參數
- 使用 Gemini 2.0 Flash 模型
- 支援繁體中文分析報告
- 可自訂分析深度和報告格式

## ⚠️ 注意事項

- **API 限制**：請注意 Gemini API 的使用配額
- **資料延遲**：股票數據可能有 15-20 分鐘延遲
- **網路需求**：需要穩定網路連線以確保數據即時性
- **隱私保護**：環境變數請妥善保管，避免洩露
- **Discord 限制**：單一訊息最大 2000 字元，程式會自動分段

## 🐛 常見問題

**Q: 測試失敗怎麼辦？**
A: 檢查環境變數設定、網路連線狀態，並確認 API 金鑰有效性

**Q: 無法獲取台股數據？**
A: 程式有多重備援機制，如持續失敗請檢查防火牆設定

**Q: LINE 推送失敗？**
A: 確認 LINE Bot 設定正確，並檢查 User ID 是否正確

**Q: Discord 推送失敗？**
A: 檢查 Webhook URL 是否正確，並確認頻道權限設定

## 📈 技術架構

- **資料獲取**：yfinance + pandas
- **AI 分析**：Google Gemini 2.0
- **通訊推播**：LINE Messaging API + Discord Webhooks
- **HTTP 請求**：requests
- **錯誤處理**：多重備援機制
- **資料處理**：即時篩選與分析算法
