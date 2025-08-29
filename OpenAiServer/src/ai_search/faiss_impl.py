import os

import faiss
import json
import torch
import open_clip

MAX_SEARCH = 10
class FaissSearch:
    tokenizer = None
    metadata = None
    model = None
    device = None
    index = None

    def __init__(self, index_file, metadata_file, device="cuda"):
        # Load FAISS index
        self.index = faiss.read_index(index_file)

        # Load metadata
        with open(metadata_file, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        # Load CLIP model
        self.model, _, _ = open_clip.create_model_and_transforms(
            'hf-hub:laion/CLIP-ViT-H-14-laion2B-s32B-b79K'
        )
        self.model = self.model.to(device);
        self.device = device;
        self.tokenizer = open_clip.get_tokenizer('hf-hub:laion/CLIP-ViT-H-14-laion2B-s32B-b79K')
        self.model.eval()

        assert self.model is not None
        assert self.tokenizer is not None
        assert self.device is not None
        assert self.metadata is not None
        assert self.index is not None

        pass

    def search(self, searchType, query):
            # Encode query text
            with torch.no_grad(), torch.amp.autocast(device_type=self.device):
                text_tokens = self.tokenizer([query]).to(self.device)
                text_features = self.model.encode_text(text_tokens)
                text_features /= text_features.norm(dim=-1, keepdim=True)
                text_vector = text_features.cpu().float().numpy().astype('float32')

            # Search
            distances, indices = self.index.search(text_vector, MAX_SEARCH)

            # Hiển thị kết quả
            result = []
            for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
                img_path = self.metadata[str(idx)]
                result.append(img_path);

            return result

