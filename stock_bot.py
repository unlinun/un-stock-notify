import os
import time
import pandas as pd
import yfinance as yf
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 1. 從環境變數讀取金鑰
LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

def get_market_data():
    """獲取指數數據與台股潛力篩選名單"""
    print("📊 正在收集市場數據...")
    try:
        # --- Spec 1: 美股指數與 VOO ---
        indices = {"^DJI": "道瓊", "^GSPC": "標普500", "VOO": "VOO"}
        market_summary = "【美股收盤與 VOO】\n"
        for symbol, name in indices.items():
            tk = yf.Ticker(symbol)
            # 抓取 5 天數據以確保能計算最新一天的漲跌幅（考慮週末）
            hist = tk.history(period="5d")
            if len(hist) < 2: continue
            
            last_close = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            change_pct = ((last_close - prev_close) / prev_close) * 100
            market_summary += f"● {name}: {last_close:.2f} ({change_pct:+.2f}%)\n"

        # --- Spec 4: 獲取台股 150 強並過濾 ---
        # 抓取 0050 與 0051 成分股
        df_50 = pd.read_html("https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A350%E6%8C%87%E6%95%B8")[2]
        df_51 = pd.read_html("https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A3%E4%B8%AD%E5%9E%8B100%E6%8C%87%E6%95%B8")[1]
        raw_pool = pd.concat([df_50['股票代號'], df_51['股票代號']]).unique()
        ticker_pool = [f"{str(code).strip()}.TW" for code in raw_pool]

        # 批次下載數據加速篩選
        print(f"🔍 正在過濾 {len(ticker_pool)} 支標的...")
        data = yf.download(ticker_pool, period="5d", group_by='ticker', progress=False)
        
        qualified_stocks = []
        for ticker in ticker_pool:
            try:
                hist = data[ticker]
                price = hist['Close'].iloc[-1]
                avg_vol = hist['Volume'].mean() # 5日均量
                # 篩選：價格 20-50 元，且日均量 > 3000 張
                if 20 <= price <= 50 and avg_vol > 3000000:
                    qualified_stocks.append(f"{ticker}(價:{price:.1f},量:{int(avg_vol/1000)}K)")
            except: continue
        
        qualified_str = ", ".join(qualified_stocks[:15]) # 限制長度避免 Prompt 過載
        return market_summary, qualified_str
    
    except Exception as e:
        print(f"數據獲取錯誤: {e}")
        return "無法獲取市場數據", ""

def generate_report_with_retry(client, market_data, qualified_stocks, max_retries=3):
    """使用重試機制生成報告 (整合新聞與選股邏輯)"""
    prompt = f"""
    請以專業分析師身份，根據以下數據並使用 Google Search 撰寫投資早報：

    1. 今日市場數據：
    {market_data}

    2. 台股潛力候選清單 (20-50元 & 高流動性)：
    {qualified_stocks}

    請執行以下任務：
    - [美股新聞重點]：摘要今日美股 3 個關鍵新聞。
    - [台股新聞重點]：摘要今日台股 3 個重要產業新聞。
    - [5 支潛力股精選]：從「候選清單」中，結合搜尋到的新聞（利多、財報、題材），精選 5 支並提供推薦理由。

    請使用繁體中文、Emoji 排版，內容簡潔適合手機閱讀。
    """

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.7
                )
            )
            return response.text
        except ServerError:
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 5)
            else:
                return f"📊 市場數據摘要\n\n{market_data}\n\n⚠️ AI 暫時無法分析新聞。"
        except Exception as e:
            return f"❌ 生成報告錯誤: {str(e)}"
    return None

def send_line_message(message):
    """發送 LINE 訊息 (保留原本的分割邏輯)"""
    if not LINE_ACCESS_TOKEN or not LINE_USER_ID:
        print("🚫 缺少金鑰，輸出內容：\n", message)
        return False
    try:
        line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
        max_length = 4500
        for i in range(0, len(message), max_length):
            line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text=message[i:i+max_length]))
            time.sleep(1)
        return True
    except Exception as e:
        print(f"❌ LINE 發送失敗: {e}")
        return False

def main():
    print("🚀 啟動早報機器人...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        market_data, qualified_stocks = get_market_data()
        report = generate_report_with_retry(client, market_data, qualified_stocks)
        if report:
            send_line_message(report)
        print("🎉 任務完成!")
    except Exception as e:
        print(f"❌ 執行異常: {e}")

if __name__ == "__main__":
    main()
