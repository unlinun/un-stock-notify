#!/usr/bin/env python3
"""
測試版本 - 只測試資料獲取功能
不需要 API 金鑰，專注於驗證股票數據和網頁抓取功能
"""

import pandas as pd
import yfinance as yf
import traceback

def test_market_data():
    """測試獲取指數數據與台股潛力篩選名單"""
    print("🚀 開始測試股票數據獲取功能...")
    print("=" * 50)

    try:
        # --- 測試 1: 美股指數與 VOO ---
        print("\n📈 測試美股指數數據...")
        indices = {"^DJI": "道瓊", "^GSPC": "標普500", "VOO": "VOO"}
        market_summary = "【美股收盤與 VOO】\n"

        for symbol, name in indices.items():
            try:
                print(f"   正在獲取 {name} ({symbol}) 數據...")
                tk = yf.Ticker(symbol)
                hist = tk.history(period="5d")

                if len(hist) < 2:
                    print(f"   ❌ {name} 數據不足")
                    continue

                last_close = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                change_pct = ((last_close - prev_close) / prev_close) * 100

                result_line = f"● {name}: {last_close:.2f} ({change_pct:+.2f}%)\n"
                market_summary += result_line
                print(f"   ✅ {result_line.strip()}")

            except Exception as e:
                print(f"   ❌ {name} 獲取失敗: {e}")
                continue

        print(f"\n✅ 美股數據獲取完成!")
        print("完整市場摘要:")
        print(market_summary)

        # --- 測試 2: 台股成分股數據 ---
        print("\n🇹🇼 測試台股數據...")
        print("   正在從 Wikipedia 獲取 0050 成分股...")

        try:
            df_50 = pd.read_html("https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A350%E6%8C%87%E6%95%B8")[2]
            print(f"   ✅ 0050 成分股: {len(df_50)} 支")
            print(f"   前 5 支: {list(df_50['股票代號'].head())}")
        except Exception as e:
            print(f"   ❌ 0050 數據獲取失敗: {e}")
            return False

        print("   正在從 Wikipedia 獲取 0051 成分股...")
        try:
            df_51 = pd.read_html("https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A3%E4%B8%AD%E5%9E%8B100%E6%8C%87%E6%95%B8")[1]
            print(f"   ✅ 0051 成分股: {len(df_51)} 支")
            print(f"   前 5 支: {list(df_51['股票代號'].head())}")
        except Exception as e:
            print(f"   ❌ 0051 數據獲取失敗: {e}")
            return False

        # 合併股票池
        raw_pool = pd.concat([df_50['股票代號'], df_51['股票代號']]).unique()
        ticker_pool = [f"{str(code).strip()}.TW" for code in raw_pool]

        print(f"   📊 總股票池: {len(ticker_pool)} 支標的")
        print(f"   範例標的: {ticker_pool[:5]}")

        # --- 測試 3: 批次下載台股數據並篩選 ---
        print("\n💹 測試批次下載與篩選...")
        print(f"   正在下載 {len(ticker_pool)} 支台股數據...")

        # 限制測試數量以加快速度
        test_pool = ticker_pool[:20]  # 只測試前 20 支
        print(f"   (測試模式: 只下載前 {len(test_pool)} 支)")

        try:
            data = yf.download(test_pool, period="5d", group_by='ticker', progress=False)
            print("   ✅ 批次下載完成!")

            qualified_stocks = []
            processed_count = 0

            for ticker in test_pool:
                try:
                    hist = data[ticker] if len(test_pool) > 1 else data
                    price = hist['Close'].iloc[-1]
                    avg_vol = hist['Volume'].mean()

                    processed_count += 1

                    # 篩選：價格 20-50 元，且日均量 > 3000 張 (3,000,000 股)
                    if 20 <= price <= 50 and avg_vol > 3000000:
                        stock_info = f"{ticker}(價:{price:.1f},量:{int(avg_vol/1000)}K)"
                        qualified_stocks.append(stock_info)
                        print(f"   ✅ 符合條件: {stock_info}")
                    else:
                        reason = []
                        if not (20 <= price <= 50):
                            reason.append(f"價格{price:.1f}不在20-50範圍")
                        if avg_vol <= 3000000:
                            reason.append(f"均量{int(avg_vol/1000)}K太低")
                        print(f"   ⚠️  {ticker}: {', '.join(reason)}")

                except Exception as e:
                    print(f"   ❌ {ticker} 處理失敗: {str(e)[:50]}")
                    continue

            print(f"\n📋 篩選結果:")
            print(f"   處理標的: {processed_count}/{len(test_pool)}")
            print(f"   符合條件: {len(qualified_stocks)} 支")

            if qualified_stocks:
                print("   合格清單:")
                for stock in qualified_stocks:
                    print(f"     • {stock}")

                qualified_str = ", ".join(qualified_stocks)
                print(f"\n   格式化字串: {qualified_str}")
            else:
                print("   ⚠️  沒有找到符合條件的股票（可能因為測試樣本太小）")

            return True, market_summary, qualified_str if qualified_stocks else "測試模式：無符合條件股票"

        except Exception as e:
            print(f"   ❌ 批次下載失敗: {e}")
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"❌ 整體測試失敗: {e}")
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("🧪 股票數據獲取功能測試")
    print("本測試不需要 API 金鑰，專門驗證數據獲取功能")
    print("=" * 50)

    try:
        result = test_market_data()

        if result and result[0]:
            print("\n🎉 所有測試通過!")
            print("\n📄 最終報告預覽:")
            print("-" * 30)
            print(result[1])  # market_summary
            print(f"台股潛力候選: {result[2]}")  # qualified_stocks
            print("-" * 30)
            print("\n✅ 資料獲取功能正常，可以開始使用!")
        else:
            print("\n❌ 測試失敗，請檢查網路連接或程式碼")

    except Exception as e:
        print(f"\n💥 測試異常: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
