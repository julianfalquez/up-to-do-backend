import os
import boto3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/flaskr')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region,
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "up-to-do-bucket")

engine = create_engine(os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/flaskr'
), echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine)