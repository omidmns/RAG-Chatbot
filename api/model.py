from typing import Optional
from langchain.llms import HuggingFaceHub
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# default HF repo id
HF_REPO_ID = os.environ.get("HF_REPO_ID")


class RAGModel:
    def __init__(self):
        self.model_kwargs = dict(
            max_length=512,
            top_k=5,
            top_p=0.25,
            temperature=0.01,
        )
        self.repo_id = HF_REPO_ID
        self.huggingfacehub_api_token = None
        self.llm = None
        self.db = None
        self.url = None

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )

    def update_llm(
        self,
        huggingfacehub_api_token: Optional[str] = None,
        repo_id: Optional[str] = None,
        **model_kwargs,
    ):
        self.model_kwargs.update(model_kwargs)

        if repo_id:
            self.repo_id = repo_id

        if huggingfacehub_api_token:
            self.huggingfacehub_api_token = huggingfacehub_api_token

        self.llm = HuggingFaceHub(
            repo_id=self.repo_id,
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            model_kwargs=self.model_kwargs,
        )

        return self.llm

    def load_url(self, url: str):
        self.url = url
        loader = WebBaseLoader(url)

        # interpret information in the documents
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(documents)

        # create and save the local database
        self.db = FAISS.from_documents(splits, self.embeddings)

        return self.db

    def retrieve_response(self, question: str, template: Optional[str] = None):
        if not template:
            template = """Use the following pieces of information to answer the user's question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            Context: {context}
            Question: {question}
            Only return the helpful answer below and nothing else.
            Helpful answer:
            """

        if not self.db:
            logger.warning("Please provide the url!")
            return "Please provide the url before asking a question!"

        retriever = self.db.as_retriever(search_kwargs={"k": 4, "fetch_k": 4})

        prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        qa_llm = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        output = qa_llm({"query": question})

        logger.info(f"repo_id: {self.repo_id}")
        logger.info(f"url: {self.url}")
        logger.info(f"model_kwargs: {self.model_kwargs}")

        return output["result"]
