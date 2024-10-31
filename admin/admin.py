import boto3
import streamlit as st
import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import BedrockEmbeddings


# S3 client
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Bedrock config

# Text Splitter

# pdf loader


def main():
    st.write("This is admin site for chat with pdf demo")
    uploaded_file = st.file_uploader("Choose a file", type="pdf")
    if uploaded_file is not None:
        request_id = uuid()
        st.write(f"Request ID: {request_id}")
        saved_file_name = f"{request_id}.pdf"
        with open(saved_file_name, mode="wb") as w:
            w.write(uploaded_file.getvalue())

        loader = PyMuPDFLoader(saved_file_name)
        pages = loader.load_and_split()

        st.write(f"Total Pages: {len(pages)}")


if __name__ == "__main__":
    main()
