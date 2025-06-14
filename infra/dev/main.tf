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


# 3. Attach S3 read-only policy (add this new resource)
resource "aws_iam_role_policy_attachment" "s3_read" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

#For full S3 access, use this instead:
resource "aws_iam_role_policy_attachment" "s3_full" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}


# 3. Create an instance profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2-SSM-Profile"
  role = aws_iam_role.ec2_ssm_role.name
}






resource "aws_security_group" "web_access" {
  name        = "allow_http"
  description = "Allow HTTP inbound traffic"

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http"
  }
}




# 4. Update your EC2 instance to use this profile
resource "aws_instance" "nano_instance" {
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name  # << Critical line

  # Add the security group here
  vpc_security_group_ids = [aws_security_group.web_access.id]

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





















