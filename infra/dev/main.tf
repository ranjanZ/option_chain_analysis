
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>3.3.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}


resource "null_resource" "budget_check" {
  triggers = {
    budget_exists = <<EOT
      #!/bin/bash
      aws budgets describe-budgets --account-id 992382828607 \
        --query 'Budgets[?Name==`monthly-budget`].Name' \
        --output text | grep -q monthly-budget && echo "exists"
    EOT
  }
}

resource "aws_budgets_budget" "monthly-budget" {
  count         = null_resource.budget_check.triggers.budget_exists == "exists" ? 0 : 1
  name          = "monthly-budget"
  budget_type   = "COST"
  limit_amount  = "0.001"
  limit_unit    = "USD"
  time_unit     = "MONTHLY"
}






}




