from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch
from typing import List, Optional
from langchain.schema import Document
import os

class ModelLoader:
    def __init__(self):
        """Initialize the Flan-T5-Small model and tokenizer"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.model_path = os.path.join(project_root, "model")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.base_model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)
        self.base_model.to(self.device)

    def load_model(self):
        """Load the Flan-T5 model with LangChain integration"""
        pipe = pipeline(
            "text2text-generation",
            model=self.base_model,
            tokenizer=self.tokenizer,
            max_length=512,
            temperature=0.1,
            device=self.device
        )
        
        return HuggingFacePipeline(pipeline=pipe)
    
    def load_embedding_model(self):
        """Load HuggingFace embeddings model"""
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': self.device}
        )