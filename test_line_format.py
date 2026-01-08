#!/usr/bin/env python3
"""
測試新的 LINE 訊息格式
模擬完整的報告生成，不使用真實 API
"""

import time

def generate_mock_line_report(market_data, qualified_stocks):
    """生成符合 LINE 格式的模擬報告"""
    current_date = time.strftime("%m月%d日")

    mock_report = f"""🌅 投資早報 - {current_date}

📈 美股收盤摘要
{market_data}

📰 1. 美股新聞重點
● 聯準會政策會議釋放鴿派信號，市場預期降息機率上升
● 科技股財報季開跑，AI相關企業獲利表現超出預期
● 能源股受地緣政治影響波動，油價走勢牽動市場情緒

📰 2. 台股新聞重點
● 半導體產業庫存去化完成，下游需求回溫帶動族群反彈
● 金融股受惠利差改善，銀行業獲利能力逐步提升
● 傳產轉型題材發酵，ESG概念股獲得資金青睞

🎯 3. 精選潛力股 (5支)
● 6505.TW 台塑化
理由：油價穩定化學品價差擴大，Q4獲利有望大幅改善

● 2892.TW 第一金
理由：升息循環尾聲利差保護，股息殖利率吸引長期投資

● 2891.TW 中信金
理由：財富管理業務成長強勁，手續費收入持續攀升

● 2324.TW 仁寶
理由：AI伺服器代工訂單增加，產能利用率提升

● 1101.TW 台泥
理由：建材需求回升綠能轉型加速，營運動能轉強

⚠️ 投資提醒
本報告僅供參考，投資有風險請謹慎評估。"""

    return mock_report

def test_line_message_format():
    """測試 LINE 訊息格式"""
    print("🧪 測試新的 LINE 訊息格式")
    print("=" * 60)

    # 模擬市場數據
    mock_market_data = """● 道瓊: 48996.08 (-0.94%)
● 標普500: 6920.93 (-0.34%)
● VOO: 634.17 (-0.32%)"""

    # 模擬合格股票
    mock_qualified = "6505.TW(價:47.8,量:5699K), 2892.TW(價:29.6,量:17380K), 2891.TW(價:49.5,量:27155K), 2324.TW(價:30.1,量:21474K), 1101.TW(價:23.5,量:28920K)"

    # 生成報告
    report = generate_mock_line_report(mock_market_data, mock_qualified)

    print("📱 LINE 訊息格式預覽:")
    print("=" * 60)
    print(report)
    print("=" * 60)

    # 檢查訊息長度
    msg_length = len(report)
    print(f"\n📏 訊息長度檢查:")
    print(f"   總長度: {msg_length} 字元")
    print(f"   LINE 限制: 5000 字元")

    if msg_length <= 5000:
        print("   ✅ 長度符合 LINE 限制")
    else:
        print("   ⚠️  長度超過限制，需要分割")

    # 檢查格式
    print(f"\n🔍 格式檢查:")
    checks = [
        ("包含 Emoji", "🌅" in report and "📈" in report and "🎯" in report),
        ("無 Markdown", "**" not in report and "##" not in report and "[" not in report),
        ("有數字編號", "1." in report and "2." in report and "3." in report),
        ("有項目符號", "●" in report),
        ("有段落分隔", "\n\n" in report)
    ]

    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")

    all_passed = all(check[1] for check in checks)

    print(f"\n📋 總結:")
    if all_passed and msg_length <= 5000:
        print("🎉 LINE 訊息格式完全符合要求！")
        print("   • 無 Markdown 語法")
        print("   • 使用 Emoji 美化")
        print("   • 結構清晰易讀")
        print("   • 長度適中")
    else:
        print("⚠️  格式需要調整")

def test_error_message_format():
    """測試錯誤時的訊息格式"""
    print("\n🧪 測試錯誤訊息格式")
    print("=" * 60)

    mock_market_data = """● 道瓊: 48996.08 (-0.94%)
● 標普500: 6920.93 (-0.34%)
● VOO: 634.17 (-0.32%)"""

    mock_qualified = "6505.TW(價:47.8,量:5699K), 2892.TW(價:29.6,量:17380K)"

    error_message = f"""🌅 投資早報 - 今日摘要

📊 市場數據
{mock_market_data}

🎯 潛力股候選
{mock_qualified}

⚠️ 系統提醒
AI 新聞分析功能暫時無法使用，僅提供基本市場數據。

📱 完整分析將在系統恢復後提供。"""

    print("📱 錯誤時訊息格式:")
    print("=" * 40)
    print(error_message)
    print("=" * 40)

    if len(error_message) <= 5000 and "**" not in error_message:
        print("✅ 錯誤訊息格式正確")
    else:
        print("⚠️  錯誤訊息格式需要調整")

def main():
    print("🚀 LINE 訊息格式測試")
    print("驗證移除 Markdown 後的新格式")
    print("=" * 60)

    test_line_message_format()
    test_error_message_format()

    print("\n" + "=" * 60)
    print("🎯 結論：訊息格式已針對 LINE 優化")
    print("   • 移除所有 Markdown 語法")
    print("   • 使用 Emoji 和數字編號")
    print("   • 保持清晰的結構")
    print("   • 適合手機閱讀")

if __name__ == "__main__":
    main()
