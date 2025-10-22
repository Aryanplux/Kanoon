from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    local_dir="models/mistral-7b",
    local_dir_use_symlinks=False
)
