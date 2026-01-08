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

def get_taiwan_stock_pool():
    """獲取台股池 - 使用多重備用方案"""
    print("🔍 正在獲取台股清單...")

    # 方案 1: 嘗試從 MoneyDJ 獲取 0050 成分股
    try:
        print("   嘗試從 MoneyDJ 獲取 0050 成分股...")
        url_0050 = "https://www.moneydj.com/ETF/X/Basic/Basic0007.xdjhtm?etfid=0050.TW"
        tables = pd.read_html(url_0050, encoding='utf-8')
        # 找到包含股票代號的表格
        for table in tables:
            if '代號' in str(table.columns) or '股票代號' in str(table.columns):
                df_0050 = table
                break
        else:
            df_0050 = tables[0]  # 如果找不到，使用第一個表格

        # 提取股票代號
        code_column = None
        for col in df_0050.columns:
            if '代號' in str(col) or 'code' in str(col).lower():
                code_column = col
                break

        if code_column is not None:
            codes_0050 = df_0050[code_column].dropna().astype(str).tolist()
            print(f"   ✅ 從 MoneyDJ 獲取到 {len(codes_0050)} 支 0050 成分股")
        else:
            raise Exception("找不到股票代號欄位")

    except Exception as e:
        print(f"   ❌ MoneyDJ 方案失敗: {e}")
        codes_0050 = []

    # 方案 2: 嘗試從 Yahoo Finance 獲取台股資訊
    try:
        print("   嘗試從 Yahoo Finance 獲取熱門台股...")
        # 台股市值前 50 大熱門股票（手動維護清單，較穩定）
        popular_tw_stocks = [
            "2330", "2317", "2454", "2882", "6505", "2412", "2303", "3711", "2881", "2892",
            "2891", "2002", "1303", "2408", "2886", "2395", "3008", "2409", "2002", "2912",
            "2885", "2357", "2474", "2801", "2880", "2883", "2887", "3045", "2301", "2308",
            "2382", "2888", "2890", "6669", "2327", "2379", "2324", "2344", "2201", "2207",
            "3231", "1216", "6415", "6239", "2609", "1101", "1102", "2105", "2498", "8046"
        ]
        codes_yahoo = popular_tw_stocks
        print(f"   ✅ 使用熱門台股清單 {len(codes_yahoo)} 支")
    except Exception as e:
        print(f"   ❌ Yahoo Finance 方案失敗: {e}")
        codes_yahoo = []

    # 方案 3: 備用的基本台股清單（ETF 成分股近似）
    backup_stocks = [
        "2330", "2317", "2454", "2882", "6505", "2412", "2303", "3711", "2881", "2892",
        "2891", "2002", "1303", "2408", "2886", "2395", "3008", "2409", "2912", "2885",
        "2357", "2474", "2801", "2880", "2883", "2887", "3045", "2301", "2308", "2382",
        "2888", "2890", "6669", "2327", "2379", "2324", "2344", "2201", "2207", "3231",
        "1216", "6415", "6239", "2609", "1101", "1102", "2105", "2498", "8046", "2823",
        "2207", "2615", "6446", "3034", "2618", "2610", "1301", "2002", "2049", "2020"
    ]

    # 合併所有獲取的股票代號
    all_codes = []
    if codes_0050:
        # 清理 0050 代碼格式
        clean_codes_0050 = [str(code).strip().replace('.TW', '') for code in codes_0050 if str(code).strip().isdigit()]
        all_codes.extend(clean_codes_0050)

    if codes_yahoo:
        all_codes.extend(codes_yahoo)

    # 如果前面的方案都失敗，使用備用清單
    if not all_codes:
        print("   ⚠️  使用備用台股清單")
        all_codes = backup_stocks

    # 去重並格式化
    unique_codes = list(set(all_codes))
    ticker_pool = [f"{code}.TW" for code in unique_codes if code.isdigit()]

    print(f"   📊 最終股票池: {len(ticker_pool)} 支標的")
    print(f"   範例: {ticker_pool[:5]}")

    return ticker_pool

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

        # --- Spec 4: 獲取台股池並過濾 (使用多重備用方案) ---
        ticker_pool = get_taiwan_stock_pool()

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

    請執行以下任務並按照指定格式輸出：

    🌅 投資早報 - [今日日期]

    📈 美股收盤摘要
    {market_data}

    📰 1. 美股新聞重點
    摘要今日美股 3 個關鍵新聞，每則新聞用「●」開頭，一行一則。

    📰 2. 台股新聞重點
    摘要今日台股 3 個重要產業新聞，每則新聞用「●」開頭，一行一則。

    🎯 3. 精選潛力股 (5支)
    從候選清單中精選 5 支股票，格式如下：
    ● [股票代號] [公司名稱]
    理由：[結合新聞的推薦理由，限50字內]

    ⚠️ 投資提醒
    本報告僅供參考，投資有風險請謹慎評估。

    注意事項：
    - 不要使用任何 Markdown 語法 (如 **、##、[]() 等)
    - 使用 Emoji 和數字編號來美化排版
    - 每個段落間空一行提升可讀性
    - 內容簡潔適合手機 LINE 閱讀
    - 使用繁體中文
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
                return f"""🌅 投資早報 - 今日摘要

📊 市場數據
{market_data}

🎯 潛力股候選
{qualified_stocks}

⚠️ 系統提醒
AI 新聞分析功能暫時無法使用，僅提供基本市場數據。

📱 完整分析將在系統恢復後提供。"""
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
