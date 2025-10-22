#!/usr/bin/env python3
"""
Updated installation script for Voice-to-Law Assistant
Covers: audio processing, translation, scraping, ML models, LLM fine-tuning
"""

import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed: {package}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package}")

def main():
    print("🚀 Installing Full Project Dependencies (Audio + LLM + Scraping + Fine-tuning)")
    print("=" * 70)

    required_packages = [
        # Core Voice-to-Law dependencies
        "SpeechRecognition",
        "sounddevice",
        "scipy",
        "numpy",
        "deep-translator",

        # Scraping tools
        "requests",
        "beautifulsoup4",
        "tqdm",

        # Embeddings & Semantic Search
        "sentence-transformers",
        "faiss-cpu",

        # LLM & Fine-Tuning Stack
        "torch",
        "transformers",
        "datasets",
        "accelerate",
        "peft",
        "bitsandbytes",  # Optional for 4-bit/8-bit training

        # Optional for GUI / Audio extensions
        "pyaudio",
        "pocketsphinx"
    ]

    for pkg in required_packages:
        print(f"\n📦 Installing: {pkg}")
        install_package(pkg)

    print("\n✅ All installations attempted.")
    print("If you encounter issues, try the following:")
    print("- Upgrade pip: python -m pip install --upgrade pip")
    print("- On Windows: pip install pipwin && pipwin install pyaudio")
    print("- On Linux: sudo apt-get install portaudio19-dev")
    print("- On macOS: brew install portaudio")

if __name__ == "__main__":
    main()
