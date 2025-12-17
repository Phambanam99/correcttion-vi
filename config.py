# -*- coding: utf-8 -*-
"""
Configuration for Vietnamese Text Corrector
"""

# ===== QWEN MODELS (Local) =====
QWEN_MODELS = {
    "qwen2.5-7b": "Qwen/Qwen2.5-7B-Instruct",
    "qwen3-8b": "Qwen/Qwen3-8B",
}
DEFAULT_QWEN_MODEL = "qwen2.5-7b"

# ===== OLLAMA ONLINE =====
# Models are fetched dynamically from the API
OLLAMA_API_URL = "https://api.devhunter9x.qzz.io"
DEFAULT_OLLAMA_MODEL = "qwen2.5:7b"

# ===== MODEL GENERATION PARAMETERS =====
MAX_NEW_TOKENS = 1024
TEMPERATURE = 0.1
TOP_P = 0.9

# ===== PIPELINE STRATEGIES =====
# Local pipelines:
# - qwen_protonx: Qwen (local) + ProtonX
# - qwen_only: Qwen only (local, no ProtonX)
# - protonx_only: ProtonX only
# - bartpho_protonx: BartPho + ProtonX
# Online pipelines:
# - ollama_protonx: Ollama (online) + ProtonX
# - ollama_only: Ollama only (online, no ProtonX)
PIPELINE_STRATEGIES = [
    "qwen_protonx",
    "qwen_only", 
    "protonx_only",
    "bartpho_protonx",
    "ollama_protonx",
    "ollama_only"
]
DEFAULT_PIPELINE = "qwen_protonx"

# ===== MISC =====
AUTHOR_NAME = "AI Vietnamese Proofreader"

# ===== QUEUE SETTINGS (for concurrent users) =====
MAX_QUEUE_SIZE = 50          # Maximum pending jobs
WORKER_THREADS = 1           # GPU can only process 1 at a time
JOB_TIMEOUT_SECONDS = 300    # 5 minutes timeout per job
JOB_CLEANUP_HOURS = 1        # Clean up completed jobs after 1 hour
