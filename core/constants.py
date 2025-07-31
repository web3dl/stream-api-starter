import os
from dotenv import load_dotenv

load_dotenv()

WEB3DL_STREAM_API_URL = "https://api.web3dl.com/stream"
DATA_DIR = "./data"

WEB3DL_API_KEY = os.environ.get("WEB3DL_API_KEY")
if not WEB3DL_API_KEY:
    raise RuntimeError("WEB3DL_API_KEY environment variable not set.")
