from huggingface_hub import snapshot_download
import os

# Define your Hugging Face repo ID for Mistral-7B-Instruct
REPO_ID = "mistralai/Mistral-7B-Instruct-v0.1"

# Define the directory to download the model into
TARGET_DIR = os.path.join(os.getcwd(), "mistral_model")
print("~13GB...")

snapshot_download(
    repo_id=REPO_ID,
    local_dir=TARGET_DIR,
    local_dir_use_symlinks=False,  # Ensures compatibility on Windows
    revision="main"
)

print(f"✅ Model downloaded to: {TARGET_DIR}")
