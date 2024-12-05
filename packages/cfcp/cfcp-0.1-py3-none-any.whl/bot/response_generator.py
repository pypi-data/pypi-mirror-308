import asyncio
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict


class ResponseGenerator:
    def __init__(self, template: str, context_length: int):
        self.model_llm = OllamaLLM(model="phi")
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = self.prompt | self.model_llm
        self.context_length = context_length

    async def generate_response(self, context: str, qna_dict: Dict[str, str], question: str, name: str, description: str) -> str:
        return await asyncio.to_thread(self.chain.invoke, {
            "context": context,
            "doc": list(qna_dict.values()),
            "question": question,
            "name": name,
            "description": description
        })
    
    def update_context(self, context: str, user_input: str, result: str) -> str:
        context += f"\nUser: {user_input}\nAI: {result}"
        return context[-self.context_length:]
