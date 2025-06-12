# Wait for the OpenSearch collection to be ready
resource "time_sleep" "wait_for_opensearch" {
  depends_on = [
    aws_opensearchserverless_collection.knowledge_base,
    aws_opensearchserverless_security_policy.knowledge_base_encryption,
    aws_opensearchserverless_security_policy.knowledge_base_network,
    aws_opensearchserverless_access_policy.knowledge_base
  ]

  create_duration = "60s"
}

# Create the Bedrock knowledge base
resource "aws_bedrockagent_knowledge_base" "main" {
  name     = "${var.project_name}-knowledge-base-${var.environment}"
  role_arn = aws_iam_role.knowledge_base_role.arn

  description = "RAG knowledge base for ${var.project_name} chatbot"

  knowledge_base_configuration {
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:${data.aws_region.current.name}::foundation-model/amazon.titan-embed-text-v1"
    }
    type = "VECTOR"
  }

  storage_configuration {
    opensearch_serverless_configuration {
      collection_arn    = aws_opensearchserverless_collection.knowledge_base.arn
      vector_index_name = "bedrock-knowledge-base-index"

      field_mapping {
        vector_field   = "embeddings"
        text_field     = "text"
        metadata_field = "bedrock-metadata"
      }
    }
    type = "OPENSEARCH_SERVERLESS"
  }

  depends_on = [
    time_sleep.wait_for_opensearch,
    aws_iam_role_policy.knowledge_base_permissions
  ]
}

# Create a data source for the knowledge base
resource "aws_bedrockagent_data_source" "main" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.main.id
  name              = "${var.project_name}-documents-${var.environment}"

  description = "S3 data source for knowledge base documents"

  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = aws_s3_bucket.knowledge_base_documents.arn
    }
  }

  # Configure how documents are processed
  vector_ingestion_configuration {
    chunking_configuration {
      chunking_strategy = "FIXED_SIZE"

      fixed_size_chunking_configuration {
        max_tokens         = 300
        overlap_percentage = 20
      }
    }
  }
}
