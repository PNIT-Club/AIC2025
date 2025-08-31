import torch

from .faiss_impl import FaissSearch
import os
import torch
# ====== Cấu hình ======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root/
index_file = os.path.join(BASE_DIR, "..", "res", "my_index.faiss")
metadata_file = os.path.join(BASE_DIR, "..", "res", "metadata.json")

class FaissSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("Initializing FaissSingleton...")
        # Initialization logic here (called only once for the first instance)
        self._instance = FaissSearch(
            index_file,
            metadata_file,
            "cuda" if torch.cuda.is_available() else "cpu")
        pass

    def get_instance(self):
        return self._instance