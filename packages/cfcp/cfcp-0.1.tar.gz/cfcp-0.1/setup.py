from setuptools import setup, find_packages

setup(
    name='cfcp',  # Название пакета, используемое при установке
    version='0.1',  # Версия пакета
    description='A Python-based consultant bot for programming courses',
    author='Santas7',
    author_email='your.email@example.com',
    packages=find_packages(),  # Находит все подкаталоги и файлы в проекте
    install_requires=[
        'torch',  # PyTorch для работы с тензорами и моделью
        'transformers',  # Hugging Face для загрузки модели и токенизатора
        'scikit-learn',  # Для расчета косинусного сходства
        'deep-translator',  # Для перевода текста
        'langchain',  # Для генерации ответов с использованием LLM
    ],
    python_requires='>=3.7',  # Укажите минимальную версию Python
    entry_points={
        'console_scripts': [
            'consultant_bot=bot.main:run',  # Делаем консольную команду для запуска бота
        ],
    },
    include_package_data=True,
    package_data={'bot': ['data.json']},  # Укажите дополнительные файлы, которые должны включаться
)
