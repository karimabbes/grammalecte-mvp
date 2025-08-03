#!/usr/bin/env python3
"""
Demo script for the Grammalecte FastAPI API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def demo_health_check():
    """Demo the health check endpoint"""
    print("🔍 Health Check")
    print("-" * 40)
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"📊 Version: {data['version']}")
        print(f"🌍 Language: {data['lang']}")
    else:
        print(f"❌ Error: {response.status_code}")
    print()

def demo_text_checking():
    """Demo the text checking functionality"""
    print("📝 Text Checking")
    print("-" * 40)
    
    test_texts = [
        "Bonjour, comment allez-tu?",
        "Je vais au magasin pour acheter du pain.",
        "Il fait beaux aujourd'hui.",
        "Je suis allé au cinéma hier."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"Text {i}: {text}")
        response = requests.post(f"{BASE_URL}/check", json={"text": text})
        print(response.json())
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                print(f"  ❌ Found {len(data['data'])} error(s):")
                for error in data['data']:
                    print(f"    - {error['message']}")
                    if error['suggestions']:
                        print(f"      Suggestions: {', '.join(error['suggestions'])}")
            else:
                print("  ✅ No errors found")
        else:
            print(f"  ❌ Error: {response.status_code}")
        print()

def demo_suggestions():
    """Demo the spelling suggestions"""
    print("💡 Spelling Suggestions")
    print("-" * 40)
    
    test_words = ["bonjour", "magasin", "cinéma", "aujourd'hui"]
    
    for word in test_words:
        print(f"Word: {word}")
        response = requests.get(f"{BASE_URL}/suggest/{word}")
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get('suggestions', [])
            if suggestions:
                print(f"  Suggestions: {', '.join(suggestions)}")
            else:
                print("  No suggestions available")
        else:
            print(f"  ❌ Error: {response.status_code}")
        print()

def demo_options():
    """Demo the options endpoint"""
    print("⚙️ Grammar Checking Options")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/options")
    
    if response.status_code == 200:
        data = response.json()
        options = data.get('options', {})
        
        print("Available options:")
        for option, value in options.items():
            status = "✅" if value else "❌"
            print(f"  {status} {option}: {value}")
    else:
        print(f"❌ Error: {response.status_code}")
    print()

def main():
    """Run all demos"""
    print("🚀 Grammalecte FastAPI Demo")
    print("=" * 50)
    print()
    
    try:
        demo_health_check()
        demo_text_checking()
        demo_suggestions()
        demo_options()
        
        print("🎉 Demo completed successfully!")
        print("\n📚 API Documentation available at:")
        print(f"   Swagger UI: {BASE_URL}/docs")
        print(f"   ReDoc: {BASE_URL}/redoc")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the server is running with:")
        print("python run.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 