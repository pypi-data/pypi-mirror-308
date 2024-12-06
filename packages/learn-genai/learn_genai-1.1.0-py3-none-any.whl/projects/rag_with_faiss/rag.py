import faiss
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

def create_vectorstore(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore

def query_vectorstore(vectorstore, query):
    llm = Ollama(model="llama2:3b")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
    result = qa_chain({"query": query})
    return result["result"]

# Example usage
if __name__ == "__main__":
    file_path = "example_data.txt"
    vectorstore = create_vectorstore(file_path)
    
    query = "What is the capital of France?"
    answer = query_vectorstore(vectorstore, query)
    print("Answer:", answer)
