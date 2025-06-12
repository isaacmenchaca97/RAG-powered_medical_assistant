# RAG-powered Medical Assistant: Terraform Infrastructure

This directory contains Terraform code to provision AWS resources for the RAG-powered Medical Assistant project. The infrastructure is organized so you can apply resources in stages to better understand and control each component.

## Staged Terraform Apply Procedure

### 1. S3 Bucket for Knowledge Base Documents
Creates an S3 bucket and configures versioning, encryption, and public access block.

```bash
terraform apply -auto-approve -target=aws_s3_bucket.knowledge_base_documents
terraform apply -auto-approve -target=aws_s3_bucket_versioning.knowledge_base_documents
terraform apply -auto-approve -target=aws_s3_bucket_server_side_encryption_configuration.knowledge_base_documents
terraform apply -auto-approve -target=aws_s3_bucket_public_access_block.knowledge_base_documents
```

### 2. IAM Role (without policy)
Creates the IAM role that will later be granted permissions for Bedrock and OpenSearch access.

```bash
terraform apply -auto-approve -target=aws_iam_role.knowledge_base_role
```

### 3. OpenSearch Serverless Components
Provisions the OpenSearch Serverless collection, security policies, and access policy. This must be done before attaching the IAM role policy, as the policy needs the collection ARN.

```bash
terraform apply -auto-approve -target=aws_opensearchserverless_security_policy.knowledge_base_encryption
terraform apply -auto-approve -target=aws_opensearchserverless_collection.knowledge_base
terraform apply -auto-approve -target=aws_opensearchserverless_security_policy.knowledge_base_network
terraform apply -auto-approve -target=aws_opensearchserverless_access_policy.knowledge_base
```

### 4. IAM Role Policy (after OpenSearch collection exists)
Attaches the permissions policy to the IAM role. This step requires the OpenSearch collection ARN, so it must be done after the collection is created.

```bash
terraform apply -auto-approve -target=aws_iam_role_policy.knowledge_base_permissions
```

**Manual Step Required:**
After this stage, you must manually create a vector index in the AWS Console:
1. Go to AWS Console > OpenSearch Serverless > Collections > [your collection] > Indexes.
2. Create a vector index with:
   - Name: `bedrock-knowledge-base-index`
   - Vector field: `embeddings` (engine: faiss, dimensions: 1536, distance metric: Euclidean)
   - Metadata fields: `text`, `bedrock-metadata`

See: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html

### 5. Bedrock Knowledge Base and Data Source
Creates the Bedrock knowledge base and attaches the S3 data source.

```bash
terraform apply -auto-approve -target=aws_bedrockagent_knowledge_base.main
terraform apply -auto-approve -target=aws_bedrockagent_data_source.main
```

## General Notes
- Run `terraform plan` before each apply to review changes.
- Each stage depends on the previous one; apply them in order.
- The `time_sleep` resource ensures OpenSearch is ready before the knowledge base is created.
- All resources are tagged for environment and project tracking.

## Cleanup
To destroy all resources:
```bash
terraform destroy
```

---
For more details, see the comments in each `.tf` file. 