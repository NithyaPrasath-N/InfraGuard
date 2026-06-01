resource "aws_security_group" "web_sg" {

  name        = "infraguard-web-sg"
  description = "Security Group for InfraGuard"

  ingress {
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
    Name = "InfraGuard-SG"
  }
}


resource "aws_s3_bucket" "logs_bucket" {

  bucket = "infraguard-logs-383423735569"

  tags = {
    Name = "InfraGuard-S3"
  }
}


resource "aws_s3_bucket_versioning" "bucket_versioning" {

  bucket = aws_s3_bucket.logs_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_instance" "web_server" {

  ami           = "ami-0f918f7e67a3323f0"
  instance_type = "t3.micro"

  vpc_security_group_ids = [
    aws_security_group.web_sg.id
  ]

  tags = {
    Name = "InfraGuard-EC2"
  }
}
resource "aws_iam_user" "audit_user" {
  name = "infraguard-audit-user"

  tags = {
    Name = "InfraGuard-IAM-User"
  }
}

resource "aws_iam_user_policy_attachment" "readonly_attach" {

  user = aws_iam_user.audit_user.name

  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}
