# Chat With PDF - Generative AI Application
## Built Using Amazon Bedrock, Langchain, Python, Docker, Amazon S3
## Models used:
    Amazon Titan Embedding G1 - Text
    Anthropic Claude 2.1

## Introduction
In this video we will build a CHATBOT like application with AWS Amazon Bedrock, docker, python, Langchain, and Streamlit. We will use Retrieval-Augmented generation concept to provide context to the Large Language model along with user query to generate response from our Knowledgebase.

In this hands-on tutorial, we will demonstrate the following:
- Architecture of the applications
- Build 2 applications (ADMIN and USER) and create DOCKER images


## Architecture
![image info](./Architecture Diagram.png)

## ADMIN Application:
    - Build Admin Web application where AdminUser can upload the pdf.
    - The PDF text is split into chunks
    - Using the Amazon Titan Embedding Model, create the vector representation of the chunks
    - Using FAISS, save the vector index locally
    - Upload the index to Amazon S3 bucket (You can use other vector stores like OpenSearch, Pinecone, PgVector etc., but for this demo, I chose cost effective S3)

### Docker Commands:

  Build Docker Image:
  `docker build -t pdf-reader-admin .`

  Run ADMIN application:
  `docker run -e BUCKET_NAME=<YOUR S3 BUCKET NAME> -v ~/.aws:/root/.aws -p 8083:8083 -it pdf-reader-admin`