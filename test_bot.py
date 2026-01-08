#!/usr/bin/env python3
"""
股票機器人簡化測試
測試核心功能，不生成複雜報告
"""

import os
import sys
import pandas as pd
import yfinance as yf

def test_environment():
    """檢查環境變數配置"""
    print("🔐 檢查環境配置...")

    required_vars = ['GEMINI_API_KEY']
    optional_vars = ['LINE_ACCESS_TOKEN', 'LINE_USER_ID', 'DISCORD_WEBHOOK_URL']
    missing_required = []

    # 檢查必要變數
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_required.append(var)
        else:
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"   ✅ {var}: {masked_value}")

    # 檢查可選變數（通知管道）
    notification_channels = 0
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"   ✅ {var}: {masked_value}")
            if var in ['LINE_ACCESS_TOKEN', 'DISCORD_WEBHOOK_URL']:
                notification_channels += 1
        else:
            print(f"   ⚠️  {var}: 未設定（可選）")

    if missing_required:
        print(f"   ❌ 缺少必要環境變數: {missing_required}")
        return False

    if notification_channels == 0:
        print("   ⚠️  建議至少設定一個通知管道（LINE 或 Discord）")

    print("   ✅ 環境配置檢查完成")
    return True

def test_yfinance_connection():
    """測試 yfinance 連線功能"""
    print("\n📊 測試資料獲取...")

    try:
        # 測試美股指數
        print("   測試美股指數...")
        dji = yf.Ticker("^DJI")
        hist = dji.history(period="2d")

        if len(hist) > 0:
            price = hist['Close'].iloc[-1]
            print(f"   ✅ 道瓊指數: {price:.2f}")
        else:
            print("   ❌ 無法獲取道瓊數據")
            return False

        # 測試台股
        print("   測試台股數據...")
        tsmc = yf.Ticker("2330.TW")
        hist = tsmc.history(period="2d")

        if len(hist) > 0:
            price = hist['Close'].iloc[-1]
            print(f"   ✅ 台積電: {price:.2f} TWD")
        else:
            print("   ❌ 無法獲取台股數據")
            return False

        return True

    except Exception as e:
        print(f"   ❌ yfinance 測試失敗: {e}")
        return False

def test_taiwan_stock_pool():
    """測試台股池獲取功能"""
    print("\n🔍 測試台股池功能...")

    try:
        # 導入並測試 get_taiwan_stock_pool 函數
        from stock_bot import get_taiwan_stock_pool

        print("   正在獲取台股池...")
        ticker_pool = get_taiwan_stock_pool()

        if len(ticker_pool) > 0:
            print(f"   ✅ 股票池包含 {len(ticker_pool)} 支股票")
            print(f"   範例股票: {ticker_pool[:3]}")
            return True
        else:
            print("   ❌ 股票池為空")
            return False

    except ImportError as e:
        print(f"   ❌ 無法導入股票池函數: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 股票池測試失敗: {e}")
        return False

def test_market_data():
    """測試市場數據獲取功能"""
    print("\n📈 測試市場數據功能...")

    try:
        from stock_bot import get_market_data

        print("   正在獲取市場數據...")
        market_data, qualified_stocks = get_market_data()

        if market_data and "美股" in market_data:
            print("   ✅ 市場數據獲取成功")
            print("   ✅ 股票篩選功能正常")
            print(f"   符合條件股票數量: {len(qualified_stocks.split(',')) if qualified_stocks else 0}")
            return True
        else:
            print("   ❌ 市場數據格式異常")
            return False

    except ImportError as e:
        print(f"   ❌ 無法導入市場數據函數: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 市場數據測試失敗: {e}")
        return False

def test_gemini_connection():
    """測試 Gemini AI 連線"""
    print("\n🤖 測試 Gemini AI 連線...")

    try:
        from google import genai

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            print("   ❌ GEMINI_API_KEY 未設定")
            return False

        client = genai.Client(api_key=api_key)

        # 簡單測試請求
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="請回答：測試成功",
        )

        if response and response.text:
            print("   ✅ Gemini AI 連線正常")
            return True
        else:
            print("   ❌ Gemini AI 無回應")
            return False

    except ImportError as e:
        print(f"   ❌ 無法導入 Gemini 模組: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Gemini 測試失敗: {e}")
        return False

def test_discord_connection():
    """測試 Discord Webhook 連線"""
    print("\n💬 測試 Discord 連線...")

    try:
        import requests

        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        if not webhook_url:
            print("   ⚠️  DISCORD_WEBHOOK_URL 未設定")
            return True  # 這是可選的，所以回傳 True

        # 發送測試訊息
        test_payload = {"content": "🤖 股票機器人測試訊息"}
        response = requests.post(webhook_url, json=test_payload)

        if response.status_code in [200, 204]:
            print("   ✅ Discord Webhook 連線正常")
            return True
        else:
            print(f"   ❌ Discord Webhook 回應異常: {response.status_code}")
            return False

    except ImportError as e:
        print(f"   ❌ 無法導入 requests 模組: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Discord 測試失敗: {e}")
        return False

def run_tests():
    """執行所有測試"""
    print("🚀 開始股票機器人測試\n")

    tests = [
        ("環境變數", test_environment),
        ("資料連線", test_yfinance_connection),
        ("台股池", test_taiwan_stock_pool),
        ("市場數據", test_market_data),
        ("Gemini AI", test_gemini_connection),
        ("Discord 連線", test_discord_connection)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ 測試 {test_name} 發生異常: {e}")
            results.append((test_name, False))

    # 結果總結
    print("\n" + "="*50)
    print("📋 測試結果")
    print("="*50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name:10}: {status}")
        if result:
            passed += 1

    print(f"\n總計: {passed}/{total} 項測試通過")

    if passed == total:
        print("🎉 所有測試通過！機器人可以正常運行")
        return True
    else:
        print("⚠️  部分測試失敗，請檢查相關設定")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
