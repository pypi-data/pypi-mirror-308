<<<<<<< HEAD
import faiss
=======
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
<<<<<<< HEAD
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

def create_vectorstore(file_path):
=======

def create_vectorstore(file_path, embeddings):
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

<<<<<<< HEAD
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore

def query_vectorstore(vectorstore, query):
    llm = Ollama(model="llama2:3b")
=======
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore

def query_vectorstore(vectorstore, query, llm):
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
    result = qa_chain({"query": query})
    return result["result"]

# Example usage
if __name__ == "__main__":
<<<<<<< HEAD
    file_path = "example_data.txt"
    vectorstore = create_vectorstore(file_path)
    
    query = "What is the capital of France?"
    answer = query_vectorstore(vectorstore, query)
=======
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    llm = Ollama(model="llama2:3b")
    
    file_path = "example_data.txt"
    vectorstore = create_vectorstore(file_path, embeddings)
    
    query = "What is the capital of France?"
    answer = query_vectorstore(vectorstore, query, llm)
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
    print("Answer:", answer)
