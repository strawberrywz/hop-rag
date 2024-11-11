from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from .prompt_templates import chat_prompt_template
from app.core.s3_loader import S3Loader
from app.core.model_loader import ModelLoader
from app.core.embeddings import Embeddings
import time
import os

class ChatModel:
    def __init__(self):
        self.document_loader = S3Loader(
            bucket=os.getenv('AWS_BUCKET'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION'),
            prefix=os.getenv('AWS_PREFIX', '')
        )
        self.model_loader = ModelLoader()
        self.embeddings = Embeddings(self.model_loader)
        self._retriever = None
        
    def load_documents(self):
        """Separate method to test document loading performance"""
        start_time = time.time()
        documents = self.document_loader.load()
        load_time = time.time() - start_time
        
        print(f"Document loading took {load_time:.2f} seconds")
        print(f"Loaded {len(documents)} document chunks")
        
        return documents
    
    def create_retriever(self, documents):
        """Separate method to test retriever creation performance"""
        start_time = time.time()
        retriever = self.embeddings.load_embeddings(documents)
        embed_time = time.time() - start_time
        
        print(f"Embedding creation took {embed_time:.2f} seconds")
        return retriever

    @property
    def retriever(self):
        if self._retriever is None:
            documents = self.load_documents()
            self._retriever = self.create_retriever(documents)
        return self._retriever
    
    def generate_response(self, query: str) -> str:
        try:
            start_time = time.time()
            
            docs = self.retriever.get_relevant_documents(query)
            retrieval_time = time.time() - start_time
            
            chain = (
                {"context": lambda _: "\n\n".join(d.page_content for d in docs),
                "question": RunnablePassthrough()}
                | chat_prompt_template
                | self.embeddings.model
                | StrOutputParser()
            )
            
            response = chain.invoke(query)
            total_time = time.time() - start_time
            
            print(f"Document retrieval took {retrieval_time:.2f} seconds")
            print(f"Total response time: {total_time:.2f} seconds")
            
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
            
    def reload_documents(self):
        self._retriever = None