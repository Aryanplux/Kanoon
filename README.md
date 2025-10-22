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

Kanoon is a desktop AI application designed specifically for legal professionals and students. It provides offline access to legal AI capabilities including document analysis, multi-language translation of legal texts, and intelligent legal research assistance.

###  Key Features

- ** Offline AI Assistant** - Powered by Mistral-7B model, works completely offline
- ** Legal Document Analysis** - Process and analyze legal documents, contracts, and case files
- ** Multi-language Translation** - Translate legal texts between English and regional languages
- ** Smart Legal Research** - Query legal databases and get contextual answers
- ** Natural Language Interface** - Ask legal questions in plain English
- ** Legal Database** - Built-in database of legal articles and precedents
- ** Voice Input Support** - Speak your legal queries (optional feature)

##  Installation

### Prerequisites
- **Windows 10/11** (64-bit)
- **Python 3.8+**
- **8GB+ RAM** (16GB recommended for optimal performance)
- **10GB+ free disk space** for AI models

Install Python Dependencies
pip install -r requirements.txt

Download AI Models
python setup_models.py

Initialize Legal Database
python create_sqlite_db.py

Launch Application
python main.py

Alternative Manual Model Setup
If automated download fails:

Visit Mistral-7B on Hugging Face

Download all files to models/mistral-7b/ folder

Ensure all .safetensors and configuration files are present
### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aryanplux/Kanoon.git
   cd Kanoon
