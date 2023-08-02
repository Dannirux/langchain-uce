import os

from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import streamlit as st

os.environ['OPENAI_API_KEY'] = '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'
default_doc_name = 'doc.pdf'


def create_db_from_document(path: str) -> Chroma:
    loader = PyPDFLoader(path)
    doc = loader.load_and_split()
    db = Chroma.from_documents(doc, embedding=OpenAIEmbeddings())
    return db

def process_doc(question: str, db: Chroma) -> str:
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=db.as_retriever())
    return qa.run(question)

def client():
    st.title('Manage LLM with LangChain')
    uploader = st.file_uploader('Upload PDF', type='pdf')

    if uploader:
        with open(f'./{default_doc_name}', 'wb') as f:
            f.write(uploader.getbuffer())
        st.success('PDF saved!!')

    question = st.text_input('Generar un resumen de 20 palabras sobre el pdf',
                             placeholder='Give response about your PDF', disabled=not uploader)

    if st.button('Send Question'):
        if uploader:
            process_doc(
                path=default_doc_name,
                is_local=True,
                question=question
            )
        else:
            st.info('Loading default PDF')
            process_doc()


if __name__ == '__main__':
    client()
    #process_doc()
