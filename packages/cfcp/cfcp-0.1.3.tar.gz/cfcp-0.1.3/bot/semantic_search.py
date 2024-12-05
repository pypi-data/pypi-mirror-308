from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
from bot.embeddings import EmbeddingsModel


class SemanticSearch:
    def __init__(self, model: EmbeddingsModel, threshold: float = 0.9):
        self.model = model
        self.threshold = threshold

    def search(self, query: str, question_embeddings: List, questions: List[str], qna_dict: Dict[str, str]) -> Optional[str]:
        query_embedding = self.model.get_embeddings(query)
        similarities = cosine_similarity([query_embedding], question_embeddings).flatten()
        top_index = similarities.argsort()[-1]
        if similarities[top_index] >= self.threshold:
            return qna_dict[questions[top_index]]
        return None
