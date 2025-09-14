#!/usr/bin/env python3
"""
LibroChef Bot Conflict Resolver
Helps resolve HTTP 409 conflicts and ensures clean bot startup
"""

import requests
import sys
from constants.variables import TOKEN

def clear_webhook():
    """Clear any existing webhook"""
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("✅ Webhook cleared successfully")
            return True
        else:
            print(f"⚠️ Warning: Could not clear webhook: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error clearing webhook: {e}")
        return False

def get_bot_info():
    """Get bot information"""
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                print(f"✅ Bot connected: @{bot_info['result']['username']}")
                return True
        print(f"❌ Bot connection failed: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")
        return False

def main():
    print("🔧 LibroChef Bot Conflict Resolver")
    print("=" * 40)
    
    print("1. Checking bot connection...")
    if not get_bot_info():
        print("❌ Cannot connect to bot. Check your TOKEN.")
        sys.exit(1)
    
    print("2. Clearing webhook...")
    clear_webhook()
    
    print("3. Conflict resolution complete!")
    print("\n🚀 Now you can start the bot with: python bot.py")
    print("\n💡 Tips to avoid conflicts:")
    print("- Only run one instance of the bot at a time")
    print("- Always stop the bot with Ctrl+C before restarting")
    print("- If you see 409 errors, run this script again")

if __name__ == "__main__":
    main()
