<<<<<<< HEAD
import PyPDF2
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
import PyPDF2


def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
=======
import pypdf2
from langchain.llms import Ollama
from langchain.chains.summarize import load_summarize_chain

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = pypdf2.PdfReader(file)
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

<<<<<<< HEAD
def summarize_text(text):
    llm = Ollama(model="llama2:3b")
=======
def summarize_text(text, llm):
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(text)
    return summary

<<<<<<< HEAD
def chat_with_document(query, text):
    llm = Ollama(model="llama2:3b")
=======
def chat_with_document(query, text, llm):
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
    response = llm(f"Based on the following text, answer this question: {query}\n\nText: {text}")
    return response

# Example usage
if __name__ == "__main__":
<<<<<<< HEAD
    pdf_path = "example.pdf"
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text)
    print("Summary:", summary)

    query = "What is the main topic of this document?"
    answer = chat_with_document(query, text)
=======
    llm = Ollama(model="llama2:3b")
    pdf_path = "example.pdf"
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text, llm)
    print("Summary:", summary)

    query = "What is the main topic of this document?"
    answer = chat_with_document(query, text, llm)
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
    print("Answer:", answer)
