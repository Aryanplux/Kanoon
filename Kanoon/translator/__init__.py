# translator/__init__.py

"""
Voice-to-Law Assistant Translator Package

This package provides translation capabilities between English and Hindi,
audio transcription, and legal question processing functionality.
"""

# Import main functions to make them available at package level
try:
    from .translator import translate_en_hi, translate_hi_en
    from .audio_utils import transcribe_audio
    from .legal_llm import ask_legal_llm
    from .ui import VoiceLawAssistant, select_language
    
    print("Translator package loaded successfully!")
    
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")
    print("This might be due to missing dependencies. Please check your installation.")

# Package metadata
__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Voice-to-Law Assistant with Hindi-English Translation"

# Make key functions available at package level
__all__ = [
    'translate_en_hi',
    'translate_hi_en', 
    'transcribe_audio',
    'ask_legal_llm',
    'VoiceLawAssistant',
    'select_language'
]