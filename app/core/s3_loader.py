from typing import List, Optional
from langchain.schema import Document
from langchain.document_loaders.base import BaseLoader
import boto3
from botocore.exceptions import ClientError
import io
from PyPDF2 import PdfReader
from PyPDF2.errors import DependencyError, PdfReadError
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class S3Loader(BaseLoader):
    def __init__(self, 
                 bucket: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 region_name: str,
                 prefix: Optional[str] = "",
                 max_workers: int = 4 
                 ):
        self.bucket = bucket
        self.prefix = prefix
        self.max_workers = max_workers
        
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def process_pdf(self, key: str) -> List[Document]:
        """Process a single PDF file."""
        documents = []
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=key)
            file_obj = io.BytesIO(response['Body'].read())
            
            try:
                pdf = PdfReader(file_obj)
                total_pages = len(pdf.pages)
                
                for page_num in range(total_pages):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        
                        if text.strip():
                            metadata = {
                                "source": f"s3://{self.bucket}/{key}",
                                "page": page_num,
                                "total_pages": total_pages,
                                "file_type": "pdf",
                                "file_name": key.split('/')[-1]
                            }
                            
                            documents.append(Document(
                                page_content=text, 
                                metadata=metadata
                            ))
                    except Exception as e:
                        print(f"Error processing page {page_num} of PDF {key}: {e}")
                        continue
                        
            except (PdfReadError, DependencyError) as e:
                print(f"Error reading PDF {key}: {e}")
                
        except ClientError as e:
            print(f"Error accessing S3 file {key}: {e}")
        except Exception as e:
            print(f"Error processing PDF {key}: {e}")
            
        return documents

    def load(self) -> List[Document]:
        """Load all PDFs in parallel."""
        try:
            pdf_files = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        if obj['Key'].lower().endswith('.pdf'):
                            pdf_files.append(obj['Key'])
            
            all_documents = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = list(tqdm(
                    executor.map(self.process_pdf, pdf_files),
                    total=len(pdf_files),
                    desc="Loading PDFs"
                ))
                
                for docs in futures:
                    all_documents.extend(docs)
                    
            return all_documents
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []