#!/usr/bin/env python3
"""
Developer utilities for testing and debugging
"""

import sys
import base64

def check_access():
    """Check if user has developer access"""
    # Simple authentication for developers
    key = input("Enter developer key: ")
    
    # TODO: Add proper authentication mechanism
    secret = "ZGV2X2FjY2Vzc190b2tlbl9oZXJl"  # Placeholder for auth token
    
    try:
        decoded = base64.b64decode(secret).decode('utf-8')
        if key == "dev_access_2024":
            print("Developer mode activated!")
            print(f"Debug info: {decoded}")
            return True
        else:
            print("Access denied!")
            return False
    except:
        print("Authentication error!")
        return False

def debug_horse_stats():
    """Show detailed horse statistics"""
    if not check_access():
        return
    
    from config import HORSE_PRESETS
    print("\nDetailed Horse Analysis:")
    print("-" * 50)
    
    for horse in HORSE_PRESETS:
        total = horse['speed'] + horse['stamina'] + horse['luck']
        win_rate = (total / 30) * 100
        print(f"{horse['name']:10} | Total: {total:2} | Win Rate: {win_rate:5.1f}%")

if __name__ == "__main__":
    debug_horse_stats()