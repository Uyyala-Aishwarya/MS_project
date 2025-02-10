import os
from docx import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

os.environ["OPENAI_API_KEY"] = "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"

def read_text_files():
    texts = []
    folder_path = "./"
    filename = "./documentation.docx"
    doc = Document(os.path.join(folder_path, filename))
    doc_text = ' '.join([para.text for para in doc.paragraphs])
    texts.append(doc_text)
    return texts

def chunk_texts(texts, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for text in texts:
        chunks.extend(text_splitter.split_text(text))
    return chunks

def create_vector_store(chunks):
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    # Create a FAISS vector store
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def create_qa_chain(vector_store):
    # Initialize OpenAI GPT-3.5 Turbo
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # Create a retrieval-based QA chain
    retriever = vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return qa_chain

def initialize_rag():
    # Read files
    texts = read_text_files()
    # Chunk the texts
    chunks = chunk_texts(texts)
    # Create vector knowledge base
    vector_store = create_vector_store(chunks)
    # Create QA chain
    qa_chain = create_qa_chain(vector_store)
    return qa_chain

def ask_question(question):
    qa_chain = initialize_rag()
    return qa_chain.invoke({'query': question})["result"]

if __name__ == "__main__":
    question = "What is the main topic of the documents?"
    answer = ask_question(question)
    print(answer)
