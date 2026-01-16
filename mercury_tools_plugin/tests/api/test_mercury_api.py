#!/usr/bin/env python3
"""测试 Mercury API Key 是否有效"""

import httpx
import sys

# Mercury API URLs (参考: https://docs.mercury.com/docs/using-mercury-sandbox)
SANDBOX_URL = "https://api-sandbox.mercury.com/api/v1"
PRODUCTION_URL = "https://api.mercury.com/api/v1"

def test_api_key(access_token: str, use_sandbox: bool = True):
    """测试 Mercury API Key"""
    
    base_url = SANDBOX_URL if use_sandbox else PRODUCTION_URL
    env_name = "Sandbox" if use_sandbox else "Production"
    
    print(f"\n{'='*60}")
    print(f"测试 Mercury API Key ({env_name})")
    print(f"{'='*60}")
    print(f"API URL: {base_url}")
    print(f"Token: {access_token[:10]}...{access_token[-4:] if len(access_token) > 14 else ''}")
    print()
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    
    # 测试 1: 获取账户列表
    print("[测试 1] GET /accounts")
    try:
        response = httpx.get(f"{base_url}/accounts", headers=headers, timeout=15)
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text[:500]}")
        
        if response.status_code == 200:
            print("  ✅ API Key 有效!")
            return True
        elif response.status_code == 401:
            print("  ❌ API Key 无效或已过期")
        elif response.status_code == 403:
            print("  ❌ API Key 权限不足")
        else:
            print(f"  ⚠️ 未知错误: {response.status_code}")
            
    except httpx.RequestException as e:
        print(f"  ❌ 网络错误: {e}")
    
    return False

def main():
    if len(sys.argv) < 2:
        print("用法: python test_mercury_api.py <API_TOKEN> [sandbox|production]")
        print()
        print("示例:")
        print("  python test_mercury_api.py your_token_here sandbox")
        print("  python test_mercury_api.py your_token_here production")
        sys.exit(1)
    
    access_token = sys.argv[1]
    use_sandbox = True
    
    if len(sys.argv) >= 3:
        env = sys.argv[2].lower()
        use_sandbox = env != "production"
    
    # 测试指定环境
    result = test_api_key(access_token, use_sandbox)
    
    # 如果失败，尝试另一个环境
    if not result:
        print("\n尝试另一个环境...")
        test_api_key(access_token, not use_sandbox)

if __name__ == "__main__":
    main()
