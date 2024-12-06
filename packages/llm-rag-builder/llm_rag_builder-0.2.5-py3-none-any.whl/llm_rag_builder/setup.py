from setuptools import setup


setup(
    name="llm-rag-builder",
    version="0.2.5",
    description="Это библиотека на Python, предназначенная для упрощения создания и управления моделями генерации"
                " с использованием поиска (Retrieval-Augmented Generation, RAG).",
    long_description=open("llm_rag_builder/README.md").read(),
    long_description_content_type="text/markdown",
    author="лень",
    author_email="pzrnqt1vrss@protonmail.com",
    url="https://github.com/leo-need-more-coffee/rag_builder",
    packages=[
        'llm_rag_builder',
        'llm_rag_builder.core',
        'llm_rag_builder.integrations',
        'llm_rag_builder.integrations.chromadb',
        'llm_rag_builder.integrations.gemini',
        'llm_rag_builder.integrations.openai',
        'llm_rag_builder.integrations.pgvector',
        'llm_rag_builder.integrations.yandex',
        'llm_rag_builder.utils'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[

    ],
    extras_require={
        "all": ["openai", "google-generativeai", "yandex-chain", "chromadb", "psycopg2", "pgvector"],
        "openai": ["openai"],
        "gemini": ["google-generativeai"],
        "yandex": ["yandex-chain"],
        "chroma": ["chromadb"],
        "pgvector": ["psycopg2", "pgvector"]
    }
)
