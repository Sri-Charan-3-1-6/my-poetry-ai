"""Test runner for multimodal poetry AI"""
import streamlit as st
import test_audio_system
import test_features

def run_tests():
    """Run the full test suite"""
    print("🧪 Poetry AI Test Suite")
    print("=" * 40)
    
    # Basic functionality tests
    print("\n1. Basic Functions")
    print("-" * 20)
    try:
        test_features.main()
    except Exception as e:
        print(f"❌ Basic function tests failed: {e}")
    
    # Audio system tests
    print("\n2. Audio System")
    print("-" * 20)
    try:
        test_audio_system.test_audio_system()
    except Exception as e:
        print(f"❌ Audio system tests failed: {e}")
    
    print("\n✅ Test suite complete!")
    return