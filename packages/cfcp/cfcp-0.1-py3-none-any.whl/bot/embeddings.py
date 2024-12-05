import torch
from transformers import AutoModel, AutoTokenizer
from typing import List


class EmbeddingsModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def get_embeddings(self, text: str) -> torch.Tensor:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

    def generate_question_embeddings(self, questions: List[str]) -> List[torch.Tensor]:
        return [self.get_embeddings(question) for question in questions]
