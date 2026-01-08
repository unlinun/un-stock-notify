#!/usr/bin/env python3
"""
模擬完整程式運行（不使用 Gemini API）
測試除了 AI 生成以外的所有功能
"""

import os
import time
import pandas as pd
import yfinance as yf

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

        # --- 由於 Wikipedia 暫時無法訪問，我們用備用方案 ---
        print("🔍 使用備用股票清單進行篩選...")

        # 熱門台股測試清單
        test_pool = [
            "2330.TW", "2317.TW", "2454.TW", "2882.TW", "6505.TW",
            "2412.TW", "2303.TW", "3711.TW", "2881.TW", "2892.TW",
            "2891.TW", "2395.TW", "2409.TW", "3008.TW", "2002.TW"
        ]

        # 批次下載數據加速篩選
        print(f"🔍 正在過濾 {len(test_pool)} 支標的...")
        data = yf.download(test_pool, period="5d", group_by='ticker', progress=False)

        qualified_stocks = []
        for ticker in test_pool:
            try:
                hist = data[ticker] if len(test_pool) > 1 else data
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

def generate_mock_report(market_data, qualified_stocks):
    """生成模擬報告（不使用 AI）"""
    print("🤖 生成模擬投資報告...")

    current_time = time.strftime("%Y-%m-%d %H:%M")

    mock_report = f"""🌅 投資早報 - {current_time}

{market_data}

【台股潛力股精選】
🎯 符合條件的潛力股票：
{qualified_stocks}

【模擬分析重點】
📈 美股表現：各大指數呈現穩定走勢
💹 台股機會：已篩選出價格合理且流動性佳的標的
⚠️  投資提醒：本報告僅供參考，請謹慎投資

🤖 本次為測試模式，未使用 AI 生成新聞分析
實際使用時會包含最新市場新聞與專業分析
"""

    return mock_report

def send_mock_message(message):
    """模擬發送 Discord 訊息"""
    print("💬 模擬發送 Discord 訊息...")
    print("=" * 50)
    print("訊息內容預覽：")
    print(message)
    print("=" * 50)
    print("✅ 模擬發送成功（實際使用時需要設定 DISCORD_WEBHOOK_URL）")
    return True

def main():
    """主程式"""
    print("🚀 啟動測試模式早報機器人...")
    print("本次測試不使用 Gemini API 與 Discord Webhook")
    print("=" * 60)

    try:
        # 1. 獲取市場數據
        market_data, qualified_stocks = get_market_data()

        if not market_data or market_data == "無法獲取市場數據":
            print("❌ 市場數據獲取失敗")
            return

        print("✅ 市場數據獲取成功")

        # 2. 生成報告
        report = generate_mock_report(market_data, qualified_stocks)

        if not report:
            print("❌ 報告生成失敗")
            return

        print("✅ 報告生成成功")

        # 3. 模擬發送
        success = send_mock_message(report)

        if success:
            print("\n🎉 測試完成！所有核心功能運作正常")
            print("\n📋 待設定項目：")
            print("   • GEMINI_API_KEY - 用於 AI 生成新聞分析")
            print("   • DISCORD_WEBHOOK_URL - 用於發送 Discord 訊息")
            print("\n💡 設定完成後即可正式使用！")
        else:
            print("❌ 模擬發送失敗")

    except Exception as e:
        print(f"❌ 執行異常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
