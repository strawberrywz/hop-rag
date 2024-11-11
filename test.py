import os
from dotenv import load_dotenv
from app.core.s3_loader import S3Loader

load_dotenv()

loader = S3Loader(
    bucket=os.getenv('AWS_BUCKET'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION'),
    prefix="training-data/",
    password="your_password_if_needed" 
)

documents = loader.load()
print(f"Loaded {len(documents)} pages")
for doc in documents:
    print(f"Page {doc.metadata['page']}: {doc.page_content}...")