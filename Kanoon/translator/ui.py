# translator/ui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

# Import functions with correct spelling and error handling
try:
    from .audio_utils import transcribe_audio, list_audio_devices
    from .translator import translate_en_hi, translate_hi_en
    from .legal_llm import ask_legal_llm
    print("All UI imports successful!")
except ImportError as e:
    print(f"Import error in UI: {e}")
    def transcribe_audio(duration=5, device_index=None): return "[Audio unavailable]"
    def list_audio_devices(): return []
    def translate_en_hi(text): return text
    def translate_hi_en(text): return text
    def ask_legal_llm(text): return "Legal assistant unavailable"

class VoiceLawAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kanoon")
        self.root.geometry("800x600")
        
        self.language_var = tk.StringVar(value="English")
        self.is_processing = False
        
        self.setup_ui()
        
        # Show available audio devices on startup
        self.show_audio_devices()
    
    def show_audio_devices(self):
        """Show available audio devices for debugging"""
        try:
            devices = list_audio_devices()
            print(f"Found {len(devices)} audio devices")
            for device in devices[:5]:
                print(f"Device {device.get('index', 'Unknown')}: {device.get('name', 'Unknown')}")
        except Exception as e:
            print(f"Could not list audio devices: {e}")
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Language selection
        self.lang_frame = ttk.LabelFrame(main_frame, text="Select Input Language", padding="10")
        self.lang_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(self.lang_frame, text="English", variable=self.language_var, value="English", command=self.change_language).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(self.lang_frame, text="Hindi", variable=self.language_var, value="Hindi", command=self.change_language).pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        self.speak_button = ttk.Button(button_frame, text="🎤 Record Audio", command=self.handle_voice_input)
        self.speak_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_output)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.test_audio_button = ttk.Button(button_frame, text="Test Audio", command=self.test_audio_system)
        self.test_audio_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to assist with legal questions")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Manual input
        self.input_frame = ttk.LabelFrame(main_frame, text="Or Type Your Question", padding="10")
        self.input_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.input_text = tk.Text(self.input_frame, height=3, width=80)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        self.submit_button = ttk.Button(self.input_frame, text="Submit Question", command=self.handle_text_input)
        self.submit_button.pack(pady=(10, 0))
        
        # Output
        self.output_frame = ttk.LabelFrame(main_frame, text="Response", padding="10")
        self.output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=15, width=80, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
    
    def change_language(self):
        """Switch UI language dynamically"""
        lang = self.language_var.get()
        
        if lang == "Hindi":
            self.root.title("क़ानून")
            self.lang_frame.config(text="भाषा चुनें")
            self.speak_button.config(text="🎤 ऑडियो रिकॉर्ड करें")
            self.clear_button.config(text="साफ करें")
            self.test_audio_button.config(text="ऑडियो जांचें")
            self.status_label.config(text="कानूनी प्रश्नों में मदद करने के लिए तैयार")
            self.input_frame.config(text="या अपना प्रश्न टाइप करें")
            self.submit_button.config(text="प्रश्न सबमिट करें")
            self.output_frame.config(text="उत्तर")
        else:
            self.root.title("Kanoon")
            self.lang_frame.config(text="Select Language")
            self.speak_button.config(text="🎤 Record Audio")
            self.clear_button.config(text="Clear")
            self.test_audio_button.config(text="Test Audio")
            self.status_label.config(text="Ready to assist with legal questions")
            self.input_frame.config(text="Or Type Your Question")
            self.submit_button.config(text="Submit Question")
            self.output_frame.config(text="Response")
    
    def test_audio_system(self):
        if self.is_processing:
            return
        
        def test_audio():
            try:
                self.is_processing = True
                self.status_label.config(text="Testing audio system...")
                self.root.update()
                
                for device_idx in [None, 5, 0, 1]:
                    try:
                        self.status_label.config(text=f"Testing device {device_idx}... Speak now!")
                        self.root.update()
                        
                        text = transcribe_audio(duration=3, device_index=device_idx)
                        print(f"Device {device_idx} result: {text}")
                        
                        if text and not text.startswith("["):
                            self.output_text.insert(tk.END, f"✅ Device {device_idx} works: {text}\n")
                            self.status_label.config(text=f"Audio test successful with device {device_idx}")
                            break
                        else:
                            self.output_text.insert(tk.END, f"❌ Device {device_idx}: {text}\n")
                            
                    except Exception as e:
                        self.output_text.insert(tk.END, f"❌ Device {device_idx} error: {e}\n")
                        continue
                        
                self.output_text.see(tk.END)
                
            except Exception as e:
                self.output_text.insert(tk.END, f"Audio test failed: {e}\n")
            finally:
                self.is_processing = False
                self.root.update()
        
        thread = threading.Thread(target=test_audio)
        thread.daemon = True
        thread.start()
    
    def handle_voice_input(self):
        if self.is_processing:
            return
        
        def process_voice():
            try:
                self.is_processing = True
                self.speak_button.config(state='disabled', text="Recording..." if self.language_var.get() == "English" else "रिकॉर्डिंग...")
                self.status_label.config(text="Listening... Speak now!" if self.language_var.get() == "English" else "सुन रहे हैं... बोलें!")
                self.root.update()
                
                text = None
                for device_idx in [5, None, 0, 1, 2]:
                    try:
                        text = transcribe_audio(duration=5, device_index=device_idx)
                        
                        if text and text.strip() and not text.startswith("["):
                            break
                        else:
                            continue
                    except Exception:
                        continue

                if text and text.strip() and not text.startswith("["):
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", text)
                    self.status_label.config(text="Speech transcribed! Click 'Submit Question'" if self.language_var.get() == "English" else "भाषण ट्रांसक्राइब! 'प्रश्न सबमिट करें' दबाएं")
                else:
                    self.status_label.config(text="No speech detected." if self.language_var.get() == "English" else "कोई आवाज़ नहीं मिली।")
                    
            finally:
                self.is_processing = False
                self.speak_button.config(state='normal', text="🎤 Record Audio" if self.language_var.get() == "English" else "🎤 ऑडियो रिकॉर्ड करें")
                self.root.update()
        
        thread = threading.Thread(target=process_voice)
        thread.daemon = True
        thread.start()
    
    def handle_text_input(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            self.process_question(text)
        else:
            messagebox.showwarning("Warning" if self.language_var.get() == "English" else "चेतावनी", "Please enter a question." if self.language_var.get() == "English" else "कृपया प्रश्न दर्ज करें।")
    
    def process_question(self, text):
        try:
            self.status_label.config(text="Processing your question..." if self.language_var.get() == "English" else "आपका प्रश्न संसाधित हो रहा है...")
            self.root.update()
            
            source_lang = self.language_var.get()
            self.output_text.insert(tk.END, f"Question ({source_lang}): {text}\n\n")
            
            if source_lang == "Hindi":
                translated = translate_hi_en(text)
                answer = ask_legal_llm(translated)
                final_output = translate_en_hi(answer)
                self.output_text.insert(tk.END, f"Response (Hindi): {final_output}\n\n")
                self.output_text.insert(tk.END, f"Response (English): {answer}\n\n")
            else:
                final_output = ask_legal_llm(text)
                self.output_text.insert(tk.END, f"Response: {final_output}\n\n")
            
            self.output_text.insert(tk.END, "-" * 80 + "\n\n")
            self.output_text.see(tk.END)
            self.status_label.config(text="Response ready!" if self.language_var.get() == "English" else "उत्तर तैयार!")
            
            self.input_text.delete("1.0", tk.END)
            
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n\n")
            self.status_label.config(text="Error occurred" if self.language_var.get() == "English" else "त्रुटि हुई")
    
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.input_text.delete("1.0", tk.END)
        self.status_label.config(text="Ready to assist with legal questions" if self.language_var.get() == "English" else "कानूनी प्रश्नों में मदद करने के लिए तैयार")
    
    def run(self):
        self.root.mainloop()

def select_language():
    app = VoiceLawAssistant()
    app.run()

if __name__ == "__main__":
    select_language()
