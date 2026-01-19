#!/usr/bin/env python3
"""
Mercury Webhook 诊断脚本

用法:
    # 设置环境变量
    export MERCURY_API_TOKEN="your_production_token"

    # 运行诊断
    python scripts/diagnose_mercury_webhook.py

    # 创建测试 webhook (用 webhook.site URL)
    python scripts/diagnose_mercury_webhook.py --create-test "https://webhook.site/xxx"

    # 删除 webhook
    python scripts/diagnose_mercury_webhook.py --delete "webhook_id"
"""

import argparse
import os
import sys
import requests
from typing import Optional

# Mercury Production API
BASE_URL = "https://api.mercury.com/api/v1"


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def check_auth(token: str) -> bool:
    """环节 1: 检查 API 认证"""
    print("=" * 50)
    print("环节 1: 检查 API 认证")
    print("=" * 50)

    try:
        resp = requests.get(
            f"{BASE_URL}/accounts",
            headers=get_headers(token),
            timeout=15
        )

        if resp.status_code == 200:
            data = resp.json()
            accounts = data.get("accounts", [])
            print(f"✅ 认证成功")
            print(f"   找到 {len(accounts)} 个账户:")
            for acc in accounts[:3]:  # 只显示前3个
                print(f"   - {acc.get('name', 'N/A')} ({acc.get('kind', 'N/A')})")
            if len(accounts) > 3:
                print(f"   ... 还有 {len(accounts) - 3} 个账户")
            return True
        else:
            print(f"❌ 认证失败")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False


def list_webhooks(token: str) -> list:
    """环节 2: 列出所有 webhooks"""
    print("\n" + "=" * 50)
    print("环节 2: 列出已注册的 Webhooks")
    print("=" * 50)

    try:
        resp = requests.get(
            f"{BASE_URL}/webhooks",
            headers=get_headers(token),
            timeout=15
        )

        if resp.status_code == 200:
            data = resp.json()
            # Mercury 可能返回 {"webhooks": [...]} 或直接返回 [...]
            webhooks = data.get("webhooks", data) if isinstance(data, dict) else data

            if not webhooks:
                print("⚠️  没有找到任何 webhook")
                print("   这可能意味着:")
                print("   - Dify trigger 没有成功创建 webhook")
                print("   - webhook 已被删除")
                return []

            print(f"✅ 找到 {len(webhooks)} 个 webhook:\n")

            for i, wh in enumerate(webhooks, 1):
                print(f"Webhook #{i}")
                print(f"   ID:     {wh.get('id', 'N/A')}")
                print(f"   URL:    {wh.get('url', 'N/A')}")
                print(f"   Status: {wh.get('status', 'N/A')}")
                print(f"   Events: {wh.get('eventTypes', 'N/A')}")
                print(f"   Secret: {str(wh.get('secret', 'N/A'))[:20]}..." if wh.get('secret') else "   Secret: N/A")
                print()

            return webhooks
        else:
            print(f"❌ 获取 webhooks 失败")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return []


def create_webhook(token: str, url: str) -> Optional[dict]:
    """创建测试 webhook"""
    print("\n" + "=" * 50)
    print("创建测试 Webhook")
    print("=" * 50)
    print(f"URL: {url}")

    payload = {
        "url": url,
        "eventTypes": ["transaction.created", "transaction.updated"]
    }

    try:
        resp = requests.post(
            f"{BASE_URL}/webhooks",
            headers=get_headers(token),
            json=payload,
            timeout=15
        )

        if resp.status_code in [200, 201]:
            result = resp.json()
            print(f"\n✅ Webhook 创建成功!")
            print(f"   ID:     {result.get('id')}")
            print(f"   URL:    {result.get('url')}")
            print(f"   Status: {result.get('status')}")
            print(f"   Events: {result.get('eventTypes')}")

            secret = result.get('secret', '')
            if secret:
                print(f"   Secret: {secret[:30]}...")
                print(f"\n⚠️  请保存这个 Secret，后续验证签名需要用到")

            return result
        else:
            print(f"\n❌ 创建失败")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return None


def delete_webhook(token: str, webhook_id: str) -> bool:
    """删除 webhook"""
    print("\n" + "=" * 50)
    print(f"删除 Webhook: {webhook_id}")
    print("=" * 50)

    try:
        resp = requests.delete(
            f"{BASE_URL}/webhooks/{webhook_id}",
            headers=get_headers(token),
            timeout=15
        )

        if resp.status_code in [200, 204]:
            print(f"✅ Webhook 删除成功")
            return True
        elif resp.status_code == 404:
            print(f"⚠️  Webhook 不存在 (可能已被删除)")
            return True
        else:
            print(f"❌ 删除失败")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False


def print_next_steps(webhooks: list):
    """打印下一步建议"""
    print("\n" + "=" * 50)
    print("下一步建议")
    print("=" * 50)

    if not webhooks:
        print("""
1. 检查 Dify Trigger 是否成功创建
   - 在 Dify 中查看 trigger 配置
   - 检查 Dify 日志是否有错误

2. 手动创建测试 webhook:
   python scripts/diagnose_mercury_webhook.py --create-test "https://webhook.site/YOUR-ID"

3. 在 Mercury 账户中触发一笔交易

4. 检查 webhook.site 是否收到请求
""")
    else:
        print("""
Webhook 已存在，接下来验证:

1. 检查 webhook URL 是否指向你的 Dify 实例
   - 应该类似: https://your-dify.com/webhook/xxx

2. 用 webhook.site 测试 Mercury 是否发送 webhook:
   a. 访问 https://webhook.site 获取临时 URL
   b. 创建测试 webhook:
      python scripts/diagnose_mercury_webhook.py --create-test "https://webhook.site/YOUR-ID"
   c. 在 Mercury 触发交易
   d. 检查 webhook.site 是否收到请求

3. 如果 webhook.site 收到请求但 Dify 没反应:
   - 检查 Dify 网络配置 (防火墙、HTTPS 证书等)
   - 检查 Dify 插件日志
""")


def main():
    parser = argparse.ArgumentParser(description="Mercury Webhook 诊断工具")
    parser.add_argument(
        "--create-test",
        metavar="URL",
        help="创建测试 webhook (推荐用 webhook.site URL)"
    )
    parser.add_argument(
        "--delete",
        metavar="WEBHOOK_ID",
        help="删除指定的 webhook"
    )
    args = parser.parse_args()

    # 获取 API token
    token = os.environ.get("MERCURY_API_TOKEN")
    if not token:
        print("❌ 请设置环境变量 MERCURY_API_TOKEN")
        print("   export MERCURY_API_TOKEN='your_production_api_token'")
        sys.exit(1)

    print("\n🔍 Mercury Webhook 诊断工具\n")

    # 检查认证
    if not check_auth(token):
        print("\n❌ API 认证失败，请检查 token 是否正确")
        sys.exit(1)

    # 执行操作
    if args.delete:
        delete_webhook(token, args.delete)
    elif args.create_test:
        create_webhook(token, args.create_test)

    # 列出 webhooks
    webhooks = list_webhooks(token)

    # 打印建议
    print_next_steps(webhooks)


if __name__ == "__main__":
    main()
