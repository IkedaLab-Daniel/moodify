#!/usr/bin/env python3
"""
Test script to verify VADER installation and functionality
Run this to debug VADER installation issues
"""

print("🔍 Testing VADER Sentiment Installation")
print("=" * 50)

# Test 1: Try importing vaderSentiment
print("\n1. Testing vaderSentiment import...")
try:
    import vaderSentiment
    print(f"✅ vaderSentiment package found at: {vaderSentiment.__file__}")
    print(f"   Version: {getattr(vaderSentiment, '__version__', 'Unknown')}")
except ImportError as e:
    print(f"❌ Failed to import vaderSentiment: {e}")

# Test 2: Try importing the analyzer
print("\n2. Testing SentimentIntensityAnalyzer import...")
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    print("✅ SentimentIntensityAnalyzer imported successfully")
    
    # Test 3: Try creating analyzer instance
    print("\n3. Testing analyzer initialization...")
    analyzer = SentimentIntensityAnalyzer()
    print("✅ SentimentIntensityAnalyzer initialized successfully")
    
    # Test 4: Try analyzing text
    print("\n4. Testing text analysis...")
    test_text = "I love this amazing product!"
    scores = analyzer.polarity_scores(test_text)
    print(f"✅ Analysis successful!")
    print(f"   Text: '{test_text}'")
    print(f"   Scores: {scores}")
    
except ImportError as e:
    print(f"❌ Failed to import SentimentIntensityAnalyzer: {e}")
except Exception as e:
    print(f"❌ Error during analysis: {e}")

# Test 5: Test TextBlob fallback
print("\n5. Testing TextBlob fallback...")
try:
    from textblob import TextBlob
    blob = TextBlob("I love this amazing product!")
    polarity = blob.sentiment.polarity
    print(f"✅ TextBlob working! Polarity: {polarity}")
except ImportError as e:
    print(f"❌ TextBlob not available: {e}")

print("\n" + "=" * 50)
print("🎯 Installation Commands:")
print("pip install vaderSentiment==3.3.2")
print("pip install textblob==0.17.1")
print("\n📋 For Render deployment, ensure requirements-light.txt contains:")
print("vaderSentiment==3.3.2")
print("textblob==0.17.1")
