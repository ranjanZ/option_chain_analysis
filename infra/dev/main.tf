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
  filter {
    name   = "instance-state-name"
    values = ["running", "stopped"]  # Only count active instances
  }
}

resource "aws_instance" "nano_instance" {
  # Only create if NO matching instance exists
  count = length(data.aws_instances.existing_nano.ids) == 0 ? 1 : 0

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
