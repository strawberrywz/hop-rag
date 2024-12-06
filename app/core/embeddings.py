from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

class Embeddings:
  def __init__(self,
               model_loader 
               ):
    self.model_loader = model_loader
    self.embeddings = self.model_loader.load_embedding_model()
    self.model = self.model_loader.load_model()
        
  def load_embeddings(self, documents):
    try:
      db = Chroma.from_documents(documents, self.embeddings)
      k = min(3, len(documents))
      return db.as_retriever(search_kwargs={"k": k})
    except Exception as e:
      raise Exception(f"Error creating retriever: {str(e)}")
