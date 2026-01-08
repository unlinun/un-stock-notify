#!/usr/bin/env python3
"""
簡化測試版本 - 逐步測試各個功能
"""

import pandas as pd
import yfinance as yf
import time

def test_basic_yfinance():
    """測試基本 yfinance 功能"""
    print("🔍 測試基本 yfinance 功能...")
    try:
        # 測試單一股票
        print("   測試獲取 AAPL 數據...")
        aapl = yf.Ticker("AAPL")
        hist = aapl.history(period="2d")
        print(f"   ✅ AAPL 數據: {len(hist)} 天")
        print(f"   最新價格: ${hist['Close'].iloc[-1]:.2f}")
        return True
    except Exception as e:
        print(f"   ❌ 基本測試失敗: {e}")
        return False

def test_us_indices():
    """測試美股指數"""
    print("\n📊 測試美股指數...")
    indices = {"^DJI": "道瓊", "^GSPC": "標普500", "VOO": "VOO"}

    for symbol, name in indices.items():
        try:
            print(f"   測試 {name} ({symbol})...")
            tk = yf.Ticker(symbol)
            hist = tk.history(period="2d")

            if len(hist) >= 1:
                price = hist['Close'].iloc[-1]
                print(f"   ✅ {name}: ${price:.2f}")
            else:
                print(f"   ⚠️  {name}: 無數據")

        except Exception as e:
            print(f"   ❌ {name} 失敗: {e}")
    return True

def test_wikipedia_access():
    """測試 Wikipedia 訪問"""
    print("\n🌐 測試 Wikipedia 數據獲取...")
    try:
        print("   測試 0050 成分股頁面...")
        df_50 = pd.read_html("https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A350%E6%8C%87%E6%95%B8")
        print(f"   ✅ 找到 {len(df_50)} 個表格")

        target_table = df_50[2]  # 第3個表格是成分股
        print(f"   ✅ 成分股表格: {len(target_table)} 支股票")
        print(f"   前 3 支: {list(target_table['股票代號'].head(3))}")
        return True
    except Exception as e:
        print(f"   ❌ Wikipedia 訪問失敗: {e}")
        return False

def test_taiwan_stock():
    """測試台股數據"""
    print("\n🇹🇼 測試台股數據...")
    try:
        # 測試台積電
        print("   測試台積電 (2330.TW)...")
        tsm = yf.Ticker("2330.TW")
        hist = tsm.history(period="2d")

        if len(hist) >= 1:
            price = hist['Close'].iloc[-1]
            volume = hist['Volume'].iloc[-1]
            print(f"   ✅ 台積電: NT${price:.2f}, 成交量: {int(volume/1000)}K")
        else:
            print("   ⚠️  台積電: 無數據")

        return True
    except Exception as e:
        print(f"   ❌ 台股測試失敗: {e}")
        return False

def main():
    """主測試流程"""
    print("🧪 分步驟資料獲取測試")
    print("=" * 40)

    tests = [
        ("基本功能", test_basic_yfinance),
        ("美股指數", test_us_indices),
        ("Wikipedia", test_wikipedia_access),
        ("台股數據", test_taiwan_stock)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🚀 開始測試: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} 測試通過")
            else:
                print(f"❌ {test_name} 測試失敗")
        except Exception as e:
            print(f"💥 {test_name} 測試異常: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 40)
    print("📋 測試結果摘要:")
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")

    passed = sum(1 for _, result in results if result)
    print(f"\n總結: {passed}/{len(results)} 項測試通過")

    if passed == len(results):
        print("🎉 所有測試通過！資料獲取功能正常")
    else:
        print("⚠️  部分測試失敗，請檢查網路連接")

if __name__ == "__main__":
    main()
