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


#/*

data "aws_instances" "existing_nano" {
  filter {
    name   = "tag:Name"
    values = ["Nano-EC2-Instance"]  
  }
}

resource "aws_instance" "nano_instance" {
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
  tags = {
    Name = "Nano-EC2-Instance"
  }

  lifecycle {
    ignore_changes = [ami, instance_type]  # Prevents recreation if specs change
    prevent_destroy = true                  # Blocks accidental deletion
  }
}


#*/





/*
resource "aws_instance" "nano_instance" {
  count =1
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
  tags = {
    Name = "Nano-EC2-Instance"
  }
}

*/
