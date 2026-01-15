#!/usr/bin/env python3
"""本地测试 Mercury Tools Plugin"""

import sys
import os

# 添加插件目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mercury_tools_plugin'))

from collections.abc import Mapping
from typing import Any


# 模拟 Dify Runtime
class MockRuntime:
    def __init__(self, credentials: dict):
        self.credentials = credentials


class MockSession:
    class MockModel:
        class MockSummary:
            @staticmethod
            def invoke(text: str, instruction: str) -> str:
                """模拟 summary 调用，直接返回原文"""
                return text

        summary = MockSummary()

    model = MockModel()


# 测试 Provider
def test_provider(api_key: str, environment: str = "sandbox"):
    """测试 Provider 验证"""
    print("=" * 80)
    print("测试 Mercury Tools Provider 验证")
    print("=" * 80)

    from provider.mercury_tools import MercuryToolsProvider

    provider = MercuryToolsProvider()

    credentials = {
        "access_token": api_key,
        "api_environment": environment
    }

    try:
        print(f"\n验证凭证...")
        print(f"  Environment: {environment}")
        print(f"  API Key: {api_key[:12]}...{api_key[-4:]}")

        provider._validate_credentials(credentials)
        print("\n✅ Provider 验证成功!")
        return True
    except Exception as e:
        print(f"\n❌ Provider 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


# 测试 get_accounts 工具
def test_get_accounts(api_key: str, environment: str = "sandbox"):
    """测试 get_accounts 工具"""
    print("\n" + "=" * 80)
    print("测试 get_accounts 工具")
    print("=" * 80)

    from tools.get_accounts import GetAccountsTool

    runtime = MockRuntime({
        "access_token": api_key,
        "api_environment": environment
    })
    session = MockSession()
    tool = GetAccountsTool(runtime=runtime, session=session)

    try:
        print("\n调用 get_accounts...")
        results = list(tool._invoke({}))

        print(f"\n返回了 {len(results)} 个消息:")
        for idx, result in enumerate(results, 1):
            print(f"\n消息 {idx}:")
            print(f"  类型: {result.__class__.__name__}")
            if hasattr(result, 'message'):
                msg = str(result.message)
                print(f"  内容: {msg[:200]}...")
            elif hasattr(result, 'json_object'):
                import json
                print(f"  JSON: {json.dumps(result.json_object, indent=2, ensure_ascii=False)[:500]}...")

        print("\n✅ get_accounts 测试成功!")
        return True
    except Exception as e:
        print(f"\n❌ get_accounts 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


# 测试 get_account 工具
def test_get_account(api_key: str, account_id: str, environment: str = "sandbox"):
    """测试 get_account 工具"""
    print("\n" + "=" * 80)
    print("测试 get_account 工具")
    print("=" * 80)

    from tools.get_account import GetAccountTool

    runtime = MockRuntime({
        "access_token": api_key,
        "api_environment": environment
    })
    session = MockSession()
    tool = GetAccountTool(runtime=runtime, session=session)

    try:
        print(f"\n调用 get_account...")
        print(f"  Account ID: {account_id}")

        results = list(tool._invoke({"account_id": account_id}))

        print(f"\n返回了 {len(results)} 个消息:")
        for idx, result in enumerate(results, 1):
            print(f"\n消息 {idx}:")
            print(f"  类型: {result.__class__.__name__}")
            if hasattr(result, 'message'):
                msg = str(result.message)
                print(f"  内容: {msg[:200]}...")
            elif hasattr(result, 'json_object'):
                import json
                print(f"  JSON: {json.dumps(result.json_object, indent=2, ensure_ascii=False)[:500]}...")

        print("\n✅ get_account 测试成功!")
        return True
    except Exception as e:
        print(f"\n❌ get_account 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


# 测试 get_transactions 工具
def test_get_transactions(api_key: str, account_id: str, environment: str = "sandbox"):
    """测试 get_transactions 工具"""
    print("\n" + "=" * 80)
    print("测试 get_transactions 工具")
    print("=" * 80)

    from tools.get_transactions import GetTransactionsTool

    runtime = MockRuntime({
        "access_token": api_key,
        "api_environment": environment
    })
    session = MockSession()
    tool = GetTransactionsTool(runtime=runtime, session=session)

    try:
        print(f"\n调用 get_transactions...")
        print(f"  Account ID: {account_id}")
        print(f"  Limit: 5")

        results = list(tool._invoke({
            "account_id": account_id,
            "limit": 5
        }))

        print(f"\n返回了 {len(results)} 个消息:")
        for idx, result in enumerate(results, 1):
            print(f"\n消息 {idx}:")
            print(f"  类型: {result.__class__.__name__}")
            if hasattr(result, 'message'):
                msg = str(result.message)
                print(f"  内容: {msg[:200]}...")
            elif hasattr(result, 'json_object'):
                import json
                print(f"  JSON: {json.dumps(result.json_object, indent=2, ensure_ascii=False)[:500]}...")

        print("\n✅ get_transactions 测试成功!")
        return True
    except Exception as e:
        print(f"\n❌ get_transactions 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    api_key = "secret-token:mercury_sandbox_wma_tGx7hBKbXmnFJy3xHjtZV4t2J717xe6XT9EZSdnmUbMmh_yrucrem"
    environment = "sandbox"

    print("\n" + "=" * 80)
    print("Mercury Tools Plugin 本地测试")
    print("=" * 80)
    print(f"\nAPI Key: {api_key[:12]}...{api_key[-4:]}")
    print(f"Environment: {environment}")
    print()

    results = []

    # 测试 1: Provider 验证
    results.append(("Provider 验证", test_provider(api_key, environment)))

    # 测试 2: get_accounts
    results.append(("get_accounts", test_get_accounts(api_key, environment)))

    # 测试 3: get_account
    # 使用第一个账户 ID
    account_id = "717cd9fe-e534-11f0-a795-27b3496b6aa5"
    results.append(("get_account", test_get_account(api_key, account_id, environment)))

    # 测试 4: get_transactions
    results.append(("get_transactions", test_get_transactions(api_key, account_id, environment)))

    # 汇总结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)

    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{name:30s} {status}")

    all_passed = all(success for _, success in results)

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 所有测试通过!")
    else:
        print("❌ 有测试失败，请检查上面的错误信息")
    print("=" * 80)
    print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
