import asyncio
from bot.config import DATA_FILE_PATH, MAX_CONTEXT_LENGTH, THRESHOLD
from bot.data_handler import DataHandler
from bot.embeddings import EmbeddingsModel
from bot.semantic_search import SemanticSearch
from bot.translator import Translator
from bot.response_generator import ResponseGenerator
from typing import Tuple, Optional

class CFCP:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.context = ""
        self.data_handler = DataHandler(DATA_FILE_PATH)
        self.embeddings_model = EmbeddingsModel()
        self.semantic_search = SemanticSearch(self.embeddings_model, threshold=THRESHOLD)
        self.translator = Translator()
        template = """
        Вы — {name}
        Данные: {doc}
        История общения: {context}
        Вопрос пользователя: {question}
        Отвечай только на вопросы по программированию, остальное вежливо отклоняй.
        Ответ:
        """
        self.response_generator = ResponseGenerator(template, MAX_CONTEXT_LENGTH)
        data = self.data_handler.load_data()
        self.questions, self.qna_dict = self.data_handler.extract_questions_and_answers(data)
        self.question_embeddings = self.embeddings_model.generate_question_embeddings(self.questions)

    async def generate_answer(self, user_input: str) -> str:
        question_en = self.translator.translate_to_english(user_input)
        top_answer = self.semantic_search.search(question_en, self.question_embeddings, self.questions, self.qna_dict)
        if top_answer:
            return self.translator.translate_to_russian(top_answer)
        result = await self.response_generator.generate_response(
            self.context, self.qna_dict, question_en, self.name, self.description
        )
        translated_result = self.translator.translate_to_russian(result)
        self.context = self.response_generator.update_context(self.context, user_input, translated_result)
        return translated_result

    async def run(self):
        print(f"{self.name} готов к работе.")
        while True:
            user_input = input("> ")
            result = await self.generate_answer(user_input)
            print(result)

