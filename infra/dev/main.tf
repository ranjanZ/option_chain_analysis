
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


resource "aws_budgets_budget" "monthly-budget" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "0.01"
  limit_unit        = "USD"
  time_period_start = "2024-09-01_00:00"
  time_unit         = "MONTHLY"

}




