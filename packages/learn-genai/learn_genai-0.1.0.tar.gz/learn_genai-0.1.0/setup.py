from setuptools import setup, find_packages

setup(
    name="learn_genai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langgraph",
        "beautifulsoup4",
        "requests",
        "faiss-cpu",
    ],
    entry_points={
        "console_scripts": [
            "learn_genai=learn_genai.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to learn Generative AI through practical examples",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/learn_genai",
)
