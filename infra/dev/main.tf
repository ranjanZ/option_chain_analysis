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

# Check if instance with our tag already exists
data "aws_instances" "existing" {
  filter {
    name   = "tag:Name"
    values = ["Nano-EC2-Instance"]
  }
}

resource "aws_instance" "nano_instance" {
  count         = length(data.aws_instances.existing.ids) == 0 ? 1 : 0
  ami           = "ami-0d1b5a8c13042c939"
  instance_type = "t2.nano"
  
  # Corrected user_data path and using file() instead of filebase64()
  user_data = file("${path.module}/start_script.sh")

  tags = {
    Name = "Nano-EC2-Instance"
  }
}

# Correct way to stop an instance (using aws_instance resource)
resource "null_resource" "stop_instance" {
  triggers = {
    instance_id = length(data.aws_instances.existing.ids) > 0 ? data.aws_instances.existing.ids[0] : aws_instance.nano_instance[0].id
  }

  provisioner "local-exec" {
    command = "aws ec2 stop-instances --instance-ids ${self.triggers.instance_id} --region us-east-2"
  }
}

output "public_ip" {
  value = length(data.aws_instances.existing.ids) > 0 ? data.aws_instances.existing.public_ips[0] : aws_instance.nano_instance[0].public_ip
}







