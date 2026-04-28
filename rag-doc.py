from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from fastapi import FastAPI
from pydantic import BaseModel

loader = PyPDFLoader("document.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("""
Responde la pregunta usando únicamente el contexto dado.

Contexto:
{context}

Pregunta:
{input}
""")

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    result = qa_chain.invoke({"input": req.question})
    return {"answer": result["answer"]}
