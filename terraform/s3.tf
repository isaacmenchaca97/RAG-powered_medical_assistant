    # Create the S3 bucket for storing knowledge base documents
resource "aws_s3_bucket" "knowledge_base_documents" {
  bucket = "${var.project_name}-knowledge-base-documents-${var.environment}"
  
  # Force delete allows Terraform to delete non-empty buckets
  # Be careful with this in production environments
  force_destroy = var.environment == "dev" ? true : false
}

# Configure bucket versioning to track document changes
resource "aws_s3_bucket_versioning" "knowledge_base_documents" {
  bucket = aws_s3_bucket.knowledge_base_documents.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption for document security
resource "aws_s3_bucket_server_side_encryption_configuration" "knowledge_base_documents" {
  bucket = aws_s3_bucket.knowledge_base_documents.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Block public access to ensure documents remain private
resource "aws_s3_bucket_public_access_block" "knowledge_base_documents" {
  bucket = aws_s3_bucket.knowledge_base_documents.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}