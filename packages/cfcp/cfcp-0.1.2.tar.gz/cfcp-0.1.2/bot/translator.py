from deep_translator import GoogleTranslator


class Translator:
    def __init__(self, source_lang: str = 'ru', target_lang: str = 'en'):
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate_to_english(self, text: str) -> str:
        return GoogleTranslator(source=self.source_lang, target=self.target_lang).translate(text)

    def translate_to_russian(self, text: str) -> str:
        return GoogleTranslator(source=self.target_lang, target=self.source_lang).translate(text)
