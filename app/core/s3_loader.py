from typing import List, Optional
from langchain.schema import Document
from langchain.document_loaders.base import BaseLoader
import boto3
from botocore.exceptions import ClientError
from langchain.text_splitter import RecursiveCharacterTextSplitter
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class S3Loader(BaseLoader):
    def __init__(self, 
                 bucket: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 region_name: str,
                 prefix: Optional[str] = "",
                 max_workers: int = 4):
        self.bucket = bucket
        self.prefix = prefix
        self.max_workers = max_workers
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def process_text(self, key: str) -> List[Document]:
        """Process a single text file."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=key)
            text = response['Body'].read().decode('utf-8')
            
            text_splitter = RecursiveCharacterTextSplitter(
              chunk_size=500, 
              chunk_overlap=50,
              separators=["\n\n", "\n", " ", ""]
              )
            
            chunks = text_splitter.create_documents(
              texts=[text],
              metadatas = [{
                "source": f"s3://{self.bucket}/{key}",
                "file_type": "txt",
                "file_name": key.split('/')[-1]
                }]
            )
            
            return chunks
            
        except ClientError as e:
            print(f"Error accessing S3 file {key}: {e}")
        except Exception as e:
            print(f"Error processing text file {key}: {e}")
        
        return []

    def load(self) -> List[Document]:
        """Load all text files in parallel."""
        try:
            text_files = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        if obj['Key'].lower().endswith('.txt'):
                            text_files.append(obj['Key'])
            
            all_documents = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = list(tqdm(
                    executor.map(self.process_text, text_files),
                    total=len(text_files),
                    desc="Loading text files"
                ))
                
                for docs in futures:
                    all_documents.extend(docs)
                    
            return all_documents
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []