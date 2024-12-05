from setuptools import setup, find_packages

setup(
    name='cfcp',  # Название пакета
    version='0.1.3',
    description='A Python-based consultant bot for programming courses',
    author='Santas7',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'torch',  
        'transformers',  
        'scikit-learn',  
        'deep-translator',  
        'langchain',  
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'cfcp=bot.main:run',  # Консольная команда, которая будет вызывать функцию `run()` из `bot/main.py`
        ],
    },
    include_package_data=True,
    package_data={'bot': ['data.json']},  # Указание дополнительных файлов для включения в пакет
)
