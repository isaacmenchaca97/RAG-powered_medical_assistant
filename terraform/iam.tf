# Create the trust policy document for the knowledge base service role
data "aws_iam_policy_document" "knowledge_base_trust_policy" {
  statement {
    effect = "Allow"
    
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
    
    actions = ["sts:AssumeRole"]
    
    # Add conditions for enhanced security
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
    
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:bedrock:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:knowledge-base/*"]
    }
  }
}

# Create the permissions policy document
data "aws_iam_policy_document" "knowledge_base_permissions" {
  # Allow reading from the S3 bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.knowledge_base_documents.arn,
      "${aws_s3_bucket.knowledge_base_documents.arn}/*"
    ]
  }
  
  # Allow invoking the embedding model
  statement {
    effect = "Allow"
    actions = ["bedrock:InvokeModel"]
    resources = [
      "arn:aws:bedrock:${data.aws_region.current.name}::foundation-model/amazon.titan-embed-text-v1"
    ]
  }
  
  # Allow access to the OpenSearch collection
  statement {
    effect = "Allow"
    actions = ["aoss:APIAccessAll"]
    resources = [aws_opensearchserverless_collection.knowledge_base.arn]
  }
}

# Create the IAM role using the policy documents
resource "aws_iam_role" "knowledge_base_role" {
  name               = "${var.project_name}-knowledge-base-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.knowledge_base_trust_policy.json
}

# Attach the permissions policy to the role
resource "aws_iam_role_policy" "knowledge_base_permissions" {
  name   = "${var.project_name}-knowledge-base-permissions-${var.environment}"
  role   = aws_iam_role.knowledge_base_role.id
  policy = data.aws_iam_policy_document.knowledge_base_permissions.json
}