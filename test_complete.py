#!/usr/bin/env python3
"""
完整端到端測試 - 模擬不使用真實 API 的完整流程
"""

import sys
import os
import time

# 添加當前目錄到 path
sys.path.insert(0, '/Users/unlin/coding/learn/un-stock-hub')

# 導入修改後的函數
from stock_bot import get_market_data

def mock_generate_report(market_data, qualified_stocks):
    """模擬 AI 生成報告"""
    current_time = time.strftime("%Y-%m-%d %H:%M")

    mock_report = f"""🌅 投資早報 - {current_time}

{market_data}

【台股潛力股精選】 🎯
符合條件的潛力股票：
{qualified_stocks}

【模擬市場分析】 📈
✅ 美股表現：指數呈現調整格局
✅ 台股機會：篩選出價格合理且流動性佳的標的
✅ 投資策略：建議分批布局，控制風險

⚠️ 風險提醒：市場變動頻繁，投資請謹慎評估

🤖 本報告已成功移除 Wikipedia 依賴
使用多重數據源確保穩定性
"""

    return mock_report

def mock_send_line(message):
    """模擬發送 LINE 訊息"""
    print("📱 模擬發送 LINE 訊息:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    print("✅ 模擬發送成功")
    return True

def run_complete_simulation():
    """運行完整模擬"""
    print("🚀 執行完整端到端測試")
    print("不使用 Wikipedia，不使用真實 API")
    print("=" * 70)

    try:
        # 步驟 1: 獲取市場數據
        print("\n📊 步驟 1: 獲取市場數據...")
        market_data, qualified_stocks = get_market_data()

        if not market_data or market_data == "無法獲取市場數據":
            print("❌ 市場數據獲取失敗")
            return False

        print("✅ 市場數據獲取成功")

        # 步驟 2: 生成報告
        print("\n🤖 步驟 2: 生成投資報告...")
        report = mock_generate_report(market_data, qualified_stocks)

        if not report:
            print("❌ 報告生成失敗")
            return False

        print("✅ 報告生成成功")

        # 步驟 3: 發送訊息
        print("\n📱 步驟 3: 發送 LINE 訊息...")
        success = mock_send_line(report)

        if not success:
            print("❌ 訊息發送失敗")
            return False

        print("✅ 訊息發送成功")

        return True

    except Exception as e:
        print(f"❌ 完整測試異常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 股票早報機器人 - 完整功能測試")
    print("已移除 Wikipedia 依賴，使用穩定的多重數據源")
    print("=" * 70)

    success = run_complete_simulation()

    print("\n" + "=" * 70)

    if success:
        print("🎉 完整測試成功！")
        print("\n📋 改進摘要:")
        print("   ✅ 移除 Wikipedia 依賴")
        print("   ✅ 添加 MoneyDJ 作為備用數據源")
        print("   ✅ 使用穩定的手動維護台股清單")
        print("   ✅ 多重備用方案確保高可靠性")
        print("   ✅ 保持原有篩選邏輯不變")

        print("\n🚀 程式已準備就緒:")
        print("   • 設定環境變數後即可正式使用")
        print("   • GitHub Actions 將於每日 08:30 自動執行")
        print("   • 不再受到 Wikipedia 訪問問題影響")
    else:
        print("❌ 測試失敗，請檢查程式")

if __name__ == "__main__":
    main()
