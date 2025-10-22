# translator/translator.py
# Updated to use deep-translator instead of googletrans

from deep_translator import GoogleTranslator

def translate_en_hi(text: str) -> str:
    """Translate English text to Hindi using Deep Translator"""
    try:
        if not text or not text.strip():
            return ""
        
        print(f"Translating EN->HI: {text}")
        translated = GoogleTranslator(source='en', target='hi').translate(text)
        print(f"Result: {translated}")
        return translated
    
    except Exception as e:
        print(f"Translation error (EN->HI): {e}")
        return f"[Translation failed] {text}"

def translate_hi_en(text: str) -> str:
    """Translate Hindi text to English using Deep Translator"""
    try:
        if not text or not text.strip():
            return ""
        
        print(f"Translating HI->EN: {text}")
        translated = GoogleTranslator(source='hi', target='en').translate(text)
        print(f"Result: {translated}")
        return translated
    
    except Exception as e:
        print(f"Translation error (HI->EN): {e}")
        return f"[Translation failed] {text}"

# Test the translation functions
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Testing Deep Translator...")
    print("="*50)

    # Test English to Hindi
    test_en = "Hello, how are you today?"
    print(f"\nTesting EN->HI:")
    print(f"Input: {test_en}")
    result_hi = translate_en_hi(test_en)
    print(f"Output: {result_hi}")

    # Test Hindi to English
    test_hi = "नमस्ते, आप कैसे हैं?"
    print(f"\nTesting HI->EN:")
    print(f"Input: {test_hi}")
    result_en = translate_hi_en(test_hi)
    print(f"Output: {result_en}")

    print("\n" + "="*50)
    print("Translation test completed!")
    print("="*50)
