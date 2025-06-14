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

# Create the instance (Terraform will handle duplicates via state)
resource "aws_instance" "nano_instance" {
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"

  tags = {
    Name = "Nano-EC2-Instance"
  }
  lifecycle {
    prevent_destroy = true  # Blocks `terraform destroy` and accidental replaces
  }

}

# Output the instance IP
output "instance_ip" {
  value = aws_instance.nano_instance.public_ip
}
