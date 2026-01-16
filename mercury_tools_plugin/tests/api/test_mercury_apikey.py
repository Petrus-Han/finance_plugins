#!/usr/bin/env python3
"""测试 Mercury API Key 的详细诊断脚本"""

import sys
import json
import httpx
from datetime import datetime


def test_mercury_apikey(api_key: str, environment: str = "production"):
    """
    测试 Mercury API Key

    Args:
        api_key: Mercury API Token
        environment: 'production' 或 'sandbox'
    """
    print("=" * 80)
    print(f"Mercury API Key 诊断工具 - {environment.upper()}")
    print("=" * 80)
    print(f"\n测试时间: {datetime.now().isoformat()}")
    print(f"API Key (前12字符): {api_key[:12]}...")
    print(f"API Key 长度: {len(api_key)}")
    print(f"环境: {environment}")
    print()

    # 确定 API Base URL
    if environment.lower() == "sandbox":
        base_url = "https://api-sandbox.mercury.com/api/v1"
    else:
        base_url = "https://api.mercury.com/api/v1"

    print(f"API Base URL: {base_url}")
    print()

    # 准备请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json;charset=utf-8",
    }

    print("=" * 80)
    print("测试 1: GET /accounts (获取账户列表)")
    print("=" * 80)

    try:
        print(f"\n发送请求到: {base_url}/accounts")
        print(f"请求头:")
        print(f"  Authorization: Bearer {api_key[:12]}...{api_key[-4:]}")
        print(f"  Accept: {headers['Accept']}")

        response = httpx.get(
            f"{base_url}/accounts",
            headers=headers,
            timeout=15
        )

        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头:")
        for key, value in response.headers.items():
            if key.lower() in ['content-type', 'date', 'x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset']:
                print(f"  {key}: {value}")

        if response.status_code == 200:
            print("\n✅ 成功！API Key 有效")
            data = response.json()

            print(f"\n响应数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))

            accounts = data.get("accounts", [])
            print(f"\n📊 找到 {len(accounts)} 个账户")

            if accounts:
                print("\n账户列表:")
                for idx, account in enumerate(accounts, 1):
                    print(f"\n  账户 {idx}:")
                    print(f"    ID: {account.get('id')}")
                    print(f"    名称: {account.get('name')}")
                    print(f"    类型: {account.get('type')}")
                    print(f"    状态: {account.get('status')}")
                    print(f"    当前余额: {account.get('currentBalance')}")
                    print(f"    可用余额: {account.get('availableBalance')}")
                    print(f"    货币: {account.get('currency', 'USD')}")

                # 测试获取第一个账户的交易
                print("\n" + "=" * 80)
                print("测试 2: GET /account/{id}/transactions (获取交易记录)")
                print("=" * 80)

                first_account_id = accounts[0]['id']
                print(f"\n使用账户 ID: {first_account_id}")

                tx_response = httpx.get(
                    f"{base_url}/account/{first_account_id}/transactions",
                    headers=headers,
                    params={"limit": 5},
                    timeout=15
                )

                print(f"响应状态码: {tx_response.status_code}")

                if tx_response.status_code == 200:
                    print("✅ 成功获取交易记录")
                    tx_data = tx_response.json()
                    transactions = tx_data.get("transactions", [])
                    print(f"\n找到 {len(transactions)} 笔交易（显示最近 5 笔）")

                    if transactions:
                        for idx, tx in enumerate(transactions, 1):
                            print(f"\n  交易 {idx}:")
                            print(f"    ID: {tx.get('id')}")
                            print(f"    金额: {tx.get('amount')}")
                            print(f"    时间: {tx.get('postedAt')}")
                            print(f"    状态: {tx.get('status')}")
                            print(f"    对方: {tx.get('counterpartyName')}")
                            print(f"    描述: {tx.get('bankDescription')}")
                else:
                    print(f"❌ 获取交易失败: {tx_response.status_code}")
                    try:
                        error_data = tx_response.json()
                        print(f"错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                    except:
                        print(f"错误响应: {tx_response.text[:500]}")

            return True

        elif response.status_code == 401:
            print("\n❌ 认证失败 (401 Unauthorized)")
            print("\n可能原因:")
            print("  1. API Key 无效")
            print("  2. API Key 已过期")
            print("  3. API Key 被撤销")
            print("  4. API Key 不适用于此环境")

            try:
                error_data = response.json()
                print(f"\n错误详情:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"\n错误响应文本:")
                print(response.text[:500])

        elif response.status_code == 403:
            print("\n❌ 权限不足 (403 Forbidden)")
            print("\n可能原因:")
            print("  1. API Key 缺少必要的权限")
            print("  2. 需要 'read:accounts' scope")

            try:
                error_data = response.json()
                print(f"\n错误详情:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"\n错误响应文本:")
                print(response.text[:500])

        elif response.status_code == 404:
            print("\n❌ 端点不存在 (404 Not Found)")
            print("\n可能原因:")
            print("  1. API Base URL 错误")
            print("  2. 此环境不支持该端点")

            try:
                error_data = response.json()
                print(f"\n错误详情:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"\n错误响应文本:")
                print(response.text[:500])

        else:
            print(f"\n❌ 请求失败 ({response.status_code})")

            try:
                error_data = response.json()
                print(f"\n错误详情:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"\n错误响应文本:")
                print(response.text[:500])

        return False

    except httpx.TimeoutException:
        print("\n❌ 请求超时")
        print("可能原因:")
        print("  1. 网络连接问题")
        print("  2. Mercury API 响应缓慢")
        return False

    except httpx.ConnectError as e:
        print(f"\n❌ 连接错误: {e}")
        print("可能原因:")
        print("  1. 无法连接到 Mercury API")
        print("  2. 网络连接问题")
        print("  3. DNS 解析失败")
        return False

    except Exception as e:
        print(f"\n❌ 未知错误: {type(e).__name__}: {e}")
        import traceback
        print("\n详细错误:")
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print()

    if len(sys.argv) < 2:
        print("用法: python test_mercury_apikey.py <API_KEY> [environment]")
        print()
        print("参数:")
        print("  API_KEY      - Mercury API Token (必需)")
        print("  environment  - 'production' 或 'sandbox' (可选，默认 'production')")
        print()
        print("示例:")
        print("  python test_mercury_apikey.py your_api_key_here")
        print("  python test_mercury_apikey.py your_api_key_here production")
        print("  python test_mercury_apikey.py your_api_key_here sandbox")
        print()
        sys.exit(1)

    api_key = sys.argv[1]
    environment = sys.argv[2] if len(sys.argv) > 2 else "production"

    if environment.lower() not in ["production", "sandbox"]:
        print(f"❌ 错误: 环境必须是 'production' 或 'sandbox'，但得到 '{environment}'")
        sys.exit(1)

    # 测试指定环境
    result = test_mercury_apikey(api_key, environment)

    # 如果失败，建议尝试另一个环境
    if not result:
        other_env = "sandbox" if environment.lower() == "production" else "production"
        print("\n" + "=" * 80)
        print("建议")
        print("=" * 80)
        print(f"\n当前环境 '{environment}' 测试失败")
        print(f"建议尝试另一个环境: {other_env}")
        print(f"\n运行命令:")
        print(f"  python test_mercury_apikey.py {api_key[:12]}... {other_env}")

    print("\n" + "=" * 80)
    print("诊断建议")
    print("=" * 80)

    if not result:
        print("\n❌ API Key 验证失败")
        print("\n请检查:")
        print("  1. API Key 是否从正确的环境获取")
        print("     - Production: https://mercury.com/settings/tokens")
        print("     - Sandbox: https://sandbox.mercury.com/settings/tokens")
        print("  2. API Key 是否有正确的权限:")
        print("     - read:accounts")
        print("     - read:transactions")
        print("  3. API Key 是否已过期或被撤销")
        print("  4. 环境选择是否正确 (production vs sandbox)")
    else:
        print("\n✅ API Key 验证成功!")
        print("\n可以在 Dify 插件中使用此 API Key:")
        print(f"  - 环境: {environment}")
        print(f"  - API Key: {api_key[:12]}...{api_key[-4:]}")

    print()


if __name__ == "__main__":
    main()
