#!/usr/bin/env python3
"""
測試環境變數設定
"""

import os

def test_env_vars():
    """檢查必要的環境變數"""
    print("🔐 檢查環境變數設定...")

    required_vars = {
        'GEMINI_API_KEY': 'Gemini AI API 金鑰',
        'DISCORD_WEBHOOK_URL': 'Discord Webhook URL'
    }

    results = {}

    for var_name, description in required_vars.items():
        value = os.environ.get(var_name)
        if value:
            # 隱藏敏感資訊
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"   ✅ {var_name}: {masked_value}")
            results[var_name] = True
        else:
            print(f"   ❌ {var_name}: 未設定")
            results[var_name] = False

    print("\n📋 環境變數檢查結果：")
    for var_name, is_set in results.items():
        status = "✅ 已設定" if is_set else "❌ 未設定"
        print(f"   {var_name}: {status}")

    all_set = all(results.values())

    if all_set:
        print("\n🎉 所有環境變數都已正確設定！")
        print("您現在可以執行原始程式： python stock_bot.py")
    else:
        print("\n⚠️  部分環境變數未設定")
        print("請設定缺少的環境變數後再執行原始程式")
        print("\n💡 設定方式：")
        for var_name, is_set in results.items():
            if not is_set:
                print(f"   export {var_name}='your_key_here'")

    return all_set

def main():
    print("🧪 環境變數測試")
    print("=" * 40)
    test_env_vars()

if __name__ == "__main__":
    main()
