
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




resource "aws_instance" "nano_instance" {
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
}



resource "aws_ec2_tag" "nano_instance_tag" {
  resource_id = aws_instance.nano_instance.id
  key         = "Name"
  value       = "Nano-EC2-Instance"
}




output "public_ip" {
  value = aws_instance.nano_instance.public_ip
}




