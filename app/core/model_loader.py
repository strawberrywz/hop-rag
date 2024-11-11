from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from dotenv import load_dotenv

class ModelLoader:
  def __init__(self):
    """_summary_
    """
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
        