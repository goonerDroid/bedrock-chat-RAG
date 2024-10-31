import boto3
import streamlit as st
import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS


# S3 client
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Bedrock Config
bedrock_client = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-image-v1", client=bedrock_client)


def get_unique_id():
    return str(uuid.uuid4())


# Split the pages/text into chunks


def split_text(pages, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs


# Create Vector Store
def create_vector_store(request_id, documents):
    vectorstore_faiss = FAISS.from_documents(documents, bedrock_embeddings)
    file_name = f"{request_id}.bin"
    folder_path = "/tmp/"
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)

    # upload to S3
    s3_client.upload_file(Filename=folder_path + "/" + file_name +
                          ".faiss", Bucket=BUCKET_NAME, Key="my_faiss.faiss")
    s3_client.upload_file(Filename=folder_path + "/" + file_name +
                          ".pkl", Bucket=BUCKET_NAME, Key="my_faiss.pkl")

    return True


def main():
    st.write("Admin site to upload pdf files for RAG")
    uploaded_file = st.file_uploader("Choose a file", type="pdf")
    if uploaded_file is not None:
        request_id = get_unique_id()
        st.write(f"Request ID: {request_id}")
        saved_file_name = f"{request_id}.pdf"
        with open(saved_file_name, mode="wb") as w:
            w.write(uploaded_file.getvalue())

        loader = PyMuPDFLoader(saved_file_name)
        pages = loader.load_and_split()

        st.write(f"Total Pages: {len(pages)}")

        # Split text
        splitted_docs = split_text(pages, 1000, 200)
        st.write(f"Splitted Docs Length: {len(splitted_docs)}")
        st.write("===================")
        st.write(splitted_docs[0])
        st.write("===================")
        st.write(splitted_docs[1])
        st.write("Creating the Vector Store")
        result = create_vector_store(request_id, splitted_docs)

        if result:
            st.write("PDF processed successfully")
        else:
            st.write("Error!! Please check logs.")


if __name__ == "__main__":
    main()
