#!/usr/bin/env python3
"""
測試修改後的台股獲取功能
"""

import sys
import os

# 添加當前目錄到 path
sys.path.insert(0, '/Users/unlin/coding/learn/un-stock-hub')

# 導入修改後的函數
from stock_bot import get_taiwan_stock_pool, get_market_data

def test_new_stock_pool():
    """測試新的台股池獲取功能"""
    print("🧪 測試新的台股池獲取功能")
    print("=" * 50)

    try:
        # 測試台股池獲取
        ticker_pool = get_taiwan_stock_pool()

        if ticker_pool and len(ticker_pool) > 0:
            print(f"\n✅ 成功獲取 {len(ticker_pool)} 支台股")
            print(f"前 10 支: {ticker_pool[:10]}")
            print(f"最後 10 支: {ticker_pool[-10:]}")

            # 簡單驗證格式
            valid_format = all(stock.endswith('.TW') and stock[:-3].isdigit() for stock in ticker_pool[:5])
            if valid_format:
                print("✅ 股票代碼格式正確")
            else:
                print("⚠️  股票代碼格式需要檢查")

            return True, ticker_pool
        else:
            print("❌ 無法獲取台股清單")
            return False, []

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def test_market_data_complete():
    """測試完整的市場數據獲取（包含新的台股池）"""
    print("\n🧪 測試完整市場數據獲取")
    print("=" * 50)

    try:
        market_data, qualified_stocks = get_market_data()

        print(f"\n📊 市場數據:\n{market_data}")
        print(f"\n🎯 合格股票: {qualified_stocks}")

        if market_data and market_data != "無法獲取市場數據":
            print("\n✅ 完整測試成功！")
            return True
        else:
            print("\n❌ 完整測試失敗")
            return False

    except Exception as e:
        print(f"❌ 完整測試異常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 測試修改後的股票數據獲取功能")
    print("移除 Wikipedia 依賴，使用多重備用方案")
    print("=" * 60)

    # 測試 1: 台股池獲取
    success1, ticker_pool = test_new_stock_pool()

    # 測試 2: 完整市場數據
    success2 = test_market_data_complete()

    print("\n" + "=" * 60)
    print("📋 測試結果總結:")
    print(f"   台股池獲取: {'✅ 成功' if success1 else '❌ 失敗'}")
    print(f"   完整數據獲取: {'✅ 成功' if success2 else '❌ 失敗'}")

    if success1 and success2:
        print("\n🎉 所有測試通過！")
        print("📱 程式已準備好使用，不再依賴 Wikipedia")
        print("💡 現在使用多重數據源，確保穩定性更高")
    else:
        print("\n⚠️  部分功能需要檢查")

if __name__ == "__main__":
    main()
