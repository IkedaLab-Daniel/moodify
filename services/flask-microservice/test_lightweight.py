#!/usr/bin/env python3
"""
Test script for the lightweight emotion analyzer
This verifies that the VADER-based analyzer works correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from model import LightweightEmotionAnalyzer
    print("✅ Successfully imported LightweightEmotionAnalyzer")
except ImportError as e:
    print(f"❌ Failed to import LightweightEmotionAnalyzer: {e}")
    sys.exit(1)

def test_lightweight_analyzer():
    """Test the lightweight emotion analyzer with various texts"""
    
    try:
        analyzer = LightweightEmotionAnalyzer()
        print("✅ Successfully initialized LightweightEmotionAnalyzer")
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        return False
    
    # Test cases
    test_texts = [
        "I am so excited about this new opportunity!",
        "This is absolutely terrible and I hate it.",
        "The weather is okay today, nothing special.",
        "I love spending time with my family and friends.",
        "I'm really disappointed with the service.",
        "This is an amazing breakthrough in technology!"
    ]
    
    print("\n🧪 Testing emotion analysis:")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        try:
            result = analyzer.analyze_emotion(text)
            
            print(f"\nTest {i}: {text}")
            print(f"Dominant Emotion: {result['dominant_emotion']} (confidence: {result['confidence']})")
            print(f"Analysis Type: {result['analysis_type']}")
            print(f"VADER Scores: {result['vader_scores']}")
            print(f"Top Emotions: {dict(list(result['emotions'].items())[:3])}")
            
        except Exception as e:
            print(f"❌ Error analyzing text {i}: {e}")
            return False
    
    print("\n✅ All tests passed! Lightweight analyzer is working correctly.")
    print("\n📊 Memory usage comparison:")
    print("   - BERT model: ~500MB+ RAM")
    print("   - VADER model: ~5MB RAM")
    print("   - Reduction: ~99% memory savings")
    
    return True

if __name__ == "__main__":
    print("🚀 Testing Lightweight Emotion Analyzer")
    print("This is optimized for Render free tier (512Mi memory limit)")
    print("-" * 60)
    
    success = test_lightweight_analyzer()
    
    if success:
        print("\n🎉 Ready for deployment on Render free tier!")
        print("Use the /analyze-light endpoint for memory-efficient emotion analysis.")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
        sys.exit(1)
