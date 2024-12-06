from setuptools import setup, find_packages

setup(
    name='learn_genai',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'streamlit',
        'jupyter',
        'PyPDF2',
        'faiss-cpu',
        'langchain',
        'langgraph',
        'transformers',
        'torch'
    ],
    entry_points={
        'console_scripts': [
            'learn_genai_app=learn_genai.app:main',  # Lanza la app Streamlit desde learn_genai/app.py
            'learn_genai_process=learn_genai.data_processor:run_data_processing',  # Lanza otro script .py para procesamiento de datos
        ],
    },
    author='Antonio Esposito',
    author_email='fbanespo@gmail.com',
    description='Paquete para aprender Generative AI con ejemplos prácticos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fbanespo1/learn_genai',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
