"""
LibroChef Bot Starter
Starts both the bot and web server for the beautiful interface
"""

import subprocess
import threading
import time
import sys

def start_web_server():
    """Start the web server for the beautiful HTML interface"""
    print("🌐 Starting web server...")
    try:
        subprocess.run([sys.executable, "web_server.py"], check=True)
    except KeyboardInterrupt:
        print("🛑 Web server stopped")
    except Exception as e:
        print(f"❌ Web server error: {e}")

def start_bot():
    """Start the main bot"""
    print("🤖 Starting LibroChef bot...")
    try:
        subprocess.run([sys.executable, "bot.py"], check=True)
    except KeyboardInterrupt:
        print("🛑 Bot stopped")
    except Exception as e:
        print(f"❌ Bot error: {e}")

def main():
    """Start both services"""
    print("🚀 LibroChef Bot with Beautiful Interface")
    print("=" * 50)
    
    # Start web server in background thread
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    # Give web server time to start
    time.sleep(2)
    
    # Start bot in main thread
    try:
        start_bot()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down LibroChef Bot...")

if __name__ == "__main__":
    main()
