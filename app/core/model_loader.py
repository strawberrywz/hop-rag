from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import S3FileLoader
from langchain.chains import RetrievalQA
import torch
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv

class ModelLoader:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

    def load_model(self):
        return ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.1,
            openai_api_key=self.api_key
        )
    
    def load_embedding_model(self):
        return OpenAIEmbeddings(
            openai_api_key=self.api_key
        )
        