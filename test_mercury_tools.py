#!/usr/bin/env python3
"""测试 Mercury Tools 插件的工具"""

import sys
import httpx
import json
from datetime import datetime, timedelta

class MercuryToolsTester:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.mercury.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

    def test_get_accounts(self):
        """测试 get_accounts 工具"""
        print("\n" + "="*60)
        print("测试 1: Get Accounts")
        print("="*60)

        try:
            response = httpx.get(
                f"{self.base_url}/accounts",
                headers=self.headers,
                timeout=15
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                accounts = data.get("accounts", [])
                print(f"✅ 成功获取 {len(accounts)} 个账户")

                for i, account in enumerate(accounts, 1):
                    print(f"\n账户 {i}:")
                    print(f"  ID: {account.get('id')}")
                    print(f"  名称: {account.get('name')}")
                    print(f"  类型: {account.get('type')}")
                    print(f"  当前余额: ${account.get('currentBalance', 0):,.2f}")
                    print(f"  可用余额: ${account.get('availableBalance', 0):,.2f}")

                return accounts
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"响应: {response.text}")
                return []

        except Exception as e:
            print(f"❌ 错误: {e}")
            return []

    def test_get_account(self, account_id: str):
        """测试 get_account 工具"""
        print("\n" + "="*60)
        print(f"测试 2: Get Account (ID: {account_id})")
        print("="*60)

        try:
            response = httpx.get(
                f"{self.base_url}/account/{account_id}",
                headers=self.headers,
                timeout=15
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                account = response.json()
                print("✅ 成功获取账户详情")
                print(f"\n账户详情:")
                print(f"  ID: {account.get('id')}")
                print(f"  名称: {account.get('name')}")
                print(f"  类型: {account.get('type')}")
                print(f"  状态: {account.get('status')}")
                print(f"  当前余额: ${account.get('currentBalance', 0):,.2f}")
                print(f"  可用余额: ${account.get('availableBalance', 0):,.2f}")
                print(f"  货币: {account.get('currency', 'USD')}")
                print(f"  路由号码: {account.get('routingNumber', 'N/A')}")

                return account
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"响应: {response.text}")
                return None

        except Exception as e:
            print(f"❌ 错误: {e}")
            return None

    def test_get_transactions(self, account_id: str, limit: int = 10):
        """测试 get_transactions 工具"""
        print("\n" + "="*60)
        print(f"测试 3: Get Transactions (账户: {account_id}, 限制: {limit})")
        print("="*60)

        # 获取最近30天的交易
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        params = {
            "limit": limit,
            "offset": 0,
        }

        try:
            response = httpx.get(
                f"{self.base_url}/account/{account_id}/transactions",
                headers=self.headers,
                params=params,
                timeout=15
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                transactions = data.get("transactions", [])
                total = data.get("total", len(transactions))

                print(f"✅ 成功获取 {len(transactions)} 笔交易（总计: {total}）")

                if transactions:
                    print("\n最近的交易:")
                    for i, txn in enumerate(transactions[:5], 1):  # 只显示前5笔
                        amount = txn.get('amount', 0)
                        sign = "-" if amount < 0 else "+"
                        print(f"\n交易 {i}:")
                        print(f"  ID: {txn.get('id')}")
                        print(f"  金额: {sign}${abs(amount):,.2f}")
                        print(f"  日期: {txn.get('postedAt', 'N/A')}")
                        print(f"  商家: {txn.get('counterpartyName', 'N/A')}")
                        print(f"  描述: {txn.get('bankDescription', 'N/A')}")
                        print(f"  状态: {txn.get('status', 'N/A')}")
                        print(f"  类型: {txn.get('type', 'N/A')}")
                else:
                    print("\n⚠️ 该账户暂无交易记录")

                return transactions
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"响应: {response.text}")
                return []

        except Exception as e:
            print(f"❌ 错误: {e}")
            return []

def main():
    print("\n" + "="*60)
    print("Mercury Tools 插件测试")
    print("="*60)

    if len(sys.argv) < 2:
        print("\n用法: python test_mercury_tools.py <API_TOKEN>")
        print("\n示例:")
        print("  python test_mercury_tools.py your_token_here")
        sys.exit(1)

    access_token = sys.argv[1]
    tester = MercuryToolsTester(access_token)

    # 测试 1: 获取所有账户
    accounts = tester.test_get_accounts()

    if not accounts:
        print("\n❌ 无法获取账户列表，测试终止")
        sys.exit(1)

    # 使用第一个账户进行后续测试
    first_account_id = accounts[0].get('id')

    # 测试 2: 获取单个账户详情
    account = tester.test_get_account(first_account_id)

    # 测试 3: 获取交易记录
    transactions = tester.test_get_transactions(first_account_id, limit=10)

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"✅ 获取账户列表: {'成功' if accounts else '失败'}")
    print(f"✅ 获取账户详情: {'成功' if account else '失败'}")
    print(f"✅ 获取交易记录: {'成功' if transactions is not None else '失败'}")
    print("\n所有测试完成！")

if __name__ == "__main__":
    main()
