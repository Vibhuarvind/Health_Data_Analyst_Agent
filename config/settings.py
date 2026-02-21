import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Primary high-performance model
GROQ_FALLBACK_MODELS = [
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "llama-3.2-11b-vision-preview"
]
TEMPERATURE = 0.1
MAX_TOKENS = 800

# Hugging Face Configuration (for deployment)
# Token should be stored in environment variable HF_TOKEN or GitHub Secrets
# Never commit tokens directly! Use: export HF_TOKEN=your_token_here
HF_TOKEN = os.getenv("HF_TOKEN")  # Load from environment
HF_SPACE_URL = "https://huggingface.co/spaces/VA6573/Nexus-Health-Analyst"
HF_USERNAME = "VA6573"
HF_SPACE_NAME = "Nexus-Health-Analyst"

# Data Paths
DATA_DIR = BASE_DIR / "data"
DATASET_1_PATH = DATA_DIR / "health_dataset_1.csv"
DATASET_2_PATH = DATA_DIR / "health_dataset_2.csv"

# Cache Configuration
CACHE_TTL = 3600  # 1 hour

# Safety Configuration
ALLOWED_IMPORTS = ["pandas", "numpy"]
BLOCKED_KEYWORDS = ["os.", "sys.", "subprocess.", "open(", "write(", "read(", "exec(", "eval("]
