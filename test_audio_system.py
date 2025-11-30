"""Test script for the enhanced audio generation system"""
import os
import time
import streamlit as st
from audio_utils import (
    init_audio_cache, clean_audio_cache, get_cache_path,
    get_voice_config, validate_speed, clean_text_for_tts,
    is_internet_available, CACHE_DIR
)

def test_audio_system():
    """Run comprehensive tests of the audio system"""
    st.title("🎵 Audio System Test Suite")
    
    # Test 1: Cache System
    st.header("1. Audio Cache System")
    init_audio_cache()
    cache_before = len(list(CACHE_DIR.glob("*.mp3")))
    st.info(f"Initial cache size: {cache_before} cached files")
    
    # Test text samples in different languages
    test_samples = [
        ("Hello, this is a test of the audio system.", "English"),
        ("Bonjour, ceci est un test du système audio.", "French"),
        ("Hola, esta es una prueba del sistema de audio.", "Spanish"),
        ("こんにちは、オーディオシステムのテストです。", "Japanese")
    ]
    
    # Test 2: Voice Configurations
    st.header("2. Voice Configurations")
    for voice_type in ["male_1", "male_2", "female_1", "female_2", "neutral"]:
        config = get_voice_config(voice_type)
        st.write(f"**{voice_type}**: {config['description']} (TLD: {config['tld']})")
    
    # Test 3: Text Processing
    st.header("3. Text Processing")
    markdown_text = "**Bold** and *italic* test with # headers"
    clean = clean_text_for_tts(markdown_text)
    st.write(f"Original: {markdown_text}")
    st.write(f"Cleaned: {clean}")
    
    # Test 4: Speed Validation
    st.header("4. Speed Validation")
    test_speeds = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5]
    for speed in test_speeds:
        valid_speed = validate_speed(speed, "neutral")
        st.write(f"Input speed: {speed} → Validated: {valid_speed}")
    
    # Test 5: Audio Generation
    st.header("5. Audio Generation Test")
    if is_internet_available():
        st.success("✅ Internet connection available")
        for text, lang in test_samples:
            st.subheader(f"{lang} Test")
            st.write(text)
            
            # Try all three methods
            try:
                from app import create_musical_poetry_audio
                audio_file = create_musical_poetry_audio(
                    text=text,
                    language=lang,
                    speed=1.0,
                    theme="neutral",
                    audio_effects="enhance",
                    bg_volume_percent=40,
                    voice_type="neutral"
                )
                if audio_file and os.path.exists(audio_file):
                    st.success("✅ Musical audio generated")
                    st.audio(audio_file)
            except Exception as e:
                st.error(f"❌ Musical audio failed: {str(e)}")
            
            try:
                from app import create_audio_from_text
                audio_file = create_audio_from_text(
                    text=text,
                    language=lang,
                    speed=1.0,
                    voice_type="neutral"
                )
                if audio_file and os.path.exists(audio_file):
                    st.success("✅ Simple audio generated")
                    st.audio(audio_file)
            except Exception as e:
                st.error(f"❌ Simple audio failed: {str(e)}")
            
            try:
                from app import render_browser_tts
                st.info("Testing browser TTS:")
                render_browser_tts(text, lang)
            except Exception as e:
                st.error(f"❌ Browser TTS failed: {str(e)}")
    else:
        st.error("❌ No internet connection available")
    
    # Test 6: Cache Cleanup
    st.header("6. Cache Cleanup")
    clean_audio_cache()
    cache_after = len(list(CACHE_DIR.glob("*.mp3")))
    st.info(f"Cache size after cleanup: {cache_after} cached files")

if __name__ == "__main__":
    test_audio_system()