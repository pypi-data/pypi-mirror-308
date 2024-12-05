import json
from typing import Any, List, Dict, Tuple


class DataHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> Any:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def extract_questions_and_answers(self, data: Any) -> Tuple[List[str], Dict[str, str]]:
        questions, qna_dict = [], {}
        if 'faq' in data:
            for entry in data['faq']:
                question = entry.get('question', '')
                answer = entry.get('answer', '')
                if question and answer:
                    questions.append(question)
                    qna_dict[question] = answer
        return questions, qna_dict
