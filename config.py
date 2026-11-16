
import os
from pathlib import Path
from dotenv import load_dotenv

# Main project folder
BASE_DIR = Path(__file__).resolve().parent

# Load API key
load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

# Project folders
PDF_FOLDER = BASE_DIR / "pdfs"
FAISS_FOLDER = BASE_DIR / "farmer_faiss_index"
ASSET_FOLDER = BASE_DIR / "assets"

# Create folders automatically
PDF_FOLDER.mkdir(exist_ok=True)
FAISS_FOLDER.mkdir(exist_ok=True)
ASSET_FOLDER.mkdir(exist_ok=True)

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# AI models
LLM_MODEL = "gpt-4o-mini"

# Multilingual model for Tamil and English
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# RAG settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4

# Application name
APP_NAME = "Namma Vivasayam"

# Banner image
BANNER_IMAGE = ASSET_FOLDER / "farmer_banner.png"
