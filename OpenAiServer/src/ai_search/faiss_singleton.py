import torch

from .faiss_impl import FaissSearch
import os
import torch
# ====== Cấu hình ======
index_file = "C:\\Users\\magic\\Documents\\repo\\OpenAiServer\\OpenAIServer\\res\\my_index.faiss"
metadata_file = "C:\\Users\\magic\\Documents\\repo\\OpenAiServer\\OpenAIServer\\res\\metadata.json"

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