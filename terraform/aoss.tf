# Create a security policy for the collection
resource "aws_opensearchserverless_security_policy" "knowledge_base_encryption" {
  name = "${var.project_name}-kb-enc-${var.environment}"
  type = "encryption"
  
  policy = jsonencode({
    Rules = [
      {
        Resource = [
          "collection/${var.project_name}-kb-${var.environment}"
        ]
        ResourceType = "collection"
      }
    ]
    AWSOwnedKey = true
  })
}

# Create the OpenSearch Serverless collection for storing embeddings
resource "aws_opensearchserverless_collection" "knowledge_base" {
  name = "${var.project_name}-kb-${var.environment}"
  type = "VECTORSEARCH"
  
  description = "Vector database for Bedrock knowledge base embeddings"

  depends_on = [aws_opensearchserverless_security_policy.knowledge_base_encryption]
}

# Create a network security policy
resource "aws_opensearchserverless_security_policy" "knowledge_base_network" {
  name = "${var.project_name}-kb-net-${var.environment}"
  type = "network"
  
  policy = jsonencode([
    {
      Rules = [
        {
          Resource = [
            "collection/${aws_opensearchserverless_collection.knowledge_base.name}"
          ]
          ResourceType = "collection"
        }
      ]
      AllowFromPublic = true
    }
  ])
}

# Create an access policy that allows the knowledge base role to use the collection
resource "aws_opensearchserverless_access_policy" "knowledge_base" {
  name = "${var.project_name}-kb-access-${var.environment}"
  type = "data"
  
  policy = jsonencode([
    {
      Rules = [
        {
          Resource = [
            "collection/${aws_opensearchserverless_collection.knowledge_base.name}"
          ]
          Permission = [
            "aoss:CreateCollectionItems",
            "aoss:DeleteCollectionItems", 
            "aoss:UpdateCollectionItems",
            "aoss:DescribeCollectionItems"
          ]
          ResourceType = "collection"
        },
        {
          Resource = [
            "index/${aws_opensearchserverless_collection.knowledge_base.name}/*"
          ]
          Permission = [
            "aoss:CreateIndex",
            "aoss:DeleteIndex",
            "aoss:UpdateIndex",
            "aoss:DescribeIndex",
            "aoss:ReadDocument",
            "aoss:WriteDocument"
          ]
          ResourceType = "index"
        }
      ]
      Principal = [
        aws_iam_role.knowledge_base_role.arn,
        data.aws_caller_identity.current.arn
      ]
    }
  ])
}
