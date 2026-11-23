import urllib.request
import sys
import os

url = "https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors"
BASE_DIR = os.environ.get("ASTRA_HOME") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dest = os.path.join(BASE_DIR, "ComfyUI", "models", "checkpoints", "v1-5-pruned-emaonly.safetensors")
os.makedirs(os.path.dirname(dest), exist_ok=True)

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d MB" % (
            percent, len(str(totalsize)), readsofar / 1e6, totalsize / 1e6)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

print("Downloading standard SD 1.5 Model (this is ~2GB, may take a few minutes)...")
try:
    urllib.request.urlretrieve(url, dest, reporthook)
    print("\nDownload complete! Model saved to:", dest)
except Exception as e:
    print(f"\nFailed to download: {e}")
    if os.path.exists(dest):
        os.remove(dest)
