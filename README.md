# 🩺 RAG-Powered Medical Assistant

📍 Objective

Develop a Retrieval-Augmented Generation (RAG) system that assists healthcare professionals by providing accurate, real-time information from medical literature and internal protocols. The assistant aims to enhance clinical decision-making by retrieving relevant documents and generating concise, context-aware responses.

🧠 Features

- Colect data from PubMed, NIH guidlines, internal hospital protocols
- Fine-tune an open-source LLM using the collected data to give the model an understanding of internal protocols or proprietary clinical knowledge
- Populate a vector database (DB) using our digital data for RAG
- Have a simple web interface to interact with the LLM and be able to do the following:
    - Upload patient data (PDF)
    - Manage different chats
- Implement HIPAA (Health Insurance Portability and Accountability Act) compliance

🔧 System Architecture Overview
- Data Collection Pipeline
    Goal: Collect and store unstructured healthcare data.
- Feature Pipeline
    Goal: Convert raw documents to vector embeddings, store in a retrievable format and instruct dataset for fine-tuning.
- Training Pipeline
    Goal: Fine-tune a domain-specific LLM to give the model an understanding of internal protocols or proprietary clinical knowledge.
- Inference Pipeline
    Goal: Serve responses grounded in retrieved documents using RAG.


🗂️ Project Structure
```
rag-powered-medical-assistant/
├── configs/             # Pipeline configuration files
├── llm_engineering/     # Core project package
│   ├── application/    
│   ├── domain/         
│   ├── infrastructure/ 
│   ├── model/         
├── notebooks/
├── pipelines/           # ML pipeline definitions
├── steps/               # Pipeline components
├── terraform/           # Terraform for S3, Bedrock, OpenSearch, etc.
├── tests/               # Test examples
├── tools/               # Utility scripts
│   ├── run.py
│   ├── ml_service.py
│   ├── rag.py
│   ├── data_warehouse.py
```

🧰 Tools 

- Python: Poetry (dependency and virtual environment management), Poe the Poet (task execution tool).
- MLOps and LLMOps tooling: MLFlow (experiment tracker and model registry), ZenML (orchestrator, artifacts, and metadata), Langfuse (prompt monitoring).
- Databases: Amazon DocumentDB (NoSQL database), Amazon OpenSearch Service (vector store).
- Cloud: S3 (object storage), ECR (container registry), and SageMaker (compute for training and inference), FastAPI + ECS Fargate (deployment), Streamlit (UI).