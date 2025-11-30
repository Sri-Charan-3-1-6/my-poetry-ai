"""Utilities for audio synthesis and management"""
import os
import time
import tempfile
import hashlib
import warnings
import streamlit as st
from pathlib import Path
from typing import Optional, Dict, Any

# Constants for audio cache
CACHE_DIR = Path(tempfile.gettempdir()) / "poetry_ai_audio_cache"
CACHE_MAX_AGE = 60 * 60 * 24  # 24 hours in seconds

# Voice profiles with richer configuration
VOICE_PROFILES = {
    "male_1": {
        "tld": "com",
        "description": "Professional Male Voice",
        "pitch_adjust": 0.95,  # Slightly lower pitch
        "speed_range": (0.8, 1.5)
    },
    "male_2": {
        "tld": "co.uk", 
        "description": "British Male Voice",
        "pitch_adjust": 0.9,  # Lower pitch
        "speed_range": (0.8, 1.5)
    },
    "female_1": {
        "tld": "com.au",
        "description": "Australian Female Voice",
        "pitch_adjust": 1.05,  # Slightly higher pitch
        "speed_range": (0.8, 1.5)
    },
    "female_2": {
        "tld": "ca",
        "description": "Canadian Female Voice",
        "pitch_adjust": 1.1,  # Higher pitch
        "speed_range": (0.8, 1.5)
    },
    "neutral": {
        "tld": "com",
        "description": "Neutral Voice",
        "pitch_adjust": 1.0,  # No pitch adjustment
        "speed_range": (0.5, 2.0)
    }
}

def init_audio_cache():
    """Initialize the audio cache directory"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
def clean_audio_cache():
    """Remove old cache files"""
    if not CACHE_DIR.exists():
        return
        
    current_time = time.time()
    for cache_file in CACHE_DIR.glob("*.mp3"):
        if current_time - cache_file.stat().st_mtime > CACHE_MAX_AGE:
            try:
                cache_file.unlink()
            except Exception as e:
                warnings.warn(f"Failed to remove cache file {cache_file}: {e}")

def get_cache_path(text: str, lang_code: str, speed: float, voice_type: str) -> Path:
    """Generate a cache file path based on input parameters"""
    # Create a unique hash of the input parameters
    params = f"{text}{lang_code}{speed}{voice_type}".encode('utf-8')
    file_hash = hashlib.md5(params).hexdigest()
    return CACHE_DIR / f"{file_hash}.mp3"

def get_voice_config(voice_type: str) -> Dict[str, Any]:
    """Get voice configuration with fallback to neutral"""
    return VOICE_PROFILES.get(voice_type, VOICE_PROFILES["neutral"])

def validate_speed(speed: float, voice_type: str) -> float:
    """Validate and adjust speed based on voice profile"""
    profile = get_voice_config(voice_type)
    min_speed, max_speed = profile["speed_range"]
    return max(min_speed, min(speed, max_speed))

def clean_text_for_tts(text: str) -> str:
    """Clean text for TTS processing"""
    # Remove markdown formatting
    clean = text.replace("*", "").replace("#", "").replace("**", "")
    
    # Add pauses for better flow
    clean = clean.replace("\n\n", ". ").replace("\n", ". ")
    
    # Normalize spacing
    clean = " ".join(clean.split())
    
    return clean.strip()

def is_internet_available() -> bool:
    """Check if internet connection is available"""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False