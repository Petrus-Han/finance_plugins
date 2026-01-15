#!/usr/bin/env python3
"""诊断 Mercury API Token 问题"""

import sys
import httpx
import json

def test_token(token: str):
    """测试 Mercury API Token"""

    print("="*70)
    print("Mercury API Token 诊断工具")
    print("="*70)
    print(f"\nToken (前10字符): {token[:10]}...")
    print(f"Token 长度: {len(token)}")
    print()

    environments = [
        ("Production", "https://api.mercury.com/api/v1"),
        ("Sandbox", "https://api-sandbox.mercury.com/api/v1"),
    ]

    for env_name, base_url in environments:
        print(f"\n{'='*70}")
        print(f"测试环境: {env_name}")
        print(f"API URL: {base_url}")
        print('='*70)

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json;charset=utf-8",
        }

        # 测试 1: GET /accounts
        print("\n[测试] GET /accounts")
        try:
            response = httpx.get(
                f"{base_url}/accounts",
                headers=headers,
                timeout=15
            )

            print(f"  状态码: {response.status_code}")
            print(f"  响应头: {dict(response.headers)}")

            if response.status_code == 200:
                print(f"  ✅ 成功!")
                data = response.json()
                accounts = data.get("accounts", [])
                print(f"  账户数量: {len(accounts)}")
                if accounts:
                    print(f"\n  第一个账户:")
                    print(f"    ID: {accounts[0].get('id')}")
                    print(f"    名称: {accounts[0].get('name')}")
                    print(f"    类型: {accounts[0].get('type')}")
                return True

            elif response.status_code == 401:
                print(f"  ❌ 认证失败 (401)")
                print(f"  可能原因:")
                print(f"    1. Token 无效或已过期")
                print(f"    2. Token 不适用于此环境 ({env_name})")

            elif response.status_code == 403:
                print(f"  ❌ 权限不足 (403)")
                print(f"  可能原因:")
                print(f"    1. Token 缺少必要的权限")
                print(f"    2. 需要 'read:accounts' scope")

            elif response.status_code == 404:
                print(f"  ❌ 端点不存在 (404)")
                print(f"  可能原因:")
                print(f"    1. API 端点错误")
                print(f"    2. 此环境不支持该端点")

            else:
                print(f"  ❌ 未知错误 ({response.status_code})")

            # 打印响应内容
            try:
                response_data = response.json()
                print(f"\n  响应内容:")
                print(f"    {json.dumps(response_data, indent=4, ensure_ascii=False)}")
            except:
                print(f"\n  响应文本:")
                print(f"    {response.text[:500]}")

        except httpx.RequestException as e:
            print(f"  ❌ 网络错误: {e}")
        except Exception as e:
            print(f"  ❌ 未知错误: {e}")

    return False

def main():
    print()
    if len(sys.argv) < 2:
        print("用法: python debug_mercury_token.py <API_TOKEN>")
        print()
        print("示例:")
        print("  python debug_mercury_token.py your_token_here")
        print()
        sys.exit(1)

    token = sys.argv[1]
    result = test_token(token)

    print("\n" + "="*70)
    print("诊断建议")
    print("="*70)

    if not result:
        print("\n❌ Token 验证失败")
        print("\n请检查:")
        print("  1. Token 是否从正确的环境获取 (Production vs Sandbox)")
        print("  2. Token 是否有正确的权限:")
        print("     - read:accounts")
        print("     - read:transactions")
        print("  3. Token 是否已过期")
        print("\n获取 Token:")
        print("  Production: https://mercury.com/settings/tokens")
        print("  Sandbox: https://sandbox.mercury.com/settings/tokens")
    else:
        print("\n✅ Token 验证成功!")

    print()

if __name__ == "__main__":
    main()
