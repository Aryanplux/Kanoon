# translator/audio_utils.py
import sys
import warnings
from typing import Optional

# Dependency checking and imports
try:
    import sounddevice as sd
except ImportError:
    print("❌ sounddevice not found. Install with: pip install sounddevice")
    sd = None

try:
    import numpy as np
except ImportError:
    print("❌ numpy not found. Install with: pip install numpy")
    np = None

try:
    import scipy.io.wavfile as wav
except ImportError:
    print("❌ scipy not found. Install with: pip install scipy")
    wav = None

try:
    import speech_recognition as sr
except ImportError:
    print("❌ speech_recognition not found. Install with: pip install SpeechRecognition")
    sr = None

import tempfile
import os

def transcribe_audio(duration=5, samplerate=16000, device_index=None):
    """
    Record audio and convert it to text using SpeechRecognition.
    This is the main function that your UI expects.
    
    Args:
        duration (int): Recording duration in seconds
        samplerate (int): Sample rate for recording
        device_index (int, optional): Audio device index to use
        
    Returns:
        str: Transcribed text or error message
    """
    # Check if required modules are available
    if not all([sd, np, wav, sr]):
        return "[Audio modules not available - please install dependencies]"
    
    recognizer = sr.Recognizer()
    
    try:
        print(f"🎙 Recording {duration}s of audio{' using device ' + str(device_index) if device_index else ''}...")
        
        if device_index is not None:
            sd.default.device = device_index
        
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
        sd.wait()
        
        audio_data = (recording * 32767).astype(np.int16)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav.write(f.name, samplerate, audio_data)
            audio_path = f.name
        
        print("🔍 Transcribing audio...")
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        
        os.unlink(audio_path)
        
        # Try using Google Web Speech API (free tier)
        text = recognizer.recognize_google(audio, language="en-IN")
        return text.strip()
        
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError as e:
        return f"[STT API error: {e}]"
    except Exception as e:
        return f"[Audio transcription failed: {e}]"

def list_audio_devices():
    """List available audio devices"""
    if not sd:
        print("❌ sounddevice not available")
        return []
    
    try:
        print("🎧 Available audio devices:")
        devices = []
        for i, dev in enumerate(sd.query_devices()):
            roles = []
            if dev["max_input_channels"] > 0:
                roles.append("input")
            if dev["max_output_channels"] > 0:
                roles.append("output")
            print(f"{i}: {dev['name']} ({', '.join(roles)})")
            devices.append({
                'index': i,
                'name': dev['name'],
                'roles': roles
            })
        return devices
    except Exception as e:
        print(f"❌ Error listing devices: {e}")
        return []

class SpeechToTextLibrary:
    """
    A comprehensive Speech-to-Text library for real-time audio transcription.
    Compatible with the UI system.
    """
    
    def __init__(self, default_samplerate: int = 16000, default_duration: float = 5.0):
        """Initialize the Speech-to-Text library."""
        self.default_samplerate = default_samplerate
        self.default_duration = default_duration
        
        if sr:
            self.recognizer = sr.Recognizer()
            # Configure recognizer settings for better accuracy
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
        else:
            self.recognizer = None
    
    def record_audio(self, duration: Optional[float] = None, 
                    samplerate: Optional[int] = None, 
                    device_index: Optional[int] = None):
        """Record audio from the microphone."""
        if not all([sd, np]):
            raise Exception("Audio recording not available - missing dependencies")
        
        duration = duration or self.default_duration
        samplerate = samplerate or self.default_samplerate
        
        if device_index is not None:
            sd.default.device = device_index
        
        recording = sd.rec(int(duration * samplerate), 
                         samplerate=samplerate, 
                         channels=1, 
                         dtype=np.float32)
        sd.wait()
        
        # Convert to 16-bit integer format
        audio_data = (recording * 32767).astype(np.int16)
        return audio_data
    
    def transcribe_audio_data(self, audio_data, samplerate: int, 
                            language: str = "en-IN", 
                            engine: str = "google") -> str:
        """Transcribe audio data to text."""
        if not all([wav, sr]):
            return "[Transcription not available - missing dependencies]"
        
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                wav.write(f.name, samplerate, audio_data)
                audio_path = f.name
            
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.record(source)
            
            # Clean up temporary file
            os.unlink(audio_path)
            
            # Choose recognition engine
            if engine.lower() == "google":
                text = self.recognizer.recognize_google(audio, language=language)
            elif engine.lower() == "sphinx":
                text = self.recognizer.recognize_sphinx(audio)
            else:
                text = self.recognizer.recognize_google(audio, language=language)
            
            return text.strip()
            
        except sr.UnknownValueError:
            return "[Could not understand audio]"
        except sr.RequestError as e:
            return f"[STT API error: {e}]"
        except Exception as e:
            return f"[Audio transcription failed: {e}]"
    
    def transcribe_live(self, duration: Optional[float] = None, 
                       samplerate: Optional[int] = None, 
                       device_index: Optional[int] = None,
                       language: str = "en-IN",
                       engine: str = "google") -> str:
        """Record audio and convert it to text in one step."""
        try:
            # Use the standalone function for compatibility
            return transcribe_audio(
                duration=duration or self.default_duration,
                samplerate=samplerate or self.default_samplerate,
                device_index=device_index
            )
        except Exception as e:
            return f"[Live transcription failed: {e}]"

# Convenience functions for UI compatibility
def quick_transcribe(duration: float = 5, language: str = "en-IN", device_index=None) -> str:
    """Quick transcription function for UI use."""
    return transcribe_audio(duration=duration, device_index=device_index)

# Test function to check if everything works
def test_audio_system():
    """Test the audio system"""
    print("🧪 Testing audio system...")
    
    # Check dependencies
    missing = []
    if not sd: missing.append("sounddevice")
    if not np: missing.append("numpy")
    if not wav: missing.append("scipy")
    if not sr: missing.append("speech_recognition")
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("✅ All dependencies available")
    
    # List devices
    devices = list_audio_devices()
    
    if devices:
        print("✅ Audio devices found")
        return True
    else:
        print("⚠️  No audio devices found")
        return False

# Example usage
if __name__ == "__main__":
    # Test the system
    test_audio_system()
    
    # Quick test
    print("\n" + "="*50)
    print("Testing transcription...")
    result = transcribe_audio(duration=3)
    print(f"Result: {result}")