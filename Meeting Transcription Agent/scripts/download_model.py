import os
from huggingface_hub import hf_hub_download

# where to store
models_dir = os.path.join(os.getcwd(), "backend", "models")
os.makedirs(models_dir, exist_ok=True)

# download the GGUF
local_path = hf_hub_download(
    repo_id="TheBloke/Llama-2-13B-Chat-GGUF",
    filename="llama-2-13b-chat.Q2_K.gguf",
    local_dir=models_dir
)

# rename to match our code
dst = os.path.join(models_dir, "llama-2-13b-chat-32k.gguf")
os.replace(local_path, dst)
print("Model downloaded to", dst)
