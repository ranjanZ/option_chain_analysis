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





# 1. Create IAM role for EC2
resource "aws_iam_role" "ec2_ssm_role" {
  name = "EC2-SSM-Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# 2. Attach the SSM policy
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# 3. Create an instance profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2-SSM-Profile"
  role = aws_iam_role.ec2_ssm_role.name
}

# 4. Update your EC2 instance to use this profile
resource "aws_instance" "nano_instance" {
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name  # << Critical line

  user_data = file("${path.module}/start_script.sh")
  tags = {
    Name = "Nano-EC2-Instance"
  }
}








/*
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

*/





















