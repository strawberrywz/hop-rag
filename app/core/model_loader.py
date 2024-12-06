from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch


class ModelLoader:
    def __init__(self):
        self.model_path = self.model_path = "sshleifer/distilbart-cnn-6-6"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.base_model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path) 
        self.base_model.to(self.device)

    def load_model(self):
        """Load the Flan-T5 model with LangChain integration"""
        pipe = pipeline(
            "summarization",
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