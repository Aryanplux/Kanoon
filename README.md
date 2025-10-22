#  Kanoon - Law AI Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Development-yellow.svg)
![Offline](https://img.shields.io/badge/💯-Offline_Capable-green.svg)

**An intelligent offline legal assistant that helps with legal document analysis, translation, and research using Mistral AI**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [Support](#-support)

</div>

---

##  Overview

Kanoon is a desktop AI application designed for legal professionals and law students.  
It provides **offline** access to AI capabilities like document analysis, multilingual translation, and intelligent legal research assistance—all powered by the **Mistral-7B model**.

---

##  Features

- ** Offline AI Assistant** – Works completely offline, powered by Mistral-7B
- ** Legal Document Analysis** – Processes and analyzes legal files (PDF/DOCX/TXT)
- ** Multi-language Translation** – Accurately translates legal content
- ** Smart Legal Research** – Context-based answers from legal datasets
- ** Natural Language Interface** – Query using plain English
- ** Legal Database** – Built-in repository of legal articles and case precedents
- ** Voice Input Support** – Optional voice recognition for queries

---

##  Quick Start

### Prerequisites

- **Windows 10/11** (64-bit)
- **Python 3.8+**
- **8GB+ RAM** (16GB recommended)
- **10GB+ free disk space**

---

### Installation

1. **Clone the repository**
git clone https://github.com/Aryanplux/Kanoon.git
cd Kanoon

text

2. **Install dependencies**
pip install -r requirements.txt

text

3. **Download AI models**
python setup_models.py

text

4. **Initialize the database**
python create_sqlite_db.py

text

5. **Launch the app**
python main.py

text

---

##  Usage

### Starting the Application
python main.py

text

### Example Queries

- "What are the requirements for a valid contract in Indian law?"
- "Explain the difference between murder and culpable homicide"
- "Summarize the key points of the Consumer Protection Act"
- "Translate this legal clause to Hindi"

---

##  Features Overview

### Legal Query Interface
- Type natural-language legal questions  
- Get detailed answers with citations  
- Context-aware, intelligent responses  

### Document Analysis
- Upload **PDF, DOCX, or TXT** files  
- Automatic summarization and key-point extraction  
- Legal implication and term analysis  

### Translation Module
- Translate legal text between English and Indian languages  
- Maintains correct legal terminology and formatting  

---

##  Project Structure

Kanoon/
├── models/mistral-7b/ # AI Model files
├── data/ # Legal databases
│ ├── legal_docs.db # SQLite database
│ ├── law_articles.csv # Legal corpus
│ └── embeddings.npy # Document embeddings
├── translator/ # Translation modules
│ ├── translator.py # Translation engine
│ └── audio_utils.py # Voice processing
├── ingest/ # Data processing
│ ├── build_embeddings.py # Vector embeddings
│ └── utils_parse.py # Document parser
├── main.py # Main application entrypoint
├── create_sqlite_db.py # Database setup
├── setup_models.py # Model downloader
├── requirements.txt # Dependencies
└── README.md # Documentation

text

---

##  Technical Details

### AI Architecture
- **Base Model:** Mistral-7B-Instruct-v0.1  
- **Embeddings:** FAISS vector database  
- **Retrieval System:** Retrieval-Augmented Generation (RAG)  
- **Operation:** Fully offline  

### Supported Formats
- **Documents:** PDF, DOCX, TXT  
- **Audio:** WAV, MP3  
- **Databases:** SQLite, CSV, JSON  

---

##  FAQ

**Q:** Why is the first setup slow?  
**A:** The first setup builds vector embeddings for the legal database.  

**Q:** Can I add my own legal documents?  
**A:** Yes! Place them in the `data/` folder and run:
python ingest/build_embeddings.py

text

**Q:** How do I update the legal database?  
**A:** Edit `data/law_articles.csv` and run:
python create_sqlite_db.py

text

---

##  Troubleshooting

### Model Loading Issues
- Ensure all model files are in `models/mistral-7b/`
- Verify system RAM (minimum 8GB required)

### Database Errors
python create_sqlite_db.py

text

### Performance Tips
- Close memory-intensive applications  
- 16GB RAM recommended for smooth operation  

---

##  Contributing

We welcome all contributions!  
**Areas for improvement:**
- Additional legal datasets  
- More Indian languages  
- UI/UX enhancements  
- Model performance optimizations  

---

##  License

Licensed under the **MIT License** — See the `LICENSE` file for details.

---

##  Disclaimer

Kanoon is an AI legal assistant tool and **must not** be treated as professional legal advice.  
Always consult certified legal professionals for formal legal matters.

---

<div align="center">

Built with ❤️ for the legal community  
**Making legal AI accessible to everyone, everywhere**

</div>

---

##  requirements.txt

torch>=2.0.0
transformers>=4.30.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
langchain>=0.0.200
accelerate>=0.20.0
huggingface-hub>=0.15.0
python-docx>=0.8.11
PyPDF2>=3.0.0
sqlite3
numpy>=1.21.0
sounddevice>=0.4.0
speechrecognition>=3.8.0
pygame>=2.0.0

text

---

##  setup_models.py

#!/usr/bin/env python3
"""
Script to download Mistral-7B model for Kanoon Law AI Assistant
"""

import os
import sys
from huggingface_hub import snapshot_download

def download_model():
print("🏛️ Kanoon - Model Downloader")
print("=" * 40)

text
# Create models directory
os.makedirs("models/mistral-7b", exist_ok=True)

print("Downloading Mistral-7B model...")
print("This may take 30-60 minutes depending on your internet connection")
print("Required space: ~13GB")
print()

try:
    # Download model from Hugging Face
    snapshot_download(
        repo_id="mistralai/Mistral-7B-Instruct-v0.1",
        local_dir="models/mistral-7b",
        local_dir_use_symlinks=False,
        resume_download=True
    )
    print("Model downloaded successfully!")
    print("Setup complete! Run: python main.py")
    
except Exception as e:
    print(f"Error downloading model: {e}")
    print("\nAlternative manual setup:")
    print("1. Visit: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1")
    print("2. Download all files to 'models/mistral-7b/' folder")
    print("3. Ensure all .safetensors files are present")
if name == "main":
download_model()

text

---

##  .gitignore

Models
models/
mistral_model/

Virtual environment
.venv/
venv/
env/

Python cache
pycache/
*.py[cod]
*$py.class

Database
*.db
*.sqlite3

Large data files
*.npy
*.npz
*.index

Logs
*.log
logs/

OS
.DS_Store
Thumbs.db

IDE
.vscode/
.idea/
*.swp
*.swo

Audio files
*.wav
*.mp3

text

---
