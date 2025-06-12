terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"  # This ensures you have Bedrock support
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
  
  # These tags will be applied to all resources that support tagging
  default_tags {
    tags = {
      Environment = var.environment
      Project     = "rag-medical-assistant"
      ManagedBy   = "terraform"
    }
  }
}