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
  count         = 1
  ami           = "ami-0d1b5a8c13042c939"  # Ubuntu 20.04 LTS
  instance_type = "t2.nano"
  
  # Reference external script file
  user_data = file("${path.module}/start_script.sh")

  tags = {
    Name = "Nano-EC2-Instance"
  }

  lifecycle {
    prevent_destroy = true
    ignore_changes = [ami, instance_type, user_data]  # Preserve user_data changes
  }
}






/*

resource "aws_instance" "nano_instance" {
  # Only create if NO matching instance exists
  count 	= 1  
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
  
  tags = {
    Name = "Nano-EC2-Instance"
  }

  lifecycle {
    prevent_destroy = true  # Extra protection against deletion
    ignore_changes = [ami, instance_type]  # Prevents recreation if specs change
  }
}




*/





















