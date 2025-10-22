import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import whisper

print("🎙 Checking input devices:")
try:
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            print(f"{i}: {d['name']} (input)")
except Exception as e:
    print(f"❌ Could not query devices: {e}")
    exit()

try:
    device_index = int(input("👉 Enter device index to record (e.g., 5 or 14): ").strip())
    sd.default.device = device_index
except Exception as e:
    print(f"❌ Invalid device: {e}")
    exit()

samplerate = 16000
duration = 5

print(f"\n🎤 Recording {duration} seconds using device {device_index}...")
try:
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
    sd.wait()
except Exception as e:
    print(f"❌ Recording failed: {e}")
    exit()

print("✅ Recording done. Saving...")
filename = "test_audio.wav"
recording_int = (recording * 32767).astype(np.int16)
wav.write(filename, samplerate, recording_int)

print("🔍 Transcribing using Whisper...")
try:
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print(f"\n📝 Transcribed text:\n{result['text'].strip()}")
except Exception as e:
    print(f"❌ Whisper failed: {e}")
