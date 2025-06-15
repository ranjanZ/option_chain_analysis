terraform {
  backend "s3" {
    bucket         = "s2ranjan"               # Your S3 bucket name
    key            = "terraform.tfstate"      # Path to store state file
    region         = "us-east-2"              # AWS region
  }
}
